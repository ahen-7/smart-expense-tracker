from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)

DATABASE = "expenses.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", methods=["GET", "POST"])
def home():
    conn = get_db()

    if request.method == "POST":

        # -------------------------
        # SET MONTHLY BUDGET
        # -------------------------
        if "budget" in request.form:
            new_budget = float(request.form["budget"])

            conn.execute(
                "UPDATE settings SET monthly_budget = ? WHERE id = 1",
                (new_budget,)
            )

            conn.commit()

        # -------------------------
        # ADD EXPENSE
        # -------------------------
        elif "expense" in request.form:
            expense = request.form["expense"]
            amount = float(request.form["amount"])
            category = request.form["category"]
            today = date.today().strftime("%Y-%m-%d")

            conn.execute(
                """
                INSERT INTO expenses (expense, amount, category, date)
                VALUES (?, ?, ?, ?)
                """,
                (expense, amount, category, today)
            )

            conn.commit()

        conn.close()
        return redirect(url_for("home"))

    # -------------------------
    # GET ALL EXPENSES
    # -------------------------
    expenses = conn.execute(
        "SELECT * FROM expenses ORDER BY id DESC"
    ).fetchall()

    # -------------------------
    # GET MONTHLY BUDGET
    # -------------------------
    budget_row = conn.execute(
        "SELECT monthly_budget FROM settings WHERE id = 1"
    ).fetchone()

    monthly_budget = budget_row["monthly_budget"]

    # -------------------------
    # CALCULATE TOTALS
    # -------------------------
    total_expenses = sum(
        expense["amount"] for expense in expenses
    )

    remaining_budget = monthly_budget - total_expenses

    conn.close()

    return render_template(
        "index.html",
        expenses=expenses,
        monthly_budget=monthly_budget,
        total_expenses=total_expenses,
        remaining_budget=remaining_budget
    )


# -------------------------
# DELETE EXPENSE
# -------------------------
@app.route("/delete/<int:index>")
def delete(index):
    conn = get_db()

    conn.execute(
        "DELETE FROM expenses WHERE id = ?",
        (index,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("home"))


# -------------------------
# UPDATE EXPENSE
# -------------------------
@app.route("/update/<int:index>", methods=["GET", "POST"])
def update(index):

    conn = get_db()

    if request.method == "POST":
        expense = request.form["expense"]
        amount = float(request.form["amount"])
        category = request.form["category"]

        conn.execute(
            """
            UPDATE expenses
            SET expense = ?, amount = ?, category = ?
            WHERE id = ?
            """,
            (expense, amount, category, index)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("home"))

    expense = conn.execute(
        "SELECT * FROM expenses WHERE id = ?",
        (index,)
    ).fetchone()

    conn.close()

    return render_template(
        "update.html",
        expense=expense
    )


if __name__ == "__main__":
    app.run(debug=True)
