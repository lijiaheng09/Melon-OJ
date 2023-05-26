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

bp = Blueprint("jury", __name__, url_prefix="/jury")


@bp.route("/list")
def ls():
    user_id = g.user.id if g.user is not None else None
    user_probs = sa.select(ProblemManager.problem_id).where(
        ProblemManager.manager_id == user_id
    )
    submissions = db.session.execute(
        sa.select(
            Submission.id,
            Submission.problem_id, Problem.title,
            Submission.user_id, User.name,
            Submission.verdict, Submission.score, Submission.time
        ).select_from(Submission, Problem, User).where(
            (Submission.problem_id == Problem.id)
            & (Submission.user_id == User.id)
            & (Problem.id.in_(user_probs))
            & (Submission.verdict == "Waiting")
        ).order_by(Submission.id.asc())
    )
    return render_template("jury/list.html", submissions=submissions)

