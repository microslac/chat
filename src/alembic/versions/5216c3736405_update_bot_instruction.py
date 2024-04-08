"""update bot instruction

Revision ID: 5216c3736405
Revises: a6e5d9038f9b
Create Date: 2024-04-11 16:34:56.982941

"""
import logging
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm

logger = logging.getLogger("alembic")

# revision identifiers, used by Alembic.
revision: str = "5216c3736405"
down_revision: Union[str, None] = "a6e5d9038f9b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    from app.chat.models import Bot

    bind = op.get_bind()
    session = orm.Session(bind=bind)

    bots = session.query(Bot).all()
    for bot in bots:
        if isinstance(bot.instruction, dict):
            bot.instruction = bot.instruction.get("messages").pop(0).pop()
    session.bulk_save_objects(bots)
    session.commit()

    op.alter_column(
        table_name="bots",
        column_name="instruction",
        existing_type=sa.JSON(),
        existing_nullable=True,
        type_=sa.String(),
        server_default="",
    )


def downgrade() -> None:
    op.alter_column(
        table_name="bots",
        column_name="instruction",
        existing_type=sa.String(),
        existing_nullable=False,
        type_=sa.JSON(),
        server_default=sa.text("{}"),
    )
