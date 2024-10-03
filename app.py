from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    print("Hello World!")
    return render_template("index.html", title="HTracker - Home")
@app.route("/add", methods=["GET", "POST"])
def add_habit():
    return render_template("add_habit.html", title="HTracker - Add habit")



