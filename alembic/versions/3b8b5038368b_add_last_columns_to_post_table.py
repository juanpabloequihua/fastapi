"""add last columns to post table

Revision ID: 3b8b5038368b
Revises: c8a09609d9c3
Create Date: 2023-01-15 14:50:41.984241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b8b5038368b'
down_revision = 'c8a09609d9c3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable = False, server_default= 'TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                    nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column("posts", "published" )
    op.drop_column("posts", "created_at")
    pass
