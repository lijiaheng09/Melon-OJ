"""add permission control for problems

Revision ID: 24f8d6201f93
Revises: 572027cd0f1a
Create Date: 2023-05-24 18:50:26.057088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24f8d6201f93'
down_revision = '572027cd0f1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('problem_manager',
    sa.Column('problem_id', sa.Integer(), nullable=False),
    sa.Column('manager_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['manager_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['problem_id'], ['problem.id'], ),
    sa.PrimaryKeyConstraint('problem_id', 'manager_id')
    )
    with op.batch_alter_table('problem', schema=None) as batch_op:
        batch_op.add_column(sa.Column('visibility', sa.Enum('Private', 'Public'), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('problem', schema=None) as batch_op:
        batch_op.drop_column('visibility')

    op.drop_table('problem_manager')
    # ### end Alembic commands ###