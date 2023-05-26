"""add view ContestLastSubmission

Revision ID: f60012fd592f
Revises: da48dedbcf80
Create Date: 2023-05-27 03:24:54.330603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f60012fd592f"
down_revision = "da48dedbcf80"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
CREATE VIEW `contest_last_submission` AS
SELECT `contest_id`, `idx`, `user_id`, MAX(`submission`.`id`) AS `submission_id`
FROM `contest_submission`, `submission`
WHERE `submission_id` = `submission`.`id`
GROUP BY `contest_id`, `idx`, `user_id`
    """
    )
    pass


def downgrade():
    op.execute("DROP VIEW `contest_last_submission`")
    pass
