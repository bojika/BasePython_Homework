"""Create Edge Model

Revision ID: 6d379377114e
Revises: b1355c4e88f9
Create Date: 2022-03-16 11:36:13.520611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d379377114e'
down_revision = 'b1355c4e88f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('edge', sa.Column('meta_data', sa.String(), nullable=True))
    op.drop_column('edge', 'meta')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('edge', sa.Column('meta', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('edge', 'meta_data')
    # ### end Alembic commands ###
