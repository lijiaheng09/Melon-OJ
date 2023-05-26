import datetime
from flask import Blueprint, request, render_template, redirect, url_for
import sqlalchemy as sa
from .db import db, Contest

bp = Blueprint("contest", __name__, url_prefix="/contest")


@bp.route("/list")
def ls():
    now = datetime.datetime.now()
    running_contests = db.session.execute(
        sa.select(Contest)
        .where((Contest.start_time <= now) & (now < Contest.end_time))
        .order_by(Contest.end_time.asc())
    ).scalars()
    upcoming_contests = db.session.execute(
        sa.select(Contest)
        .where(
            (now < Contest.start_time)
            | Contest.start_time.is_(None)
            | Contest.end_time.is_(None)
        )
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
        upcoming_contests=upcoming_contests,
        ended_contests=ended_contests,
    )


@bp.route("/show/<int:contest_id>")
def show(contest_id: int):
    c = db.session.execute(
        sa.select(Contest).where(Contest.id == contest_id)
    ).scalar_one()
    return render_template("contest/show.html", c=c)


@bp.route("/edit/<int:contest_id>", methods=["GET", "POST"])
def edit(contest_id: int):
    c = db.session.execute(
        sa.select(Contest).where(Contest.id == contest_id)
    ).scalar_one()
    if request.method == "GET":
        return render_template("contest/edit.html", c=c)
    c.title = request.form["title"]
    c.start_time = request.form["start_time"] or None
    c.end_time = request.form["end_time"] or None
    db.session.commit()
    print(request.form)
    return redirect(request.referrer or url_for("contest.edit", contest_id=contest_id))


@bp.route("/create")
def create():
    c = Contest(title="New Contest")
    db.session.add(c)
    db.session.commit()
    return redirect(url_for("contest.show", contest_id=c.id))
