from tests.chat import ChatTestBase
from tests.factories import MessageFactory
from tests.utils import shortid
from app.chat.models import Message


class TestClearChat(ChatTestBase):
    def test_clear_chat_success(self):
        user_id, bot_id, chat_id = "U0123456789", shortid("B"), shortid("C")
        messages = MessageFactory.create_batch(
            20, user_id=user_id, bot_id=bot_id, chat_id=chat_id
        )
        response = self.client.post(
            f"{self.URL}/clear", json=dict(bot=bot_id, chat=chat_id)
        )
        assert response.status_code == 200

        result = self.session.query(Message).filter(
            Message.bot_id == bot_id,
            Message.user_id == user_id,
            Message.chat_id == chat_id,
        )

        assert result.count() == len(messages)
        assert all(msg.deleted for msg in result.all())
