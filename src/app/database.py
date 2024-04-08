from string import ascii_uppercase, digits
from shortuuid import ShortUUID
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.settings import settings

engine = create_engine(settings.db.url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

suuid = ShortUUID(alphabet=ascii_uppercase + digits)


def shortid(prefix: str, length: int = 11):
    return prefix + suuid.random(length=length)


def create_all():
    Base.metadata.create_all(bind=engine)


def db_session():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
