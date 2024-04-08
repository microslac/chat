import math
import pytest
import base64

from tests.chat import ChatTestBase
from tests.factories import MessageFactory
from tests.utils import shortid


class TestHistoryChat(ChatTestBase):
    @pytest.mark.parametrize("num_messages", (20, 50))
    def test_clear_chat_success(self, num_messages):
        user_id, bot_id, chat_id = "U0123456789", shortid("B"), shortid("C")
        messages = MessageFactory.create_batch(
            num_messages, user_id=user_id, bot_id=bot_id, chat_id=chat_id
        )

        limit = 28
        data = dict(bot=bot_id, chat=chat_id, limit=limit)
        resp = self.post(f"{self.URL}/history", json=data, status=200)

        assert resp.chat == bot_id
        assert len(resp.messages) == min(limit, len(messages))
        assert resp.has_more == (num_messages > limit)
        if next_cursor := resp.response_metadata.next_cursor:
            next_dt = messages[limit + 1].ts
            next_ts = f"next_ts:{math.trunc(next_dt.timestamp())}"
            next_cursor = base64.b64decode(next_cursor).decode("utf-8")
            assert next_cursor.startswith(next_ts)
