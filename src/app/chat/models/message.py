import uuid
from app.database import Base

from sqlalchemy import Column, String, TIMESTAMP, UUID, JSON
from sqlalchemy.sql import func


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bot_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    chat_id = Column(String, nullable=False, index=True)
    message = Column(JSON, nullable=False)
    type = Column(String, nullable=False)
    text = Column(String, default="")

    ts = Column(TIMESTAMP, server_default=func.now())
    deleted = Column(TIMESTAMP, nullable=True)
