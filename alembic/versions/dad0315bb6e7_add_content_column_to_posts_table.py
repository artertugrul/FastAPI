"""add content column to posts table

Revision ID: dad0315bb6e7
Revises: 5ad27e2ef521
Create Date: 2023-01-27 23:03:39.395754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dad0315bb6e7'
down_revision = '5ad27e2ef521'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
