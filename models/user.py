from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    alice_user_id = db.Column(db.String(128), unique=True, nullable=True)
    username = db.Column(db.String(64), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<User {self.id}>"