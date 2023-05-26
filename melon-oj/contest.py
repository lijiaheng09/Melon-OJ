import datetime
import functools
from flask import (
    Blueprint,
    request,
    g,
    render_template,
    redirect,
    abort,
    flash,
    url_for,
)
import sqlalchemy as sa
import sqlalchemy.exc
from .db import db, Contest, ContestManager, ContestProblem, User, Problem
from . import auth
from . import problem

bp = Blueprint("contest", __name__, url_prefix="/contest")


def is_manager(contest_id: int):
    return (
        g.user is not None
        and db.session.execute(
            sa.select(ContestManager)
            .where(
                (ContestManager.contest_id == contest_id)
                & (ContestManager.manager_id == g.user.id)
            )
            .exists()
            .select()
        ).scalar_one()
    )


def manager_required(view):
    @auth.login_required
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not is_manager(kwargs["contest_id"]):
            abort(403)
        return view(**kwargs)

    return wrapped_view


@bp.route("/list")
def ls():
    now = datetime.datetime.now()
    running_contests = db.session.execute(
        sa.select(Contest)
        .where((Contest.start_time <= now) & (now < Contest.end_time))
        .order_by(Contest.end_time.asc())
    ).scalars()
    my_contests = (
        db.session.execute(
            sa.select(Contest)
            .select_from(Contest, ContestManager)
            .where(
                (Contest.id == ContestManager.contest_id)
                & (ContestManager.manager_id == g.user.id)
            )
        ).scalars()
        if g.user
        else None
    )
    upcoming_contests = db.session.execute(
        sa.select(Contest)
        .where(now < Contest.start_time)
        .order_by(Contest.start_time.asc())
    ).scalars()
    ended_contests = db.session.execute(
        sa.select(Contest)
        .where(Contest.end_time <= now)
        .order_by(Contest.start_time.desc())
    ).scalars()
    return render_template(
        "contest/list.html",
        running_contests=running_contests,
        my_contests=my_contests,
        upcoming_contests=upcoming_contests,
        ended_contests=ended_contests,
    )


@bp.route("/show/<int:contest_id>")
def show(contest_id: int):
    c = db.session.execute(
        sa.select(Contest).where(Contest.id == contest_id)
    ).scalar_one()
    problems = None
    if (c.start_time is not None and c.start_time <= datetime.datetime.now()) or is_manager(contest_id):
        problems = db.session.execute(
            sa.select(ContestProblem.idx, Problem.title)
            .select_from(
                sa.outerjoin(
                    ContestProblem, Problem, ContestProblem.problem_id == Problem.id
                )
            )
            .where(ContestProblem.contest_id == contest_id)
        )
    return render_template(
        "contest/show.html", c=c, is_manager=is_manager(contest_id), problems=problems
    )


@bp.route("/show_problem/<int:contest_id>/<int:idx>")
def show_problem(contest_id: int, idx: int):
    start_time = db.session.execute(
        sa.select(Contest.start_time)
        .select_from(Contest)
        .where(Contest.id == contest_id)
    ).scalar_one()
    if not (start_time <= datetime.datetime.now()) and not is_manager(contest_id):
        abort(403)
    problem_id = db.session.execute(
        sa.select(ContestProblem.problem_id)
        .select_from(ContestProblem)
        .where((ContestProblem.contest_id == contest_id) & (ContestProblem.idx == idx))
    ).scalar_one()
    return problem.show(problem_id=problem_id, contest_id=contest_id, idx=idx)


@bp.route("/edit/<int:contest_id>", methods=["GET", "POST"])
@manager_required
def edit(contest_id: int):
    if request.method == "GET":
        c = db.session.execute(
            sa.select(Contest).where(Contest.id == contest_id)
        ).scalar_one()
        problems = db.session.execute(
            sa.select(
                ContestProblem.idx,
                ContestProblem.score,
                ContestProblem.problem_id,
                Problem.title,
            )
            .select_from(
                sa.outerjoin(
                    ContestProblem, Problem, ContestProblem.problem_id == Problem.id
                )
            )
            .where(ContestProblem.contest_id == contest_id)
        ).all()
        managers = db.session.execute(
            sa.select(User)
            .select_from(User, ContestManager)
            .where(
                (ContestManager.contest_id == contest_id)
                & (User.id == ContestManager.manager_id)
            )
        ).scalars()
        return render_template(
            "contest/edit.html", c=c, problems=problems, managers=managers
        )
    db.session.execute(
        sa.update(Contest)
        .where(Contest.id == contest_id)
        .values(
            title=request.form["title"],
            start_time=request.form["start_time"] or None,
            end_time=request.form["end_time"] or None,
        )
    )
    db.session.commit()
    return redirect(request.referrer or url_for("contest.edit", contest_id=contest_id))


@bp.route("/edit_problem/<int:contest_id>/<int:idx>", methods=["POST"])
@manager_required
def edit_problem(contest_id: int, idx: int):
    try:
        score = float(request.form["score"]) if request.form["score"] else None
        ok = True
        if request.form["problem_id"]:
            problem_id = int(request.form["problem_id"])
            visbility = db.session.execute(
                sa.select(Problem.visibility).where(
                    Problem.id == request.form["problem_id"]
                )
            ).scalar_one()
            if visbility != "Public" and not problem.is_manager(problem_id):
                flash("No access to the problem.")
                ok = False
        if ok:
            db.session.execute(
                sa.update(ContestProblem)
                .where(
                    (ContestProblem.contest_id == contest_id)
                    & (ContestProblem.idx == idx)
                )
                .values(
                    problem_id=request.form["problem_id"] or None,
                    score=score,
                )
            )
            db.session.commit()
    except ValueError:
        flash("Invalid problem ID or score.")
    except sqlalchemy.exc.NoResultFound:
        flash("No such problem.")
    return redirect(request.referrer or url_for("contest.edit", contest_id=contest_id))


@bp.route("/add_problem/<int:contest_id>", methods=["POST"])
@manager_required
def add_problem(contest_id: int):
    idx = db.session.execute(
        sa.select(sa.func.count() + 1)
        .select_from(ContestProblem)
        .where(ContestProblem.contest_id == contest_id)
    ).scalar_one()
    db.session.execute(sa.insert(ContestProblem).values(contest_id=contest_id, idx=idx))
    db.session.commit()
    return redirect(request.referrer or url_for("contest.edit", contest_id=contest_id))


@bp.route("/remove_problem/<int:contest_id>", methods=["POST"])
@manager_required
def remove_problem(contest_id: int):
    db.session.delete(
        db.session.execute(
            sa.select(ContestProblem)
            .where(ContestProblem.contest_id == contest_id)
            .order_by(ContestProblem.idx.desc())
            .limit(1)
        ).scalar_one()
    )
    db.session.commit()
    return redirect(request.referrer or url_for("contest.edit", contest_id=contest_id))


@bp.route("/drop_managers/<int:contest_id>", methods=["POST"])
@manager_required
def drop_managers(contest_id: int):
    if g.user.id in request.values.keys():
        abort(400)
    db.session.execute(
        sa.delete(ContestManager).where(
            (ContestManager.contest_id == contest_id)
            & (ContestManager.manager_id.in_(request.values.keys()))
        )
    )
    db.session.commit()
    return redirect(request.referrer or url_for("contest.edit", contest_id=contest_id))


@bp.route("/add_manager/<int:contest_id>", methods=["POST"])
@manager_required
def add_manager(contest_id: int):
    try:
        manager_id = db.session.execute(
            sa.select(User.id).where(User.name == request.values["manager"])
        ).scalar_one()
        db.session.add(ContestManager(contest_id=contest_id, manager_id=manager_id))
        db.session.commit()
    except sqlalchemy.exc.NoResultFound:
        flash("No such user.")
    except sqlalchemy.exc.IntegrityError:
        flash("Duplicate manager.")
    return redirect(request.referrer or url_for("contest.edit", contest_id=contest_id))


@bp.route("/create")
@auth.login_required
def create():
    c = Contest(title="New Contest")
    db.session.add(c)
    db.session.flush()
    db.session.add(ContestManager(contest_id=c.id, manager_id=g.user.id))
    db.session.commit()
    return redirect(url_for("contest.show", contest_id=c.id))
