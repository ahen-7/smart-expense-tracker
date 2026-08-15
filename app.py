from flask import Flask, render_template, request, redirect
from datetime import date
import sqlite3

app = Flask(__name__)
MONTHLY_BUDGET = 10000

def get_db():
    conn = sqlite3.connect("expenses.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL
        )
    """)

    columns = conn.execute("PRAGMA table_info(expenses)").fetchall()
    column_names = [column["name"] for column in columns]

    if "date" not in column_names:
        conn.execute("ALTER TABLE expenses ADD COLUMN date TEXT")

    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def home():

    conn = get_db()

    if request.method == "POST":

        # Get the values from the form FIRST
        expense = request.form["expense"]
        amount = float(request.form["amount"])
        category = request.form["category"]
        today = date.today().strftime("%Y-%m-%d")

        # Then save them
        conn.execute(
            """
            INSERT INTO expenses
            (expense, amount, category, date)
            VALUES (?, ?, ?, ?)
            """,
            (expense, amount, category, today)
        )

        conn.commit()

    expenses = conn.execute(
        "SELECT * FROM expenses ORDER BY id DESC"
    ).fetchall()
    total_expenses = sum(expense["amount"] for expense in expenses)
    remaining_budget = MONTHLY_BUDGET - total_expenses
    conn.close()

    return render_template(
    "index.html",
    expenses=expenses,
    monthly_budget=MONTHLY_BUDGET,
    total_expenses=total_expenses,
    remaining_budget=remaining_budget
)


@app.route("/delete/<int:index>")
def delete(index):

    conn = get_db()

    conn.execute(
        "DELETE FROM expenses WHERE id = ?",
        (index,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=False)
