from flask import Flask, render_template, request

app = Flask(__name__)

habits = ["Test habit", "Test habit 2"]

@app.route("/")
def index():
    print("Hello World!")
    return render_template("index.html", title="HTracker - Home", habits=habits)
@app.route("/add", methods=["GET", "POST"])
def add_habit():
    if request.method == "POST":
        habits.append(request.form.get("habit"))
    return render_template("add_habit.html", title="HTracker - Add habit")



