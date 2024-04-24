import json
from typing import List

from langchain_community.chat_message_histories.sql import (
    BaseChatMessageHistory,
    BaseMessage,
    message_to_dict,
    messages_from_dict,
)

from sqlalchemy.sql import func
from app.database import SessionLocal
from app.chat.models.message import Message
from app.chat.constants.bot import BotType
from app.chat import service


class CustomSQLChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, bot_id: str, user_id: str, chat_id: str, memory: int = 10):
        assert memory % 2 == 0

        self.memory = memory
        self.bot_id = bot_id
        self.user_id = user_id
        self.chat_id = chat_id

    def query_messages(self, session: SessionLocal):
        return service.query_messages(
            session,
            bot=self.bot_id,
            user=self.user_id,
            chat=self.chat_id,
            reverse=False,
        )

    @property
    def messages(self) -> List[BaseMessage]:
        with SessionLocal() as session:
            messages = []

            bot = service.get_bot(session, bot=self.bot_id)
            results = self.query_messages(session).limit(self.memory).all()

            if bot and bot.type in (BotType.LLAMA,):
                if bot.instruction:
                    message_dict = dict(
                        type="system", data=dict(content=bot.instruction)
                    )
                    messages.append(messages_from_dict([message_dict])[0])

            if bot and bot.type in (BotType.MISTRAL, BotType.PHI):
                for role, content in json.loads(bot.instruction):
                    message_dict = dict(type=role, data=dict(content=content))
                    messages.append(messages_from_dict([message_dict])[0])

            for record in results:
                messages.append(messages_from_dict([json.loads(record.message)])[0])

            return messages

    def add_message(self, message: BaseMessage) -> None:
        with SessionLocal() as session:
            db_message = Message(
                bot_id=self.bot_id,
                user_id=self.user_id,
                chat_id=self.chat_id,
                type=message.type,
                text=message.content or "",
                message=json.dumps(message_to_dict(message)),
            )
            session.add(db_message)
            session.commit()

    def clear(self) -> None:
        with SessionLocal() as session:
            messages = self.query_messages(session).all()
            for msg in messages:
                msg.deleted = func.now()
            session.bulk_save_objects(messages)
            session.commit()

    def destroy(self) -> None:
        with SessionLocal() as session:
            messages = self.query_messages(session).all()
            for msg in messages:
                session.delete(msg)
            session.commit()
