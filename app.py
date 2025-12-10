from flask import Flask, render_template, request, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey123"  


def load_students():
    with open("students.json", "r") as f:
        return json.load(f)


def load_results():
    if not os.path.exists("results.json"):
        return {}
    with open("results.json", "r") as f:
        return json.load(f)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        students = load_students()

        if username in students and students[username]["password"] == password:
            session["username"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")

    username = session["username"]
    students = load_students()
    results = load_results()

    student = students[username]

    # Get this student's results
    student_results = results.get(username, {})

    return render_template("dashboard.html",
                           student=student,
                           results=student_results)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)