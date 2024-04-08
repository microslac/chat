import uuid
import json
import factory
from faker import Factory
from app.chat.models import Message
from tests.factories.base import BaseFactory, FactoryMeta
from tests.utils import shortid

__all__ = ["MessageFactory"]

fake = Factory.create()


def fake_message(content: str) -> str:
    msg = {
        "type": "human",
        "data": {
            "content": content,
            "additional_kwargs": {},
            "response_metadata": {},
            "type": "human",
            "name": None,
            "id": None,
            "example": False,
        },
    }
    return json.dumps(msg)


class MessageFactory(BaseFactory):
    class Meta(FactoryMeta):
        model = Message

    id = factory.LazyAttribute(lambda _: uuid.uuid4())
    bot_id = factory.LazyAttribute(lambda _: shortid("B"))
    user_id = factory.LazyAttribute(lambda _: shortid("U"))
    chat_id = factory.LazyAttribute(lambda _: shortid("C"))
    text = factory.LazyAttribute(lambda _: fake.text())
    type = factory.LazyAttribute(lambda _: "human")
    message = factory.LazyAttribute(lambda m: fake_message(m.text))
