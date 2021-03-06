"""empty message

Revision ID: e6ba91cf6ea4
Revises: cfdf12773f54
Create Date: 2020-04-21 10:43:55.415913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6ba91cf6ea4'
down_revision = 'cfdf12773f54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('call', schema=None) as batch_op:
        batch_op.add_column(sa.Column('errors', sa.String(length=512), nullable=True))
        batch_op.add_column(sa.Column('status', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('status_msg', sa.String(length=256), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('call', schema=None) as batch_op:
        batch_op.drop_column('status_msg')
        batch_op.drop_column('status')
        batch_op.drop_column('errors')

    # ### end Alembic commands ###
