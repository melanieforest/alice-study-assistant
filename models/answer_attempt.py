from datetime import datetime
from . import db


class AnswerAttempt(db.Model):
    __tablename__ = "answer_attempts"

    id = db.Column(db.Integer, primary_key=True)
    alice_user_id = db.Column(db.String(128), nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    user_answer = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AnswerAttempt {self.id}>"