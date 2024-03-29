"""empty message

Revision ID: 243dcbdac999
Revises: 3af5c6a1076d
Create Date: 2022-12-28 18:44:01.533019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '243dcbdac999'
down_revision = '3af5c6a1076d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('image_counters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('counter', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('image_counters')
    # ### end Alembic commands ###
