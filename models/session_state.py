from . import db

class SessionState(db.Model):
    __tablename__ = "session_states"

    id = db.Column(db.Integer, primary_key=True)
    alice_user_id = db.Column(db.String(128), unique=True, nullable=False)
    mode = db.Column(db.String(50), nullable=True)
    current_topic = db.Column(db.String(255), nullable=True)
    current_question_id = db.Column(db.Integer, nullable=True)
    waiting_for_answer = db.Column(db.Boolean, default=False)
    question_index = db.Column(db.Integer, default=0)
    score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<SessionState {self.alice_user_id}>"