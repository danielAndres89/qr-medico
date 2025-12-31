from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.models import Usuario
from app.extensions import db, bcrypt

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Usuario.query.filter_by(username=request.form["username"]).first()
        if user and bcrypt.check_password_hash(user.password_hash, request.form["password"]):
            login_user(user)
            return redirect(url_for("personas.listar"))
        flash("Credenciales incorrectas")
    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
