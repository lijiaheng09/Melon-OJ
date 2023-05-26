import functools
from flask import (
    Blueprint,
    request,
    g,
    render_template,
    abort,
    flash,
    redirect,
    url_for,
)
from .db import db, Problem, User, ProblemManager, Submission
import sqlalchemy.exc
import sqlalchemy as sa
from .problem import is_manager

bp = Blueprint("submission", __name__, url_prefix="/submission")


@bp.route("/list")
def ls():
    user_id = g.user.id if g.user is not None else None
    probs = sa.select(Problem.id).where(
        (Problem.visibility == "Public") | Problem.id.in_(
            sa.select(ProblemManager.problem_id).where(
                ProblemManager.manager_id == user_id
            )
        )
    )
    submissions = db.session.execute(
        sa.select(
            Submission.id,
            Submission.problem_id, Problem.title,
            Submission.user_id, User.name,
            Submission.verdict, Submission.score, Submission.time
        ).select_from(Submission, Problem, User).where(
            (Submission.problem_id == Problem.id) & (Submission.user_id == User.id) & (Problem.id.in_(probs))
        ).order_by(Submission.id.desc())
    )
    return render_template("submission/list.html", submissions=submissions)

@bp.route("/show/<int:submission_id>")
def show(submission_id: int):
    s = db.session.execute(
        sa.select(
            Submission.id,
            Submission.problem_id, Problem.title,
            Submission.user_id, User.name,
            Submission.answer, Submission.verdict, Submission.score, Submission.time
        ).select_from(Submission, Problem, User).where(
            (Submission.id == submission_id) & (Submission.problem_id == Problem.id) & (Submission.user_id == User.id)
        )
    ).one()
    return render_template("submission/show.html", s=s, is_manager=is_manager(s.problem_id))
