"""empty message

Revision ID: 183abaaa9035
Revises: f60915773f56
Create Date: 2019-05-30 14:34:38.304841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '183abaaa9035'
down_revision = 'f60915773f56'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=25), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tag_name'), 'tag', ['name'], unique=True)
    op.create_table('bookmark_tag',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('bookmark_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bookmark_id'], ['bookmark.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bookmark_tag')
    op.drop_index(op.f('ix_tag_name'), table_name='tag')
    op.drop_table('tag')
    # ### end Alembic commands ###