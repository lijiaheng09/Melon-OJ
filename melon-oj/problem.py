import datetime
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
from . import auth
import sqlalchemy.exc

bp = Blueprint("problem", __name__, url_prefix="/problem")


@bp.route("/list")
def ls():
    user_id = g.user.id if g.user is not None else None
    my_probs = db.select(ProblemManager.problem_id).where(
        ProblemManager.manager_id == user_id
    )
    probs = db.session.execute(
        db.select(Problem).where(
            (Problem.visibility == "Public") | Problem.id.in_(my_probs)
        )
    ).scalars()
    return render_template("problem/list.html", probs=probs)


def is_manager(problem_id: int):
    return (
        g.user is not None
        and db.session.execute(
            db.select(ProblemManager)
            .where(
                (ProblemManager.problem_id == problem_id)
                & (ProblemManager.manager_id == g.user.id)
            )
            .exists()
            .select()
        ).scalar_one()
    )


def manager_required(view):
    @auth.login_required
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not is_manager(kwargs["problem_id"]):
            abort(403)
        return view(**kwargs)

    return wrapped_view


@bp.route("/show/<int:problem_id>")
def show(problem_id: int):
    p = db.session.execute(
        db.select(Problem).where(Problem.id == problem_id)
    ).scalar_one()
    return render_template("problem/show.html", p=p, is_manager=is_manager(problem_id))


@bp.route("/create")
@auth.login_required
def create():
    p = Problem(title="New Problem", statement="")
    db.session.add(p)
    db.session.commit()
    db.session.add(ProblemManager(problem_id=p.id, manager_id=g.user.id))
    db.session.commit()
    return redirect(url_for("problem.edit", problem_id=p.id))


@bp.route("/edit/<int:problem_id>", methods=["GET", "POST"])
@manager_required
def edit(problem_id: int):
    p = db.session.execute(
        db.select(Problem).where(Problem.id == problem_id)
    ).scalar_one()
    if request.method == "GET":
        managers = db.session.execute(
            db.select(User)
            .select_from(User, ProblemManager)
            .where(
                (ProblemManager.problem_id == problem_id)
                & (User.id == ProblemManager.manager_id)
            )
        ).scalars()
        return render_template("problem/edit.html", p=p, managers=managers)
    p.title = request.values["title"]
    p.statement = request.values["statement"]
    p.visibility = request.values["visibility"]
    db.session.commit()
    return redirect(request.referrer or url_for("problem.edit", problem_id=problem_id))


@bp.route("/drop_managers/<int:problem_id>", methods=["POST"])
@manager_required
def drop_managers(problem_id: int):
    if g.user.id in request.values.keys():
        abort(400)
    db.session.execute(
        db.delete(ProblemManager).where(
            (ProblemManager.problem_id == problem_id)
            & (ProblemManager.manager_id.in_(request.values.keys()))
        )
    )
    db.session.commit()
    return redirect(request.referrer or url_for("problem.edit", problem_id=problem_id))


@bp.route("/add_manager/<int:problem_id>", methods=["POST"])
@manager_required
def add_manager(problem_id: int):
    try:
        manager_id = db.session.execute(
            db.select(User.id).where(User.name == request.values["manager"])
        ).scalar_one()
        db.session.add(ProblemManager(problem_id=problem_id, manager_id=manager_id))
        db.session.commit()
    except sqlalchemy.exc.NoResultFound:
        flash("No such user.")
    except sqlalchemy.exc.IntegrityError:
        flash("Duplicate manager.")
    return redirect(request.referrer or url_for("problem.edit", problem_id=problem_id))


@bp.route("/submit/<int:problem_id>", methods=["POST"])
@auth.login_required
def submit(problem_id: int):
    sub = Submission(
        problem_id=problem_id, user_id=g.user.id, answer=request.values["answer"],
        time=datetime.datetime.now()
    )
    db.session.add(sub)
    db.session.commit()
    return redirect(url_for("submission.show", submission_id=sub.id))
