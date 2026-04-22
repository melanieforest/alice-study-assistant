from . import db

class Topic(db.Model):
    __tablename__ = "topics"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
