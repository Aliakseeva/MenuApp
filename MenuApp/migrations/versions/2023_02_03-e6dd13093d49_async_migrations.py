"""async migrations

Revision ID: e6dd13093d49
Revises:
Create Date: 2023-02-03 20:34:48.618837

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e6dd13093d49"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "menus",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("submenus_count", sa.Integer(), nullable=True),
        sa.Column("dishes_count", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "submenus",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("menu_id", sa.Integer(), nullable=True),
        sa.Column("dishes_count", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["menu_id"], ["menus.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "dishes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.String(), nullable=True),
        sa.Column("submenu_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["submenu_id"], ["submenus.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("dishes")
    op.drop_table("submenus")
    op.drop_table("menus")
    # ### end Alembic commands ###
