from flask import Blueprint, render_template

bp = Blueprint("problem", __name__, url_prefix="/problem")


@bp.route("/list")
def ls():
    return render_template("problem/list.html", probs=[{}, {}])
