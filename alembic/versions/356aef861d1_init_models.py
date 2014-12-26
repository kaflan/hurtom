"""Init models

Revision ID: 356aef861d1
Revises: 51b35ea457a
Create Date: 2014-12-26 06:34:37.261974

"""

# revision identifiers, used by Alembic.
revision = '356aef861d1'
down_revision = '51b35ea457a'
branch_labels = None
depends_on = None

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment')
    op.drop_table('user')
    op.drop_table('backer')
    op.drop_table('project')
    op.drop_table('image')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('image',
                    sa.Column(
                        'filename', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
                    sa.Column(
                        'owner_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column(
                        'project_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['owner_id'], ['user.id'], name='image_owner_id_fkey'),
                    sa.ForeignKeyConstraint(
                        ['project_id'], ['project.id'], name='image_project_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='image_pkey')
                    )
    op.create_table('project',
                    sa.Column(
                        'title', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column(
                        'slug', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column(
                        'description', sa.TEXT(), autoincrement=False, nullable=True),
                    sa.Column(
                        'sum', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('date_start', postgresql.TIMESTAMP(),
                              autoincrement=False, nullable=True),
                    sa.Column('date_end', postgresql.TIMESTAMP(),
                              autoincrement=False, nullable=True),
                    sa.Column(
                        'owner_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('id', sa.INTEGER(), server_default=sa.text(
                        "nextval('project_id_seq'::regclass)"), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['owner_id'], ['user.id'], name='project_owner_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='project_pkey'),
                    postgresql_ignore_search_path=False
                    )
    op.create_table('backer',
                    sa.Column(
                        'position', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column(
                        'bigger', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column(
                        'description', sa.TEXT(), autoincrement=False, nullable=True),
                    sa.Column(
                        'limit', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column(
                        'owner_id', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['owner_id'], ['user.id'], name='backer_owner_id_fkey'),
                    sa.PrimaryKeyConstraint(
                        'owner_id', 'id', name='backer_pkey')
                    )
    op.create_table('user',
                    sa.Column(
                        'email', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column(
                        'password', sa.VARCHAR(length=60), autoincrement=False, nullable=True),
                    sa.Column(
                        'login', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
                    sa.Column(
                        'name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
                    sa.Column('lastname', sa.VARCHAR(length=50),
                              autoincrement=False, nullable=True),
                    sa.Column(
                        'location', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('date_joined', postgresql.TIMESTAMP(),
                              autoincrement=False, nullable=True),
                    sa.Column('last_login', postgresql.TIMESTAMP(),
                              autoincrement=False, nullable=True),
                    sa.Column(
                        'active', sa.BOOLEAN(), autoincrement=False, nullable=True),
                    sa.Column(
                        'admin', sa.BOOLEAN(), autoincrement=False, nullable=True),
                    sa.Column(
                        'use_avatar', sa.BOOLEAN(), autoincrement=False, nullable=True),
                    sa.Column(
                        'github', postgresql.JSON(), autoincrement=False, nullable=True),
                    sa.Column(
                        'google', postgresql.JSON(), autoincrement=False, nullable=True),
                    sa.Column('avatar', sa.VARCHAR(length=200),
                              autoincrement=False, nullable=True),
                    sa.Column('id', sa.INTEGER(), server_default=sa.text(
                        "nextval('user_id_seq'::regclass)"), nullable=False),
                    sa.PrimaryKeyConstraint('id', name='user_pkey'),
                    postgresql_ignore_search_path=False
                    )
    op.create_table('payment',
                    sa.Column(
                        'date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
                    sa.Column(
                        'sum', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column(
                        'project_id', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column(
                        'owner_id', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['owner_id'], ['user.id'], name='payment_owner_id_fkey'),
                    sa.ForeignKeyConstraint(
                        ['project_id'], ['project.id'], name='payment_project_id_fkey'),
                    sa.PrimaryKeyConstraint(
                        'project_id', 'owner_id', 'id', name='payment_pkey')
                    )
    ### end Alembic commands ###
