from flask import Blueprint, request, g, render_template, redirect, url_for
from .db import db, Problem
from . import auth

bp = Blueprint("problem", __name__, url_prefix="/problem")


@bp.route("/list")
def ls():
    probs = db.session.execute(db.select(Problem)).scalars()
    return render_template("problem/list.html", probs=probs)


@bp.route("/show/<int:problem_id>")
def show(problem_id: int):
    p = db.session.execute(
        db.select(Problem).where(Problem.id == problem_id)
    ).scalar_one()
    return render_template("problem/show.html", p=p)


@bp.route("/create")
def create():
    p = Problem(title="New Problem", statement="")
    db.session.add(p)
    db.session.commit()
    return redirect(url_for("problem.edit", problem_id=p.id))

@bp.route("/edit/<int:problem_id>", methods=["GET", "POST"])
def edit(problem_id: int):
    p = db.session.execute(
        db.select(Problem).where(Problem.id == problem_id)
    ).scalar_one()
    if request.method == "GET":
        return render_template("problem/edit.html", p=p)
    p.title = request.values["title"]
    p.statement = request.values["statement"]
    db.session.commit()
    return redirect(request.referrer or url_for("problem.edit", problem_id=problem_id))


@bp.route("/submit/<int:problem_id>", methods=["POST"])
@auth.login_required
def submit(problem_id: int):
    return {
        "user_id": g.user.id,
        "problem_id": problem_id,
        "answer": request.values["answer"],
    }
