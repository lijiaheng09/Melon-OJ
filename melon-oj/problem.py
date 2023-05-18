from flask import Blueprint, render_template
from .db import db, Problem

bp = Blueprint("problem", __name__, url_prefix="/problem")


@bp.route("/list")
def ls():
    probs = db.session.execute(db.select(Problem)).scalars()
    return render_template("problem/list.html", probs=probs)
