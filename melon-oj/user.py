from flask import Blueprint, request, g, render_template, redirect, flash, url_for
from .db import db, User, Submission
from . import auth

bp = Blueprint("user", __name__, "/user")


@bp.route("/info/<int:user_id>")
def info(user_id: int):
    user = db.session.execute(db.select(User).where(User.id == user_id)).scalar_one()
    submissions = db.session.execute(
        db.select(Submission.id, Submission.problem_id)
        .select_from(Submission)
        .where(Submission.user_id == user_id)
    )
    return render_template("user/info.html", user=user, submissions=submissions)


@bp.route("/update_info", methods=["POST"])
@auth.login_required
def update_info():
    g.user.name = request.values["username"]
    db.session.commit()
    return redirect(request.referrer or url_for("user.info", user_id=g.user.id))


@bp.route("/update_password", methods=["POST"])
@auth.login_required
def update_password():
    if not g.user.check_password(request.values["original_password"]):
        flash("Incorrect original password.")
    else:
        g.user.password = request.values["new_password"]
        db.session.commit()
    return redirect(request.referrer or url_for("user.info", user_id=g.user.id))
