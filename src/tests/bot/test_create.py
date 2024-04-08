from app.database import shortid
from tests.bot import BotTestBase


class TestInfoBot(BotTestBase):
    def test_create_bot_success(self, llm_instruction):
        data = dict(name="bot", type="mistral", instruction=llm_instruction)
        resp = self.post(f"{self.URL}/create", json=data)

        assert resp.bot.id.startswith("B")
        assert resp.bot.instruction == llm_instruction
        assert resp.bot.name == "bot"
        assert resp.bot.created

    def test_create_bot_with_team_success(self, llm_instruction):
        team_id = shortid("T")
        data = dict(name="bot", team=team_id, instruction=llm_instruction)
        resp = self.post(f"{self.URL}/create", json=data)

        assert resp.bot.id.startswith("B")
        assert resp.bot.instruction == llm_instruction
        assert resp.bot.name == "bot"
        assert resp.bot.created
