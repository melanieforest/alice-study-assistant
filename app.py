from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User
from routes import webhook_bp, admin_bp


login_manager = LoginManager()
login_manager.login_view = "admin.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_default_admin():
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(username="admin", password="1234", is_admin=True)
        db.session.add(admin)
        db.session.commit()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(webhook_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        create_default_admin()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)