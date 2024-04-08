from tests.utils import shortid
from tests.bot import BotTestBase
from tests.factories import BotFactory, TeamBotFactory


class TestListBots(BotTestBase):
    def test_list_bots_success(self):
        team_id = shortid("T")
        bots = BotFactory.create_batch(6)
        team_bots = [TeamBotFactory(team_id=team_id, bot_id=bot.id) for bot in bots]

        data = dict(team=team_id)
        resp = self.post(f"{self.URL}/list", json=data)

        assert list(sorted(bot.id for bot in resp.bots)) == list(
            sorted(tb.bot_id for tb in team_bots)
        )
