"""Add User model

Revision ID: 161170fe476
Revises: 37973729868
Create Date: 2014-12-25 01:24:46.673537

"""

# revision identifiers, used by Alembic.
revision = '161170fe476'
down_revision = '37973729868'
branch_labels = ()
depends_on = None

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('login', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('lastname', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('location', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('date_joined', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('last_login', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('is_admin', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('use_avatar', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey')
    )
    ### end Alembic commands ###