"""empty message

Revision ID: 440555c2c5dd
Revises: 267ce1be894f
Create Date: 2021-04-24 22:33:02.953328

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '440555c2c5dd'
down_revision = '267ce1be894f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('feed', 'subtitle',
               existing_type=mysql.VARCHAR(length=80),
               type_=sa.String(length=180),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('feed', 'subtitle',
               existing_type=sa.String(length=180),
               type_=mysql.VARCHAR(length=80),
               existing_nullable=True)
    # ### end Alembic commands ###
