from typing import Tuple

from datetime import datetime
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from app.chat.utils import decode_cursor, encode_cursor
from app.chat.models import Message, Bot, TeamBot


def query_messages(db: Session, reverse: bool = False, **kwargs):
    bot_id = kwargs.pop("bot")
    user_id = kwargs.pop("user")
    chat_id = kwargs.pop("chat")

    messages = (
        db.query(Message)
        .filter(
            Message.bot_id == bot_id,
            Message.user_id == user_id,
            Message.chat_id == chat_id,
        )
        .filter(Message.deleted.is_(None))
    )

    if reverse:
        messages = messages.order_by(desc(Message.ts))

    return messages


def history_chat(db: Session, **kwargs) -> Tuple:
    cursor = kwargs.get("cursor", "")
    limit = min(kwargs.get("limit", 28), 56)

    result = query_messages(db, reverse=True, **kwargs)

    if cursor:
        from_ts = decode_cursor(
            cursor, scheme="next_ts", parser=(float, datetime.utcfromtimestamp)
        )
        result = result.filter(Message.ts <= from_ts)

    messages = result.limit(limit + 1).all()

    if len(messages) > limit:
        next_message = messages.pop()
        next_ts = next_message.ts.timestamp()
        next_cursor = encode_cursor(f"next_ts:{next_ts}")
    else:
        next_cursor = ""
        next_ts = None

    return messages, next_cursor, next_ts


def clear_chat(db: Session, **kwargs):
    messages = query_messages(db, **kwargs).all()
    for msg in messages:
        msg.deleted = datetime.utcnow()
    db.bulk_save_objects(messages)
    db.commit()


def destroy_chat(db: Session, **kwargs):
    messages = query_messages(db, **kwargs).all()
    for msg in messages:
        db.delete(msg)
    db.commit()


def create_bot(db: Session, **kwargs) -> Bot:
    name = kwargs.pop("name")
    type = kwargs.pop("type")
    model = kwargs.pop("model", "")
    status = kwargs.pop("status", "")
    instruction = kwargs.pop("instruction", "")
    bot = Bot(name=name, type=type, model=model, status=status, instruction=instruction)
    db.add(bot)
    db.commit()

    if team_id := kwargs.get("team", ""):
        team_bot = TeamBot(team_id=team_id, bot_id=bot.id)
        db.add(team_bot)
        db.commit()

    return bot


def get_bot(db: Session, **kwargs):
    bot_id = kwargs.pop("bot")

    bot = db.query(Bot).filter(Bot.id == bot_id).filter(Bot.deleted.is_(None)).first()

    return bot


def list_bots(db: Session, **kwargs):
    team_id = kwargs.pop("team")

    bot_ids = select(TeamBot.bot_id).where(TeamBot.team_id == team_id)
    bots = (
        db.query(Bot)
        .filter(Bot.id.in_(bot_ids))
        .filter(Bot.deleted.is_(None))
        .filter(Bot.status == "active")
        .all()
    )

    return bots


def populate_bots(db: Session, **kwargs):
    from app.chat.constants.bot import BotType, BotModel, BotStatus
    from app.chat.constants.llms import (
        instruction,
        instruction_json,
        sophia_instruction,
        llama3_instruction,
    )

    team = kwargs.pop("team")

    mistral = create_bot(
        db,
        name="Mistral",
        type=BotType.MISTRAL,
        model=BotModel.MISTRAL7,
        status=BotStatus.INACTIVE,
        instruction=instruction_json,
        team=team,
    )

    llama = create_bot(
        db,
        name="Meta",
        type=BotType.LLAMA,
        model=BotModel.LLAMA3,
        status=BotStatus.ACTIVE,
        instruction=llama3_instruction,
        team=team,
    )

    llama_sophia = create_bot(
        db,
        name="Sophia",
        type=BotType.LLAMA,
        model=BotModel.LLAMA3,
        status=BotStatus.ACTIVE,
        instruction=sophia_instruction,
        team=team,
    )

    phi = create_bot(
        db,
        name="Flink",
        type=BotType.PHI,
        model=BotModel.PHI2,
        status=BotStatus.ACTIVE,
        instruction=instruction_json,
        team=team,
    )

    return mistral, llama, llama_sophia, phi
