"""initial revision

Revision ID: a6e5d9038f9b
Revises:
Create Date: 2024-04-11 16:32:58.459546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "a6e5d9038f9b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "messages",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("bot_id", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("user_id", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("chat_id", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "message",
            postgresql.JSON(astext_type=sa.Text()),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("type", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("text", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "ts",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "deleted", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name="messages_pkey"),
    )
    op.create_index("ix_messages_user_id", "messages", ["user_id"], unique=False)
    op.create_index("ix_messages_chat_id", "messages", ["chat_id"], unique=False)
    op.create_index("ix_messages_bot_id", "messages", ["bot_id"], unique=False)
    op.create_table(
        "team_bots",
        sa.Column("bot_id", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("team_id", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("bot_id", "team_id", name="team_bots_pkey"),
    )
    op.create_table(
        "bots",
        sa.Column("id", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("temp_hash", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("avatar_hash", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "instruction",
            postgresql.JSON(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "deleted", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "created",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "updated", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name="bots_pkey"),
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("bots")
    op.drop_table("team_bots")
    op.drop_index("ix_messages_bot_id", table_name="messages")
    op.drop_index("ix_messages_chat_id", table_name="messages")
    op.drop_index("ix_messages_user_id", table_name="messages")
    op.drop_table("messages")
    # ### end Alembic commands ###
