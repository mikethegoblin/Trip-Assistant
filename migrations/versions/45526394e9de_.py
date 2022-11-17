"""empty message

Revision ID: 45526394e9de
Revises: 9755b6b2706b
Create Date: 2022-11-17 15:41:40.908697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45526394e9de'
down_revision = '9755b6b2706b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_flight')
    with op.batch_alter_table('flight', schema=None) as batch_op:
        batch_op.create_foreign_key('week_id', 'week', ['depart_day'], ['id'])

    with op.batch_alter_table('ticket_passenger', schema=None) as batch_op:
        # batch_op.drop_constraint(None, type_='foreignkey')
        # batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('passenger_id', 'passenger', ['passenger_id'], ['id'], ondelete='cascade')
        batch_op.create_foreign_key('ticket_id', 'ticket', ['ticket_id'], ['id'], ondelete='cascade')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ticket_passenger', schema=None) as batch_op:
        batch_op.drop_constraint('ticket_id', type_='foreignkey')
        batch_op.drop_constraint('passenger_id', type_='foreignkey')
        batch_op.create_foreign_key(None, 'ticket', ['ticket_id'], ['id'])
        batch_op.create_foreign_key(None, 'passenger', ['passenger_id'], ['id'])

    with op.batch_alter_table('flight', schema=None) as batch_op:
        batch_op.drop_constraint('week_id', type_='foreignkey')

    op.create_table('_alembic_tmp_flight',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('origin_id', sa.INTEGER(), nullable=True),
    sa.Column('destination_id', sa.INTEGER(), nullable=True),
    sa.Column('depart_time', sa.TIME(), nullable=False),
    sa.Column('duration', sa.BIGINT(), nullable=True),
    sa.Column('arrival_time', sa.TIME(), nullable=False),
    sa.Column('plane', sa.VARCHAR(length=24), nullable=True),
    sa.Column('airline', sa.VARCHAR(length=64), nullable=True),
    sa.Column('economy_fare', sa.FLOAT(), nullable=True),
    sa.Column('business_fare', sa.FLOAT(), nullable=True),
    sa.Column('first_fare', sa.FLOAT(), nullable=True),
    sa.Column('depart_day', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['depart_day'], ['week.id'], name='depart_day'),
    sa.ForeignKeyConstraint(['destination_id'], ['place.id'], ),
    sa.ForeignKeyConstraint(['origin_id'], ['place.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
