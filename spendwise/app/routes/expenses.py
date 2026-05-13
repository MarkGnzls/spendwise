from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.expense import Expense

expenses_bp = Blueprint("expenses", __name__, template_folder="../templates")

CATEGORIES = ["Food", "Transportation", "Bills", "Shopping", "School", "Entertainment", "Others"]


@expenses_bp.route("/expenses", methods=["GET", "POST"])
@login_required
def expenses():
    if request.method == "POST":
        category = request.form.get("category", "Others")
        amount = request.form.get("amount", "0").strip()
        description = request.form.get("description", "").strip()
        date_created = request.form.get("date_created")

        if not amount or float(amount) <= 0:
            flash("Enter a valid amount for the expense.", "danger")
            return redirect(url_for("expenses.expenses"))

        new_expense = Expense(
            user_id=current_user.id,
            category=category,
            amount=round(float(amount), 2),
            description=description,
            date_created=datetime.strptime(date_created, "%Y-%m-%d").date() if date_created else datetime.utcnow().date(),
        )
        db.session.add(new_expense)
        db.session.commit()
        flash("Expense added successfully.", "success")
        return redirect(url_for("expenses.expenses"))

    user_expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date_created.desc()).all()
    return render_template("expenses.html", expenses=user_expenses, categories=CATEGORIES)


@expenses_bp.route("/expenses/edit/<int:item_id>", methods=["GET", "POST"])
@login_required
def edit_expense(item_id):
    expense = Expense.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()

    if request.method == "POST":
        category = request.form.get("category", expense.category)
        amount = request.form.get("amount", "0").strip()
        description = request.form.get("description", "").strip()
        date_created = request.form.get("date_created")

        if not amount or float(amount) <= 0:
            flash("Enter a valid amount.", "danger")
            return redirect(url_for("expenses.edit_expense", item_id=item_id))

        expense.category = category
        expense.amount = round(float(amount), 2)
        expense.description = description
        expense.date_created = datetime.strptime(date_created, "%Y-%m-%d").date() if date_created else expense.date_created
        db.session.commit()
        flash("Expense updated.", "success")
        return redirect(url_for("expenses.expenses"))

    return render_template("expense_form.html", expense=expense, categories=CATEGORIES)


@expenses_bp.route("/expenses/delete/<int:item_id>", methods=["POST"])
@login_required
def delete_expense(item_id):
    expense = Expense.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    db.session.delete(expense)
    db.session.commit()
    flash("Expense removed.", "info")
    return redirect(url_for("expenses.expenses"))
