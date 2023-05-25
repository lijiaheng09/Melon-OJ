"""add Submission details

Revision ID: f576ba072ef4
Revises: 24f8d6201f93
Create Date: 2023-05-25 16:13:03.035381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f576ba072ef4'
down_revision = '24f8d6201f93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('submission', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('verdict', sa.Enum('Waiting', 'Judging', 'Accepted', 'Wrong Answer'), nullable=False))
        batch_op.add_column(sa.Column('score', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('submission', schema=None) as batch_op:
        batch_op.drop_column('score')
        batch_op.drop_column('verdict')
        batch_op.drop_column('time')

    # ### end Alembic commands ###