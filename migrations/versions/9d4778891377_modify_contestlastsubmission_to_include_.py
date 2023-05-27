"""modify ContestLastSubmission to include Submission info

Revision ID: 9d4778891377
Revises: c58b128c234f
Create Date: 2023-05-27 20:08:14.477062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9d4778891377"
down_revision = "c58b128c234f"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("DROP VIEW IF EXISTS `contest_last_submission`")
    op.execute(
        """
CREATE VIEW `contest_last_submission` AS
SELECT
    `contest_problem`.`contest_id`,
    `contest_problem`.`idx`,
    `contest_problem`.`score` AS `full_score`,
    `submission`.`id` AS `submission_id`,
    `submission`.`user_id`,
    `submission`.`time`,
    `submission`.`verdict`,
    `submission`.`score`
FROM
    `contest_problem`, `submission`, (
        SELECT `contest_id`, `idx`, MAX(`submission`.`id`) AS `submission_id`
        FROM `contest_submission`, `submission`
        WHERE `submission_id` = `submission`.`id`
        GROUP BY `contest_id`, `idx`, `user_id`
    ) AS `lastsub`
WHERE
    `contest_problem`.`contest_id` = `lastsub`.`contest_id`
    AND `contest_problem`.`idx` = `lastsub`.`idx`
    AND `submission`.`id` = `lastsub`.`submission_id`
"""
    )


def downgrade():
    op.execute("DROP VIEW IF EXISTS `contest_last_submission`")
    op.execute(
        """
CREATE VIEW `contest_last_submission` AS
SELECT `contest_id`, `idx`, `user_id`, MAX(`submission`.`id`) AS `submission_id`
FROM `contest_submission`, `submission`
WHERE `submission_id` = `submission`.`id`
GROUP BY `contest_id`, `idx`, `user_id`
"""
    )
