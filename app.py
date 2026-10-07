from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)

# Secret key for admin login
app.secret_key = "dahel-secret-key"


# ==========================================
# CREATE DATABASE
# ==========================================

def create_database():

    conn = sqlite3.connect("dahel.db")
    cursor = conn.cursor()

    # Training registrations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS training_registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            training TEXT,
            training_type TEXT,
            experience TEXT,
            location TEXT,
            start_date TEXT,
            goal TEXT
        )
    """)

    # Orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            quantity TEXT,
            name TEXT,
            phone TEXT,
            address TEXT
        )
    """)

    conn.commit()
    conn.close()


create_database()


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# ORDER PAGE
# ==========================================

@app.route("/order", methods=["GET", "POST"])
def order():

    if request.method == "POST":

        product = request.form["product"]
        quantity = request.form["quantity"]
        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]

        # Save order to database
        conn = sqlite3.connect("dahel.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO orders
            (
                product,
                quantity,
                name,
                phone,
                address
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            product,
            quantity,
            name,
            phone,
            address
        ))

        conn.commit()
        conn.close()

        return render_template("success.html")

    return render_template("order.html")


# ==========================================
# TRAINING REGISTRATION
# ==========================================

@app.route("/training", methods=["GET", "POST"])
def training():

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]

        # Allow multiple training selections
        training = ", ".join(
            request.form.getlist("training")
        )

        training_type = request.form["training_type"]
        experience = request.form["experience"]
        location = request.form["location"]
        start_date = request.form["start_date"]
        goal = request.form["goal"]

        # Save registration
        conn = sqlite3.connect("dahel.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO training_registrations
            (
                name,
                phone,
                email,
                training,
                training_type,
                experience,
                location,
                start_date,
                goal
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            phone,
            email,
            training,
            training_type,
            experience,
            location,
            start_date,
            goal
        ))

        conn.commit()
        conn.close()

        return render_template("training_success.html")

    return render_template("training.html")


# ==========================================
# ADMIN LOGIN
# ==========================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "dahel123":

            session["admin_logged_in"] = True

            return redirect(url_for("admin"))

        else:

            return render_template(
                "admin_login.html",
                error="Invalid username or password"
            )

    return render_template("admin_login.html")


# ==========================================
# ADMIN DASHBOARD
# ==========================================

@app.route("/admin")
def admin():

    # Check login
    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin_login")
        )

    conn = sqlite3.connect("dahel.db")
    cursor = conn.cursor()


    # Get training registrations
    cursor.execute("""
        SELECT *
        FROM training_registrations
        ORDER BY id DESC
    """)

    registrations = cursor.fetchall()


    # Get orders
    cursor.execute("""
        SELECT *
        FROM orders
        ORDER BY id DESC
    """)

    orders = cursor.fetchall()


    conn.close()


    return render_template(
        "admin.html",
        registrations=registrations,
        orders=orders
    )


# ==========================================
# ADMIN LOGOUT
# ==========================================

@app.route("/admin/logout")
def admin_logout():

    session.pop(
        "admin_logged_in",
        None
    )

    return redirect(
        url_for("admin_login")
    )


# ==========================================
# RUN APP
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
    