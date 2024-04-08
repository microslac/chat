from tests.chat import ChatTestBase
from tests.factories import MessageFactory
from tests.utils import shortid
from app.chat.models import Message


class TestDestroyChat(ChatTestBase):
    def test_destroy_chat_success(self):
        user_id, bot_id, chat_id = "U0123456789", shortid("B"), shortid("C")
        MessageFactory.create_batch(20, user_id=user_id, bot_id=bot_id, chat_id=chat_id)

        data = dict(bot=bot_id, user=user_id, chat=chat_id)
        self.post(f"{self.URL}/destroy", json=data, status=200, internal=True)

        result = self.session.query(Message).filter(
            Message.bot_id == bot_id,
            Message.user_id == user_id,
            Message.chat_id == chat_id,
        )

        assert result.count() == 0
