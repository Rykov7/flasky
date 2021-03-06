"""empty message

Revision ID: 5606afe4b600
Revises: 727e522b7420
Create Date: 2022-05-25 22:30:49.123551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5606afe4b600'
down_revision = '727e522b7420'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('author_id', sa.Integer(), nullable=True))
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'users', ['author_id'], ['id'])
    op.drop_column('posts', 'auth_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('auth_id', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'users', ['auth_id'], ['id'])
    op.drop_column('posts', 'author_id')
    # ### end Alembic commands ###
