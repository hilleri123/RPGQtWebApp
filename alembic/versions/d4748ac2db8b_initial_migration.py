"""Initial migration

Revision ID: d4748ac2db8b
Revises: ea47720b2427
Create Date: 2024-12-30 12:21:06.520441

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4748ac2db8b'
down_revision: Union[str, None] = 'ea47720b2427'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('PlayerAction', sa.Column('add_time_secs', sa.Integer(), nullable=True))
    op.drop_column('PlayerAction', 'add_time')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('PlayerAction', sa.Column('add_time', sa.DATETIME(), nullable=True))
    op.drop_column('PlayerAction', 'add_time_secs')
    # ### end Alembic commands ###
