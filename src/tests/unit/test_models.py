import json

from app.chat.models import Bot, TeamBot, Message
from app.database import shortid
from tests.base import UnitTest
from tests.conftest import instruction


class TestModels(UnitTest):
    def test_bot_model(self):
        bot = Bot(name="bot", type="openai", instruction=instruction)

        assert bot.name == "bot"
        assert bot.type == "openai"
        assert bot.id.startswith("B")
        assert bot.instruction == instruction
        assert bot.avatar_hash == ""
        assert bot.temp_hash == ""

    def test_team_bot_model(self):
        team_id = shortid("T")
        bot = Bot(name="bot", instruction=instruction)
        team_bot = TeamBot(team_id=team_id, bot_id=bot.id)

        assert team_bot.bot_id == bot.id
        assert team_bot.team_id == team_id

    def test_message_model(self):
        bot = Bot(name="bot")
        user_id = shortid("U")
        chat_id = shortid("C")
        text = "This is a test message"
        message_dict = {
            "type": "human",
            "data": {
                "content": text,
                "additional_kwargs": {},
                "response_metadata": {},
                "type": "human",
                "name": None,
                "id": None,
                "example": False,
            },
        }

        message = Message(
            bot_id=bot.id,
            user_id=user_id,
            chat_id=chat_id,
            message=json.dumps(message_dict),
            text=text,
        )

        assert message.id
        assert message.bot_id == bot.id
        assert message.user_id == user_id
        assert message.chat_id == chat_id
        assert message.deleted is None
        assert message.text == text

        assert message.message
