import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Problem(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String(128), nullable=False)


class User(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(32), unique=True)
    _password = sa.Column(sa.String(128), nullable=False)

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str):
        from werkzeug.security import generate_password_hash

        self._password = generate_password_hash(value)

    def check_password(self, value: str) -> bool:
        from werkzeug.security import check_password_hash

        return check_password_hash(self._password, value)
