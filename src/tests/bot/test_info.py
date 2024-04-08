from tests.bot import BotTestBase
from tests.factories import BotFactory


class TestInfoBot(BotTestBase):
    def test_info_bot_success(self, llm_instruction):
        bot = BotFactory()
        data = dict(bot=bot.id, instruction=llm_instruction)
        resp = self.post(f"{self.URL}/info", json=data)

        assert resp.bot.id == bot.id
        assert resp.bot.name == bot.name
        assert resp.bot.instruction == llm_instruction
        assert resp.bot.avatar_hash == ""
        assert resp.bot.created
