"""remove delete orphan

Revision ID: 130bcde3786d
Revises: 45526394e9de
Create Date: 2022-11-18 19:30:52.196619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '130bcde3786d'
down_revision = '45526394e9de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.alter_column('booking_date',
               existing_type=sa.DATETIME(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.alter_column('booking_date',
               existing_type=sa.DATETIME(),
               nullable=False)

    # ### end Alembic commands ###
