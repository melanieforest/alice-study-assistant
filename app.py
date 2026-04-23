from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
from config import Config
from models import db, User

from routes import webhook_bp, admin_bp, api_bp


login_manager = LoginManager()
login_manager.login_view = "admin.login"
login_manager.login_message = "Сначала войдите в систему."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


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


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(webhook_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    @app.route("/")
    def home():
        if current_user.is_authenticated:
            return redirect(url_for("admin.admin_dashboard"))
        return redirect(url_for("admin.login"))

    from services.quote_service import get_quote
    import time

    cached_quote = {"data": None, "time": 0}

    @app.context_processor
    def inject_quote():
        now = time.time()

        if not cached_quote["data"] or now - cached_quote["time"] > 3600:
            cached_quote["data"] = get_quote()
            cached_quote["time"] = now

        return {
            "quote": cached_quote["data"]
        }

    with app.app_context():
        db.create_all()
        create_default_admin()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)