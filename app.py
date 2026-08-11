from flask import Flask, render_template, request, redirect

app = Flask(__name__)

expenses = []


@app.route("/", methods=["GET", "POST"])
@app.route("/delete/<int:index>")
def delete(index):
    if 0 <= index < len(expenses):
        expenses.pop(index)

    return redirect("/")
def home():

    if request.method == "POST":
        expense = request.form["expense"]
        amount = float(request.form["amount"])
        category = request.form["category"]

        expenses.append({
            "expense": expense,
            "amount": amount,
            "category": category
        })

    return render_template("index.html", expenses=expenses)


if __name__ == "__main__":
    app.run(debug=True)
