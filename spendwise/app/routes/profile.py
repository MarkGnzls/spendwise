from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.user import User

profile_bp = Blueprint("profile", __name__, template_folder="../templates")


@profile_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")

        if not username or not email:
            flash("Username and email are required.", "danger")
            return redirect(url_for("profile.profile"))

        existing_username = User.query.filter(User.username == username, User.id != current_user.id).first()
        existing_email = User.query.filter(User.email == email, User.id != current_user.id).first()
        if existing_username:
            flash("Username is already taken.", "warning")
            return redirect(url_for("profile.profile"))
        if existing_email:
            flash("Email is already in use.", "warning")
            return redirect(url_for("profile.profile"))

        current_user.username = username
        current_user.email = email

        if password:
            if password != confirm:
                flash("Passwords do not match.", "danger")
                return redirect(url_for("profile.profile"))
            current_user.set_password(password)
            flash("Password updated.", "success")

        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("profile.profile"))

    return render_template("profile.html")
