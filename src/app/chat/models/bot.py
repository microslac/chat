from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.sql import func

from app.database import Base, shortid


class Bot(Base):
    __tablename__ = "bots"

    id = Column(String, primary_key=True, default=lambda _: shortid("B"))
    name = Column(String, nullable=False)
    type = Column(String, default="")
    model = Column(String, default="")
    temp_hash = Column(String, default="")
    instruction = Column(String, default="")
    avatar_hash = Column(String, default="")
    status = Column(String, default="inactive")

    deleted = Column(TIMESTAMP, nullable=True)
    created = Column(TIMESTAMP, server_default=func.now())
    updated = Column(TIMESTAMP, server_onupdate=func.current_time())


class TeamBot(Base):
    __tablename__ = "team_bots"

    bot_id = Column(String, nullable=False, primary_key=True)
    team_id = Column(String, nullable=False, primary_key=True)
