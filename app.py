import os

print("Database Path:", os.path.abspath("finance.db"))
import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/images"
app.secret_key = "my_secret_key"

app.config["UPLOAD_FOLDER"] = "static/images"


# ---------------- HOME ----------------
@app.route("/")
def home():
    name = "Rajraushan"
    return render_template("home.html", username=name)


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("finance.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()

        connection.close()

        if user and check_password_hash(user[3], password):

            print("User =", user)
            session["user_id"] = user[0]
            session["username"] = user[1]
            print("✅ Login Successful")
            return redirect(url_for("dashboard"))

        else:
            print("❌ Invalid Email or Password")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    # ---------------- TOTAL INCOME ----------------

    # ---------------- TOTAL INCOME ----------------

    cursor.execute(
        "SELECT SUM(amount) FROM income WHERE username=?",
        (session["username"],)
    )

    income_result = cursor.fetchone()
    income = income_result[0] if income_result and income_result[0] else 0
    
    # ---------------- TOTAL EXPENSE ----------------

    cursor.execute(
        "SELECT SUM(amount) FROM expense WHERE username=?",
        (session["username"],)
    )

    expense_result = cursor.fetchone()
    expense = expense_result[0] if expense_result and expense_result[0] else 0


    # ---------------- PROFILE PHOTO ----------------

    cursor.execute(
        "SELECT id, profile_photo FROM users WHERE id=?",
         (session["user_id"],)
    )
    user = cursor.fetchone()

    if user:
        profile_photo = user[1]
    else:
        profile_photo = None


    connection.close()


    # ---------------- BALANCE ----------------

    balance = income - expense


    print("SESSION USERNAME =", session["username"])
    print("PROFILE PHOTO =", profile_photo)


    return render_template(
        "dashboard.html",
        username=session["username"],
        income=float(income),
        expense=float(expense),
        balance=float(balance),
        profile_photo=profile_photo
    )
# ---------------- PROFILE ----------------
@app.route("/profile", methods=["GET", "POST"])
def profile():

    if "username" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    # Get current user
    cursor.execute(
        "SELECT id, profile_photo FROM users WHERE name=?",
        (session["username"],)
    )

    user = cursor.fetchone()

    if request.method == "POST":

        photo = request.files["profile_photo"]

        if photo:

            filename = photo.filename

            photo.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

            cursor.execute(
                "UPDATE users SET profile_photo=? WHERE id=?",
                (filename, user[0])
            )

            connection.commit()

    connection.close()

    return redirect(url_for("dashboard"))           
# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.pop("username", None)

    return redirect(url_for("login"))


# ---------------- INCOME ----------------
@app.route("/income", methods=["GET", "POST"])
def income():

    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        amount = request.form["amount"]
        source = request.form["source"]
        date = request.form["date"]
        print("Amount =", amount)
        print("Source =", source)

        connection = sqlite3.connect("finance.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO income(username, amount, source, date)
            VALUES (?, ?, ?, ?)
            """,
            (session["username"], amount, source, date)
        )

        connection.commit()
        connection.close()

        print("✅ Income Saved Successfully")

    return render_template("income.html")


# ---------------- INCOME HISTORY ----------------
@app.route("/history")
def history():

    if "username" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM income WHERE username=?",
        (session["username"],)
    )

    incomes = cursor.fetchall()

    connection.close()

    return render_template(
        "history.html",
        incomes=incomes
    )

# ---------------- DELETE INCOME ----------------
@app.route("/delete_income/<int:id>")
def delete_income(id):

    if "username" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM income WHERE id=?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("history"))


@app.route("/expense", methods=["GET", "POST"])
def expense():

    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        amount = request.form["amount"]
        category = request.form["category"]
        date = request.form["date"]

        print("Amount =", amount)
        print("Category =", category)
        print("Date =", date)

        connection = sqlite3.connect("finance.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO expense(username, amount, category, date)
            VALUES (?, ?, ?, ?)
            """,
            (session["username"], amount, category, date)
        )

        connection.commit()
        connection.close()

        print("✅ Expense Saved Successfully")

        return redirect(url_for("expense_history"))

    return render_template("expense.html")
# ---------------- EXPENSE HISTORY ----------------
@app.route("/expense_history")
def expense_history():

    if "username" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM expense WHERE username=?",
        (session["username"],)
    )

    expenses = cursor.fetchall()

    connection.close()

    return render_template(
        "expense_history.html",
        expenses=expenses
    )

# ---------------- DELETE EXPENSE ----------------
@app.route("/delete_expense/<int:id>")
def delete_expense(id):

    if "username" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM expense WHERE id=?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("expense_history"))


# ---------------- BALANCE ----------------
@app.route("/balance")
def balance():

    if "username" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    # Total Income
    cursor.execute(
        "SELECT SUM(amount) FROM income WHERE username=?",
        (session["username"],)
    )
    total_income = cursor.fetchone()[0]

    # Total Expense
    cursor.execute(
        "SELECT SUM(amount) FROM expense WHERE username=?",
        (session["username"],)
    )
    total_expense = cursor.fetchone()[0]

    connection.close()

    if total_income is None:
        total_income = 0

    if total_expense is None:
        total_expense = 0

    balance = total_income - total_expense

    return render_template(
        "balance.html",
        income=total_income,
        expense=total_expense,
        balance=balance
    )


# ---------------- MONTHLY REPORT ----------------
@app.route("/report")
def report():

    if "username" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    # Total Income
    cursor.execute(
        "SELECT SUM(amount) FROM income WHERE username=?",
        (session["username"],)
    )
    income = cursor.fetchone()[0] or 0

    # Total Expense
    cursor.execute(
        "SELECT SUM(amount) FROM expense WHERE username=?",
        (session["username"],)
    )
    expense = cursor.fetchone()[0] or 0

    connection.close()

    balance = income - expense

    # ---------------- AI INSIGHT ----------------

    if expense == 0:

        insight = "You have not added any expenses yet. Start tracking your spending."

    elif expense > income:

        insight = "⚠️ Your expenses are higher than your income. Try to control unnecessary spending."

    elif balance > income * 0.5:

        insight = "🎉 Excellent! You are saving more than 50% of your income."

    else:

        insight = "👍 Your finances look stable. Keep tracking your daily expenses."

    return render_template(
        "report.html",
        income=income,
        expense=expense,
        balance=balance
    )

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return "Passwords do not match!"
        
        hashed_password = generate_password_hash(password)

        connection = sqlite3.connect("finance.db")
        cursor = connection.cursor()
       
        # Check if email already exists
        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()

        if user:
            connection.close()
            return "Email already registered!"

        # Save new user
        cursor.execute(
            """
            INSERT INTO users(name, email, password)
            VALUES (?, ?, ?)
            """,
            (name, email, hashed_password)
        )

        connection.commit()
        connection.close()

        print("✅ User Registered Successfully")

        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)