"""empty message

Revision ID: 79ac56ce7c3d
Revises: 4156c9512c69
Create Date: 2020-04-19 16:06:21.413710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79ac56ce7c3d'
down_revision = '4156c9512c69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('call', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_on', sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f('ix_call_handle'), ['handle'], unique=True)

    with op.batch_alter_table('call_result', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_call_result_date'), ['date'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('call_result', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_call_result_date'))

    with op.batch_alter_table('call', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_call_handle'))
        batch_op.drop_column('created_on')

    # ### end Alembic commands ###