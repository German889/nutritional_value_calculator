"""after studing

Revision ID: 74ef1f2f6fe9
Revises: 
Create Date: 2024-04-10 10:38:57.838364

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74ef1f2f6fe9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('protein', sa.Float(), nullable=False),
    sa.Column('fat', sa.Float(), nullable=False),
    sa.Column('carbohydrate', sa.Float(), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product')
    # ### end Alembic commands ###
