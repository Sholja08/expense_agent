import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime


# Path to expense_data.json
DATA_FILE = (
    Path(__file__).resolve().parent.parent / "data" / "expense_data.json"
)


def load_expenses():
    """Load expense data from JSON file."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Expense data file not found: {DATA_FILE}"
        )
    except json.JSONDecodeError:
        raise ValueError("expense_data.json contains invalid JSON.")


def get_user_expenses(user_id: str):
    """Return all expenses belonging to a specific user."""
    expenses = load_expenses()

    return [
        expense
        for expense in expenses
        if expense["user_id"].upper() == user_id.upper()
    ]


def get_total_expenses(user_id: str) -> dict:
    """
    Calculate total expenses for a user.
    """
    expenses = get_user_expenses(user_id)

    total = sum(expense["amount"] for expense in expenses)

    return {
        "user_id": user_id,
        "total_expense": round(total, 2),
        "transaction_count": len(expenses),
    }


def get_expenses_by_category(user_id: str) -> dict:
    """
    Calculate total expenses grouped by category.
    """
    expenses = get_user_expenses(user_id)

    category_totals = defaultdict(float)

    for expense in expenses:
        category_totals[expense["category"]] += expense["amount"]

    result = {
        category: round(amount, 2)
        for category, amount in sorted(
            category_totals.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    }

    return {
        "user_id": user_id,
        "category_expenses": result,
    }


def get_expenses_by_merchant(user_id: str) -> dict:
    """
    Calculate total expenses grouped by merchant.
    """
    expenses = get_user_expenses(user_id)

    merchant_totals = defaultdict(float)

    for expense in expenses:
        merchant_totals[expense["merchant"]] += expense["amount"]

    result = {
        merchant: round(amount, 2)
        for merchant, amount in sorted(
            merchant_totals.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    }

    return {
        "user_id": user_id,
        "merchant_expenses": result,
    }


def get_expenses_by_date(
    user_id: str,
    start_date: str,
    end_date: str,
) -> dict:
    """
    Get expenses between start_date and end_date.

    Dates must be in YYYY-MM-DD format.
    """

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return {
            "error": "Invalid date format. Use YYYY-MM-DD."
        }

    if start > end:
        return {
            "error": "start_date cannot be greater than end_date."
        }

    expenses = get_user_expenses(user_id)

    filtered_expenses = []

    for expense in expenses:
        expense_date = datetime.strptime(
            expense["date"], "%Y-%m-%d"
        ).date()

        if start <= expense_date <= end:
            filtered_expenses.append(expense)

    total = sum(
        expense["amount"]
        for expense in filtered_expenses
    )

    return {
        "user_id": user_id,
        "start_date": start_date,
        "end_date": end_date,
        "total_expense": round(total, 2),
        "transaction_count": len(filtered_expenses),
        "expenses": filtered_expenses,
    }


def get_top_expenses(
    user_id: str,
    limit: int = 5,
) -> dict:
    """
    Return the largest expenses for a user.
    """

    if limit <= 0:
        return {
            "error": "limit must be greater than 0."
        }

    expenses = get_user_expenses(user_id)

    top_expenses = sorted(
        expenses,
        key=lambda expense: expense["amount"],
        reverse=True,
    )[:limit]

    return {
        "user_id": user_id,
        "top_expenses": top_expenses,
    }