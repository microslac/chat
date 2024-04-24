from fastapi import status
from fastapi import Depends, APIRouter
from app.database import db_session, Session
from app.chat import service
from app.chat.schemas.bot import (
    BotData,
    BotInfoIn,
    BotInfoOut,
    BotCreateIn,
    BotListIn,
    BotListOut,
    BotPopulateIn,
    BotPopulateOut,
)

router = APIRouter(prefix="/bots")


@router.post(
    "/create", status_code=status.HTTP_200_OK, response_model=BotInfoOut, tags=["bot"]
)
async def create(body: BotCreateIn, db: Session = Depends(db_session)):
    bot = service.create_bot(db=db, **body.model_dump())
    resp = BotInfoOut(bot=BotData.dump(bot))
    return resp


@router.post(
    "/info", status_code=status.HTTP_200_OK, response_model=BotInfoOut, tags=["bot"]
)
async def info(body: BotInfoIn, db: Session = Depends(db_session)):
    bot = service.get_bot(db=db, **body.model_dump())
    resp = BotInfoOut(bot=BotData.dump(bot))
    return resp


@router.post(
    "/list", status_code=status.HTTP_200_OK, response_model=BotListOut, tags=["bot"]
)
async def list_(body: BotListIn, db: Session = Depends(db_session)):
    bots = service.list_bots(db=db, **body.model_dump())
    resp = BotListOut(team=body.team, bots=BotData.dump(bots, many=True))
    return resp


@router.post(
    "/_populate",
    status_code=status.HTTP_200_OK,
    response_model=BotPopulateOut,
    tags=["bot"],
)
async def populate(body: BotPopulateIn, db: Session = Depends(db_session)):
    service.populate_bots(db=db, **body.model_dump())
    resp = BotPopulateOut(team=body.team)
    return resp
