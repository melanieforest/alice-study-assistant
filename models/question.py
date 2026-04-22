from . import db

class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"))
    text = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)
    question_type = db.Column(db.String(50))
    options = db.Column(db.Text)
