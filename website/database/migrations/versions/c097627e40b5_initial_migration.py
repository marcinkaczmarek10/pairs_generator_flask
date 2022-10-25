"""initial migration

Revision ID: c097627e40b5
Revises: ac1a3d89febd
Create Date: 2022-10-25 20:17:02.153790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c097627e40b5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=40), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('is_confirmed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('drawCounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usersPeople',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person_name', sa.String(length=40), nullable=False),
    sa.Column('person_email', sa.String(length=120), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('randomPairs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_person_name', sa.String(length=40), nullable=False),
    sa.Column('first_person_email', sa.String(length=120), nullable=False),
    sa.Column('second_person_name', sa.String(length=40), nullable=False),
    sa.Column('second_person_email', sa.String(length=120), nullable=False),
    sa.Column('draw_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['draw_count'], ['drawCounts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('whichDraws',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('draw_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['draw_count'], ['drawCounts.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('draw_count')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('whichDraws')
    op.drop_table('randomPairs')
    op.drop_table('usersPeople')
    op.drop_table('drawCounts')
    op.drop_table('users')
    # ### end Alembic commands ###
