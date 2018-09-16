"""empty message

Revision ID: ce510d8b8083
Revises: 5d7c8d1ce38f
Create Date: 2018-09-15 02:24:35.796289

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ce510d8b8083'
down_revision = '5d7c8d1ce38f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('website', 'url',
               existing_type=mysql.VARCHAR(length=2083))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('website', 'url',
               existing_type=mysql.VARCHAR(length=2083))
    # ### end Alembic commands ###