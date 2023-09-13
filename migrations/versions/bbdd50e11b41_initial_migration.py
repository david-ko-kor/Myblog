"""Initial migration

Revision ID: bbdd50e11b41
Revises: 
Create Date: 2023-09-10 22:50:00.016092

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbdd50e11b41'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('photo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('url', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('photo', schema=None) as batch_op:
        batch_op.drop_column('url')

    # ### end Alembic commands ###
