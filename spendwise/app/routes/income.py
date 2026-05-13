from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.income import Income

income_bp = Blueprint("income", __name__, template_folder="../templates")


@income_bp.route("/income", methods=["GET", "POST"])
@login_required
def income():
    if request.method == "POST":
        source = request.form.get("source", "Salary").strip()
        amount = request.form.get("amount", "0").strip()
        description = request.form.get("description", "").strip()
        date_created = request.form.get("date_created")

        if not amount or float(amount) <= 0:
            flash("Enter a valid income amount.", "danger")
            return redirect(url_for("income.income"))

        new_income = Income(
            user_id=current_user.id,
            source=source,
            amount=round(float(amount), 2),
            description=description,
            date_created=datetime.strptime(date_created, "%Y-%m-%d").date() if date_created else datetime.utcnow().date(),
        )
        db.session.add(new_income)
        db.session.commit()
        flash("Income recorded successfully.", "success")
        return redirect(url_for("income.income"))

    user_incomes = Income.query.filter_by(user_id=current_user.id).order_by(Income.date_created.desc()).all()
    total_income = sum([float(item.amount) for item in user_incomes])
    return render_template("income.html", incomes=user_incomes, total_income=total_income)


@income_bp.route("/income/edit/<int:item_id>", methods=["GET", "POST"])
@login_required
def edit_income(item_id):
    income_item = Income.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()

    if request.method == "POST":
        source = request.form.get("source", income_item.source).strip()
        amount = request.form.get("amount", "0").strip()
        description = request.form.get("description", "").strip()
        date_created = request.form.get("date_created")

        if not amount or float(amount) <= 0:
            flash("Enter a valid amount.", "danger")
            return redirect(url_for("income.edit_income", item_id=item_id))

        income_item.source = source
        income_item.amount = round(float(amount), 2)
        income_item.description = description
        income_item.date_created = datetime.strptime(date_created, "%Y-%m-%d").date() if date_created else income_item.date_created
        db.session.commit()
        flash("Income updated.", "success")
        return redirect(url_for("income.income"))

    return render_template("income_form.html", income=income_item)


@income_bp.route("/income/delete/<int:item_id>", methods=["POST"])
@login_required
def delete_income(item_id):
    income_item = Income.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    db.session.delete(income_item)
    db.session.commit()
    flash("Income entry removed.", "info")
    return redirect(url_for("income.income"))
