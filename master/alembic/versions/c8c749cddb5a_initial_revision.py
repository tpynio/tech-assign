"""Initial revision

Revision ID: c8c749cddb5a
Revises:
Create Date: 2025-02-17 23:02:22.188514

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from core.database.models.order import OrderTypes


def fill_order_types():
    order_types = ",".join(map(lambda elem: f'("{elem}")', OrderTypes))
    op.execute(sa.text(f"INSERT INTO order_types (name) VALUES {order_types}"))


# revision identifiers, used by Alembic.
revision: str = "c8c749cddb5a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "order_types",
        sa.Column("name", sa.String(length=16), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "orders",
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.Column("weight", sa.Integer(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("deliver_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["type_id"],
            ["order_types.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    fill_order_types()
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("orders")
    op.drop_table("users")
    op.drop_table("order_types")
    # ### end Alembic commands ###
