"""add view HighestSubmission

Revision ID: c58b128c234f
Revises: f60012fd592f
Create Date: 2023-05-27 19:26:42.917171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c58b128c234f"
down_revision = "f60012fd592f"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
CREATE VIEW `highest_submission` AS
SELECT * FROM `submission`
WHERE `submission`.`id` = (
    SELECT `sub1`.`id`
    FROM `submission` AS `sub1`
    WHERE `submission`.`problem_id` = `sub1`.`problem_id`
        AND `submission`.`user_id` = `sub1`.`user_id`
    ORDER BY `sub1`.`score` DESC, `sub1`.`id` DESC
    LIMIT 1
)
    """
    )


def downgrade():
    op.execute("DROP VIEW `highest_submission`")
