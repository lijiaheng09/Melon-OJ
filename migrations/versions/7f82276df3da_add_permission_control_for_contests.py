"""add permission control for contests

Revision ID: 7f82276df3da
Revises: 28e7cd6e5030
Create Date: 2023-05-26 16:13:22.940393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f82276df3da'
down_revision = '28e7cd6e5030'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contest_manager',
    sa.Column('contest_id', sa.Integer(), nullable=False),
    sa.Column('manager_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['contest_id'], ['contest.id'], ),
    sa.ForeignKeyConstraint(['manager_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('contest_id', 'manager_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contest_manager')
    # ### end Alembic commands ###
