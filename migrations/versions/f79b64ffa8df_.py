"""empty message

Revision ID: f79b64ffa8df
Revises: 9a284253717e
Create Date: 2022-11-15 22:51:19.068063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f79b64ffa8df'
down_revision = '9a284253717e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flight', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'week', ['depart_day'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flight', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###