import factory
from faker import Factory
from app.chat.models import Bot, TeamBot
from app.database import shortid
from tests.factories.base import BaseFactory, FactoryMeta
from tests.conftest import instruction

__all__ = ["BotFactory", "TeamBotFactory"]

fake = Factory.create()


class BotFactory(BaseFactory):
    class Meta(FactoryMeta):
        model = Bot

    id = factory.LazyAttribute(lambda _: shortid("B"))
    name = factory.LazyAttribute(lambda _: fake.name())
    instruction = factory.LazyAttribute(lambda _: instruction)


class TeamBotFactory(BaseFactory):
    class Meta(FactoryMeta):
        model = TeamBot

    bot_id = factory.LazyAttribute(lambda _: shortid("B"))
    team_id = factory.LazyAttribute(lambda _: shortid("T"))
