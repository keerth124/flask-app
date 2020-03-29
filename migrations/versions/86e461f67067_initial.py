"""initial

Revision ID: 86e461f67067
Revises: 
Create Date: 2020-03-28 09:47:24.589317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86e461f67067'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inventory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sku', sa.String(length=64), nullable=True),
    sa.Column('brand', sa.String(length=256), nullable=True),
    sa.Column('wtype', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('size', sa.String(length=64), nullable=True),
    sa.Column('price', sa.String(length=64), nullable=True),
    sa.Column('link', sa.String(length=256), nullable=True),
    sa.Column('store', sa.String(length=128), nullable=True),
    sa.Column('quantity', sa.String(length=128), nullable=True),
    sa.Column('address', sa.String(length=256), nullable=True),
    sa.Column('phone', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inventory_address'), 'inventory', ['address'], unique=False)
    op.create_index(op.f('ix_inventory_brand'), 'inventory', ['brand'], unique=False)
    op.create_index(op.f('ix_inventory_sku'), 'inventory', ['sku'], unique=False)
    op.create_index(op.f('ix_inventory_store'), 'inventory', ['store'], unique=False)
    op.create_index(op.f('ix_inventory_wtype'), 'inventory', ['wtype'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_timestamp'), 'post', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_post_timestamp'), table_name='post')
    op.drop_table('post')
    op.drop_table('followers')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_inventory_wtype'), table_name='inventory')
    op.drop_index(op.f('ix_inventory_store'), table_name='inventory')
    op.drop_index(op.f('ix_inventory_sku'), table_name='inventory')
    op.drop_index(op.f('ix_inventory_brand'), table_name='inventory')
    op.drop_index(op.f('ix_inventory_address'), table_name='inventory')
    op.drop_table('inventory')
    # ### end Alembic commands ###