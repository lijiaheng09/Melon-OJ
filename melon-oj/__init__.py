from flask import Flask, url_for, redirect
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")

    from .db import db

    db.init_app(app)
    migrate = Migrate(app, db)

    from . import auth
    from . import problem
    from . import user
    from . import submission
    from . import contest
    from . import jury

    app.register_blueprint(auth.bp)
    app.register_blueprint(problem.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(submission.bp)
    app.register_blueprint(contest.bp)
    app.register_blueprint(jury.bp)

    @app.route("/")
    def index():
        return redirect(url_for("problem.ls"))

    return app
