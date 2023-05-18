from flask import Flask, url_for, redirect


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")

    from . import db

    db.db.init_app(app)
    with app.app_context():
        db.db.create_all()

    from . import problem

    app.register_blueprint(problem.bp)

    @app.route("/")
    def index():
        return redirect(url_for("problem.ls"))

    return app
