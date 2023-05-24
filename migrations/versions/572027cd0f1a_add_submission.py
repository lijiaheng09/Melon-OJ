"""add Submission

Revision ID: 572027cd0f1a
Revises: 4acff439f3e9
Create Date: 2023-05-24 18:29:57.479504

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '572027cd0f1a'
down_revision = '4acff439f3e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('submission',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('problem_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('answer', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['problem_id'], ['problem.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('submission')
    # ### end Alembic commands ###