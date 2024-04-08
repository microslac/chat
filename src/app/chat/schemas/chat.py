from typing import List, Optional
from typing_extensions import TypedDict

from app.schema import BaseModel, ResponseOut


class MessageData(BaseModel):
    id: str
    bot: str
    type: str
    user: str
    chat: str
    text: str
    ts: float


class ChatHistoryIn(BaseModel):
    bot: str
    chat: str
    limit: Optional[int] = 28
    cursor: Optional[str] = None


class ResponseMetadata(TypedDict):
    next_cursor: str


class ChatHistoryOut(ResponseOut):
    chat: str
    messages: List[MessageData]
    response_metadata: ResponseMetadata
    has_more: bool


class ChatClearIn(BaseModel):
    bot: str
    chat: str


class ChatDestroyIn(BaseModel):
    bot: str
    chat: str
    user: str
