"""create account table

Revision ID: 9e3dec42e33c
Revises: 
Create Date: 2020-12-01 18:33:41.437541

"""
from alembic import op
import sqlalchemy as sa
from models import *


# revision identifiers, used by Alembic.
revision = '9e3dec42e33c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        Column('uid', Integer, unique=True),
        Column('username', String, primary_key=True),
        Column('password', String),
        Column('role', Integer))

    op.create_table('cities',
        Column('cid', Integer, unique=True),
        Column('name', String, primary_key=True))

    op.create_table('ads',
        Column('adid', Integer, primary_key=True),
        Column('title', String),
        Column('content', String),
        Column('author', String, ForeignKey(User.username)),
        Column('city', String, ForeignKey(City.name)))


def downgrade():
    op.drop_table(User)
    op.drop_table(City)
    op.drop_table(AD)

