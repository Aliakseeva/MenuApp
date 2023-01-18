"""in db

Revision ID: 86c62d3d9086
Revises: 
Create Date: 2023-01-15 19:59:58.814208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86c62d3d9086'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('submenus_count', sa.Integer(), nullable=True),
    sa.Column('dishes_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('submenus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('menu_id', sa.Integer(), nullable=True),
    sa.Column('dishes_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menus.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dishes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.String(), nullable=True),
    sa.Column('submenu_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['submenu_id'], ['submenus.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dishes')
    op.drop_table('submenus')
    op.drop_table('menus')
    # ### end Alembic commands ###