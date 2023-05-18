from flask import Flask, url_for, redirect


def create_app():
    app = Flask(__name__)

    from . import problem

    app.register_blueprint(problem.bp)

    @app.route("/")
    def index():
        return redirect(url_for("problem.ls"))

    return app
