from factory.alchemy import SQLAlchemyModelFactory
from tests.common import Session
from faker import Faker

fake = Faker()


class BaseFactory(SQLAlchemyModelFactory):
    pass


class FactoryMeta:
    sqlalchemy_session = Session
