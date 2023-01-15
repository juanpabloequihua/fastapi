"""add foreign key to post

Revision ID: c8a09609d9c3
Revises: ed91ee9244a7
Create Date: 2023-01-15 14:45:30.418841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8a09609d9c3'
down_revision = 'ed91ee9244a7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", 
                            referent_table='users', local_cols=['owner_id'], 
                            remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:

    op.drop_constraint('posts_users_fk', table_name= 'posts')
    op.drop_column("posts",  'owner_id')
    pass
