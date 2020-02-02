"""picture dimensions

Revision ID: d686b9575b6f
Revises: 6c1c48e21056
Create Date: 2020-02-02 00:34:42.933509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd686b9575b6f'
down_revision = '6c1c48e21056'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('picture', sa.Column('height', sa.Integer(), nullable=True))
    op.add_column('picture', sa.Column('width', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('picture', 'width')
    op.drop_column('picture', 'height')
    # ### end Alembic commands ###
