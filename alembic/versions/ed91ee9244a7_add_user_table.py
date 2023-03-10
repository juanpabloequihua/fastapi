"""add user table

Revision ID: ed91ee9244a7
Revises: 6d11d0c0f12d
Create Date: 2023-01-15 14:37:09.367966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed91ee9244a7'
down_revision = '6d11d0c0f12d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable = False),
                    sa.Column('email', sa.String(), nullable = False),
                    sa.Column('password', sa.String(), nullable = False), 
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                                server_default=sa.text('now()'), nullable = False),
                    sa.PrimaryKeyConstraint('id'), 
                    sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
