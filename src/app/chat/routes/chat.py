from fastapi import status
from fastapi import Depends, APIRouter
from app.database import db_session, Session
from app.authentication import Token, authorization_token, internal_header
from app.chat import service
from app.chat.schemas.chat import (
    MessageData,
    ResponseOut,
    ChatHistoryIn,
    ChatHistoryOut,
    ChatClearIn,
    ChatDestroyIn,
)
from app.chat.utils import to_timestamp

router = APIRouter(prefix="/chat")


@router.post("/history", status_code=status.HTTP_200_OK, response_model=ChatHistoryOut)
async def history(
    body: ChatHistoryIn,
    db: Session = Depends(db_session),
    token: Token = Depends(authorization_token),
):
    data = dict(**body.model_dump(), user=token.user_id)
    messages, next_cursor, next_ts = service.history_chat(db, **data)
    messages = [
        MessageData(
            id=str(msg.id),
            type=msg.type,
            bot=msg.bot_id,
            user=msg.user_id,
            chat=msg.chat_id,
            ts=to_timestamp(msg.ts),
            text=msg.text,
        )
        for msg in messages
    ]

    resp = ChatHistoryOut(
        ok=True,
        chat=body.bot,
        messages=messages,
        response_metadata=dict(next_cursor=next_cursor),
        has_more=bool(next_cursor),
    )

    return resp


@router.post("/clear", status_code=status.HTTP_200_OK, response_model=ResponseOut)
async def clear(
    body: ChatClearIn,
    db: Session = Depends(db_session),
    token: Token = Depends(authorization_token),
):
    data = dict(**body.model_dump(), user=token.user_id)
    service.clear_chat(db, **data)
    return ResponseOut(ok=True)


@router.post("/destroy", status_code=status.HTTP_200_OK, response_model=ResponseOut)
async def destroy(
    body: ChatDestroyIn,
    db: Session = Depends(db_session),
    internal: bool = Depends(internal_header),
):
    service.destroy_chat(db, **body.model_dump())
    return ResponseOut(ok=True)
