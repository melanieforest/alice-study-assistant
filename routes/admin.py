from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User

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