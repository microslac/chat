from app.chat.constants.llms import *  # noqa

import json
from contextlib import suppress
from typing import Optional, List
from datetime import datetime
from pydantic import field_serializer
from app.schema import BaseModel, SchemaModel, ResponseOut
from app.chat.utils import to_timestamp


class BotData(SchemaModel):
    id: str
    type: str
    name: str
    created: datetime
    updated: Optional[datetime] = None
    instruction: str
    avatar_hash: str

    @field_serializer("created", "updated")
    def serializer_dt(self, dt: datetime):
        return to_timestamp(dt)

    @field_serializer("instruction")
    def serializer_instruction(self, instruction: str):
        if self.type == "mistral":
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
    team: Optional[str] = None
    instruction: Optional[str] = ""


class AmiCreateIn(BotCreateIn):
    name: str = "Ami"
    type: str = "mistral"
    team: str = "T5L7FB6WP4IO"
    instruction: str = ami_instruction


class BotListIn(BaseModel):
    team: str


class BotListOut(ResponseOut):
    team: str
    bots: List[BotData]
