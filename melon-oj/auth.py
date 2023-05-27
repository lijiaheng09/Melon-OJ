import functools
from flask import (
    Blueprint,
    request,
    g,
    session,
    render_template,
    redirect,
    url_for,
    flash,
)
from .db import db, User
import sqlalchemy as sa
import sqlalchemy.exc

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if g.user is not None:
        return redirect(url_for("index"))
    if request.method == "GET":
        return render_template("auth/register.html")
    username = request.form["username"]
    password = request.form["password"]
    if db.session.execute(
        sa.select(User).where(User.name == username).exists().select()
    ).scalar_one():
        flash("Username already exists.")
        return redirect(url_for("auth.register"))
    user = User(name=username, password=password)
    try:
        db.session.add(user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        flash("Username already exists.")
        return redirect(url_for("auth.register"))
    flash("Successfully registered.")
    return redirect(url_for("auth.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if g.user is not None:
        return redirect(url_for("index"))
    if request.method == "GET":
        return render_template("auth/login.html")
    username = request.form["username"]
    password = request.form["password"]
    try:
        user: User = db.session.execute(
            sa.select(User).where(User.name == username)
        ).scalar_one()
        if user.check_password(password):
            session["user_id"] = user.id
            return redirect(request.referrer or url_for("index"))
        flash("Incorrect password.")
    except sqlalchemy.exc.NoResultFound:
        flash("Username does not exist.")
    return redirect(url_for("auth.login"))


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.execute(
            sa.select(User).where(User.id == user_id)
        ).scalar_one()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view
