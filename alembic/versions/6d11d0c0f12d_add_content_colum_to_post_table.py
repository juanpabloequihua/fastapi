"""add content colum to post table

Revision ID: 6d11d0c0f12d
Revises: d3f0004a10e8
Create Date: 2023-01-15 14:31:37.538453

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d11d0c0f12d'
down_revision = 'd3f0004a10e8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
