"""Order fix - cascade user-deletion

Revision ID: 17d6812f7b62
Revises: b8d9d506e565
Create Date: 2025-02-20 18:14:46.809342

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "17d6812f7b62"
down_revision: Union[str, None] = "b8d9d506e565"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("fk_orders_user_id_users", "orders", type_="foreignkey")
    op.create_foreign_key(
        op.f("fk_orders_user_id_users"),
        "orders",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f("fk_orders_user_id_users"), "orders", type_="foreignkey")
    op.create_foreign_key(
        "fk_orders_user_id_users", "orders", "users", ["user_id"], ["id"]
    )
    # ### end Alembic commands ###
