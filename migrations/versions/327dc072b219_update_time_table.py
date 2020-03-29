"""update time table

Revision ID: 327dc072b219
Revises: 86e461f67067
Create Date: 2020-03-28 10:27:53.252574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '327dc072b219'
down_revision = '86e461f67067'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('last_update',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recordcount', sa.Integer(), nullable=True),
    sa.Column('datestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_last_update_datestamp'), 'last_update', ['datestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_last_update_datestamp'), table_name='last_update')
    op.drop_table('last_update')
    # ### end Alembic commands ###