from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User, Question, Topic
from routes import webhook_bp, admin_bp

login_manager = LoginManager()
login_manager.login_view = "admin.login"
login_manager.login_message = "Сначала войдите в систему."
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_default_admin():
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(
            username="admin",
            password="1234",
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()

def create_demo_data():
    topic = Topic.query.filter_by(title="Python").first()
    if not topic:
        topic = Topic(
            title="Python",
            description="Базовые темы Python"
        )
        db.session.add(topic)
        db.session.commit()

    if Question.query.count() == 0:
        questions = [
            Question(
                topic_id=topic.id,
                text="Как в Python называется структура для хранения набора элементов в квадратных скобках?",
                correct_answer="список",
                question_type="open"
            ),
            Question(
                topic_id=topic.id,
                text="Какая функция используется для вывода текста на экран?",
                correct_answer="print",
                question_type="open"
            ),
            Question(
                topic_id=topic.id,
                text="Какой цикл используется для перебора элементов последовательности?",
                correct_answer="for",
                question_type="open"
            ),
        ]
        db.session.add_all(questions)
        db.session.commit()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(webhook_bp)
    app.register_blueprint(admin_bp)

    @app.route("/")
    def home():
        return "Flask-приложение работает."

    with app.app_context():
        db.create_all()
        create_default_admin()
        create_demo_data()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)