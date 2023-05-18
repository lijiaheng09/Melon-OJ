import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Problem(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String(128), nullable=False)
