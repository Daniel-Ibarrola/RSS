"""alert inital migration

Revision ID: 00a0290f156c
Revises: 
Create Date: 2023-05-18 16:56:47.883387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00a0290f156c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alerts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.TIMESTAMP(), nullable=False),
    sa.Column('city', sa.Integer(), nullable=False),
    sa.Column('region', sa.Integer(), nullable=False),
    sa.Column('is_event', sa.Boolean(), nullable=False),
    sa.Column('identifier', sa.String(length=50), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['alerts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('alerts')
    # ### end Alembic commands ###