from datetime import datetime
from app import db


class Expense(db.Model):
    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    date_created = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    user = db.relationship("User", back_populates="expenses")

    def __repr__(self):
        return f"<Expense {self.category} {self.amount}>"
