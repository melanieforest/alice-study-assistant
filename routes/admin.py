from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from models import db, User, Question, Topic

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.admin_dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = User.query.filter_by(username=username, is_admin=True).first()

        if user and user.password == password:
            login_user(user)
            flash("Вход выполнен успешно.", "success")
            return redirect(url_for("admin.admin_dashboard"))

        flash("Неверный логин или пароль.", "danger")

    return render_template("login.html")

@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из системы.", "info")
    return redirect(url_for("admin.login"))

@admin_bp.route("/admin")
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash("Доступ запрещён.", "danger")
        return redirect(url_for("admin.login"))

    return render_template("dashboard.html", user=current_user)

@admin_bp.route("/admin/questions")
@login_required
def questions_list():
    if not current_user.is_admin:
        flash("Доступ запрещён.", "danger")
        return redirect(url_for("admin.login"))

    questions = Question.query.order_by(Question.id.asc()).all()
    return render_template("questions.html", questions=questions)

@admin_bp.route("/admin/upload", methods=["GET", "POST"])
@login_required
def upload_questions():
    if not current_user.is_admin:
        flash("Доступ запрещён.", "danger")
        return redirect(url_for("admin.login"))

    if request.method == "POST":
        file = request.files.get("json_file")

        if not file or file.filename == "":
            flash("Файл не выбран.", "warning")
            return redirect(url_for("admin.upload_questions"))

        if not file.filename.endswith(".json"):
            flash("Нужен файл формата JSON.", "danger")
            return redirect(url_for("admin.upload_questions"))

        try:
            data = json.load(file)

            if not isinstance(data, list):
                flash("JSON должен содержать список объектов.", "danger")
                return redirect(url_for("admin.upload_questions"))

            added_count = 0

            for item in data:
                topic_title = item.get("topic", "Python").strip()
                text = item.get("text", "").strip()
                correct_answer = item.get("correct_answer", "").strip()
                question_type = item.get("question_type", "open").strip()
                options = item.get("options")

                if not text or not correct_answer:
                    continue

                topic = Topic.query.filter_by(title=topic_title).first()
                if not topic:
                    topic = Topic(title=topic_title, description=f"Тема {topic_title}")
                    db.session.add(topic)

                db.session.commit()

                question = Question(
                    topic_id=topic.id,
                    text=text,
                    correct_answer=correct_answer,
                    question_type=question_type,
                    options=json.dumps(options, ensure_ascii=False) if options else None


)
                db.session.add(question)
                added_count += 1

            db.session.commit()
            flash(f"Успешно загружено вопросов: {added_count}", "success")
            return redirect(url_for("admin.questions_list"))

        except Exception as e:
            flash(f"Ошибка при загрузке JSON: {e}", "danger")
            return redirect(url_for("admin.upload_questions"))

    return render_template("upload.html")