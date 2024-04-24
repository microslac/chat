import json
from contextlib import suppress
from typing import Optional, List
from datetime import datetime
from pydantic import field_serializer
from app.schema import BaseModel, SchemaModel, ResponseOut
from app.chat.utils import to_timestamp
from app.chat.constants.bot import BotType


class BotData(SchemaModel):
    id: str
    type: str
    name: str
    model: str
    status: str
    created: datetime
    updated: Optional[datetime] = None
    instruction: str
    avatar_hash: str

    @field_serializer("created", "updated")
    def serializer_dt(self, dt: datetime):
        return to_timestamp(dt)

    @field_serializer("instruction")
    def serializer_instruction(self, instruction: str):
        if self.type in (BotType.MISTRAL, BotType.PHI):
            with suppress(ValueError):
                messages = json.loads(instruction)
                return messages.pop(0).pop()
        return instruction


class BotInfoIn(BaseModel):
    bot: str


class BotInfoOut(ResponseOut):
    bot: BotData


class BotCreateIn(BaseModel):
    name: str
    type: Optional[str] = ""
    model: Optional[str] = ""
    team: Optional[str] = None
    instruction: Optional[str] = ""
    status: Optional[str] = "inactive"


class BotListIn(BaseModel):
    team: str


class BotListOut(ResponseOut):
    team: str
    bots: List[BotData]


class BotPopulateIn(BaseModel):
    team: str


class BotPopulateOut(ResponseOut):
    team: str
