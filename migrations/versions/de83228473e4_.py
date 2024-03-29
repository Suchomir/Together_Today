"""empty message

Revision ID: de83228473e4
Revises: 3b16cc4bf37d
Create Date: 2022-12-31 14:27:30.358091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de83228473e4'
down_revision = '3b16cc4bf37d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('current_photos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('current_photo_id', sa.Integer(), nullable=True),
    sa.Column('current_photo', sa.String(length=128), nullable=True),
    sa.Column('current_message', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('image_counters')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('image_counters',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('current_photo_id', sa.INTEGER(), nullable=True),
    sa.Column('current_photo', sa.VARCHAR(length=128), nullable=True),
    sa.Column('current_message', sa.VARCHAR(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('current_photos')
    # ### end Alembic commands ###
