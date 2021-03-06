"""add language to posts

Revision ID: 3add5ce64e61
Revises: 9807b7739dc3
Create Date: 2021-09-01 16:48:36.041487

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3add5ce64e61'
down_revision = '9807b7739dc3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('language', sa.String(length=5), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'language')
    # ### end Alembic commands ###
