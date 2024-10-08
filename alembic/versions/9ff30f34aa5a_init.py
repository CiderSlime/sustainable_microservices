"""init

Revision ID: 9ff30f34aa5a
Revises: 
Create Date: 2024-04-06 22:58:58.251920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ff30f34aa5a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('uid', sa.UUID(), nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('gender', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('social_insurance_number', sa.String(), nullable=True),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('balance', sa.Double(), nullable=False),
    sa.Column('created_at', sa.Date(), nullable=False),
    sa.Column('updated_at', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('transactions',
    sa.Column('uid', sa.UUID(), nullable=False),
    sa.Column('value', sa.Integer(), nullable=False),
    sa.Column('latency', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.UUID(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transactions')
    op.drop_table('customers')
    # ### end Alembic commands ###
