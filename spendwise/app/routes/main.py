from datetime import datetime
from collections import defaultdict
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.expense import Expense
from app.models.income import Income

main_bp = Blueprint("main", __name__, template_folder="../templates")


@main_bp.route("/")
@login_required
def dashboard():
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date_created.desc()).limit(8).all()
    incomes = Income.query.filter_by(user_id=current_user.id).order_by(Income.date_created.desc()).limit(8).all()

    total_expense = sum([float(item.amount) for item in Expense.query.filter_by(user_id=current_user.id).all()])
    total_income = sum([float(item.amount) for item in Income.query.filter_by(user_id=current_user.id).all()])
    total_balance = total_income - total_expense

    category_totals = defaultdict(float)
    for item in Expense.query.filter_by(user_id=current_user.id).all():
        category_totals[item.category] += float(item.amount)

    monthly_totals = defaultdict(float)
    for item in Expense.query.filter_by(user_id=current_user.id).all():
        month = item.date_created.strftime("%b %Y")
        monthly_totals[month] += float(item.amount)

    monthly_income = defaultdict(float)
    for item in Income.query.filter_by(user_id=current_user.id).all():
        month = item.date_created.strftime("%b %Y")
        monthly_income[month] += float(item.amount)

    months = sorted({*monthly_totals.keys(), *monthly_income.keys()}, key=lambda m: datetime.strptime(m, "%b %Y"))
    expense_series = [monthly_totals.get(month, 0) for month in months]
    income_series = [monthly_income.get(month, 0) for month in months]

    return render_template(
        "dashboard.html",
        total_balance=total_balance,
        total_income=total_income,
        total_expense=total_expense,
        recent_expenses=expenses,
        recent_incomes=incomes,
        category_labels=list(category_totals.keys()) or ["No Data"],
        category_values=list(category_totals.values()) or [0],
        month_labels=months or [],
        month_expenses=expense_series,
        month_incomes=income_series,
    )
