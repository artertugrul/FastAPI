"""add remaining columns to posts table

Revision ID: 295dcee41b05
Revises: c40172761187
Create Date: 2023-01-27 23:36:39.517844

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '295dcee41b05'
down_revision = 'c40172761187'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default="True")),
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("Now()")))

    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
