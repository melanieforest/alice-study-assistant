from . import db

class AnswerAttempt(db.Model):
    __tablename__ = "answer_attempts"

    id = db.Column(db.Integer, primary_key=True)
    alice_user_id = db.Column(db.String(128))
    question_id = db.Column(db.Integer)
    user_answer = db.Column(db.String(255))
    is_correct = db.Column(db.Boolean)
