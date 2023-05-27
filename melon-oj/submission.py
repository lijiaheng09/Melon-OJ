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
from . import problem
import sqlalchemy.exc
import sqlalchemy as sa

bp = Blueprint("submission", __name__, url_prefix="/submission")


@bp.route("/list")
def ls():
    my_user_id = g.user.id if g.user is not None else None
    my_probs = sa.select(Problem.id).where(
        (Problem.visibility == "Public") | Problem.id.in_(
            sa.select(ProblemManager.problem_id).where(
                ProblemManager.manager_id == my_user_id
            )
        )
    )
    pred = (Submission.problem_id == Problem.id) & (Submission.user_id == User.id) & (Problem.id.in_(my_probs))
    search_problem = request.args.get("problem", "")
    if search_problem:
        pred &= (Problem.id == search_problem) # | Problem.title.like(f"%{search_problem}%")
    search_user = request.args.get("user", "")
    if search_user:
        pred &= (User.name == search_user) # | User.name.like(f"%{search_user}%")
    search_verdict = request.args.get("verdict", "")
    if search_verdict:
        pred &= (Submission.verdict == search_verdict)
    submissions = db.session.execute(
        sa.select(
            Submission.id,
            Submission.problem_id, Problem.title,
            Submission.user_id, User.name,
            Submission.verdict, Submission.score, Submission.time
        ).select_from(Submission, Problem, User).where(
            pred
        ).order_by(Submission.id.desc())
    )
    return render_template("submission/list.html", submissions=submissions)


@bp.route("/show/<int:submission_id>")
def show(submission_id: int, contest_info=None):
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
    p = db.session.execute(
        sa.select(Problem).where(Problem.id == s.problem_id)
    ).scalar_one()
    if contest_info is None and p.visibility != "Public" and not problem.is_manager(s.problem_id):
        abort(403)
    return render_template(
        "submission/show.html",
        s=s,
        is_manager=problem.is_manager(s.problem_id),
        contest_info=contest_info
    )

@bp.route("/judge/<int:submission_id>", methods=["GET", "POST"])
def judge(submission_id: int, contest_info=None):
    s = db.session.execute(
        sa.select(Submission).where(Submission.id == submission_id)
    ).scalar_one()
    if not problem.is_manager(s.problem_id):
        abort(403)
    if request.method == "GET":
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
        if not problem.is_manager(s.problem_id):
            abort(403)
        return render_template(
            "submission/judge.html",
            s=s,
            contest_info=contest_info
        )
    else:
        score=float(request.form["score"]) if request.form["score"] else None
        db.session.execute(
            sa.update(Submission)
            .where(Submission.id == submission_id)
            .values(
                score=score,
                verdict=("Accepted" if score >= 1.0 else "Wrong Answer") if score is not None else "Waiting",
            )
        )
        db.session.commit()
        return redirect(request.referrer or url_for("submission.judge", submission_id=submission_id, contest_info=contest_info))

