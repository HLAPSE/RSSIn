"""empty message

Revision ID: 2fbb04edb5ee
Revises: 6c2c6ed24e7d
Create Date: 2021-03-03 00:00:41.822347

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2fbb04edb5ee'
down_revision = '6c2c6ed24e7d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('entry', 'content',
               existing_type=mysql.TEXT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('entry', 'content',
               existing_type=mysql.TEXT(),
               nullable=False)
    # ### end Alembic commands ###
