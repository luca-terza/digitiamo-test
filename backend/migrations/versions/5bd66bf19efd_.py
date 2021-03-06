"""empty message

Revision ID: 5bd66bf19efd
Revises: 4df45b814015
Create Date: 2020-04-18 22:56:17.273933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bd66bf19efd'
down_revision = '4df45b814015'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('call', schema=None) as batch_op:
        batch_op.add_column(sa.Column('path', sa.String(length=256), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('call', schema=None) as batch_op:
        batch_op.drop_column('path')

    # ### end Alembic commands ###
