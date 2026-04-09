from . import db


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), nullable=False, default="open")
    options = db.Column(db.Text, nullable=True)

    topic = db.relationship("Topic", backref=db.backref("questions", lazy=True))

    def __repr__(self):
        return f"<Question {self.id}>"