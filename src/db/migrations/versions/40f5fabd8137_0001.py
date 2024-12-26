"""0001

Revision ID: 40f5fabd8137
Revises:
Create Date: 2024-12-26 21:40:34.276304

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "40f5fabd8137"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "wallets_requests",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("wallet_address", sa.String(length=34), nullable=False),
        sa.Column("request_time", sa.DateTime(), nullable=False),
        sa.Column("response_time", sa.DateTime(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "success",
                "failure",
                "processing",
                name="wallet_request_status",
                create_constraint=True,
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("wallets_requests")
    # ### end Alembic commands ###