"""add image column to city table

Revision ID: 4a441be514a1
Revises: bc5479718dcf
Create Date: 2022-11-04 21:29:19.291477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a441be514a1'
down_revision = 'bc5479718dcf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('city', sa.Column('image', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('city', 'image')
    # ### end Alembic commands ###