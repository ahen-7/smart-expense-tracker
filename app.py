from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


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

    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def home():

    conn = get_db()

    if request.method == "POST":
        expense = request.form["expense"]
        amount = float(request.form["amount"])
        category = request.form["category"]

        conn.execute(
            "INSERT INTO expenses (expense, amount, category) VALUES (?, ?, ?)",
            (expense, amount, category)
        )

        conn.commit()

    expenses = conn.execute(
        "SELECT * FROM expenses ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template("index.html", expenses=expenses)


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
