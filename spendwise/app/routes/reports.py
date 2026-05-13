from collections import defaultdict
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.expense import Expense
from app.models.income import Income

reports_bp = Blueprint("reports", __name__, template_folder="../templates")


@reports_bp.route("/reports")
@login_required
def reports():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    incomes = Income.query.filter_by(user_id=current_user.id).all()

    category_totals = defaultdict(float)
    for item in expenses:
        category_totals[item.category] += float(item.amount)

    source_totals = defaultdict(float)
    for item in incomes:
        source_totals[item.source] += float(item.amount)

    monthly_expense = defaultdict(float)
    monthly_income = defaultdict(float)
    for item in expenses:
        month = item.date_created.strftime("%b %Y")
        monthly_expense[month] += float(item.amount)
    for item in incomes:
        month = item.date_created.strftime("%b %Y")
        monthly_income[month] += float(item.amount)

    months = sorted({*monthly_expense.keys(), *monthly_income.keys()})
    expense_series = [monthly_expense.get(m, 0) for m in months]
    income_series = [monthly_income.get(m, 0) for m in months]

    return render_template(
        "reports.html",
        category_labels=list(category_totals.keys()) or ["No Data"],
        category_values=list(category_totals.values()) or [0],
        source_labels=list(source_totals.keys()) or ["No Data"],
        source_values=list(source_totals.values()) or [0],
        month_labels=months,
        month_expenses=expense_series,
        month_incomes=income_series,
    )
