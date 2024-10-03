from flask import Flask, render_template, request, redirect, url_for
from collections import defaultdict
import datetime

app = Flask(__name__)

habits = ["Test habit", "Test habit 2"]
completions = defaultdict(list)


@app.context_processor
def add_calc_date_range():
    def date_range(start: datetime.date):
        return [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]

    return {"date_range": date_range}


@app.route("/")
def index():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.date.fromisoformat(date_str)
    else:
        selected_date = datetime.date.today()

    # Переконайтеся, що для вибраної дати є значення
    completions_list = completions.get(selected_date, [])

    return render_template("index.html", title="HTracker - Home", habits=habits, completions=completions_list,
                           selected_date=selected_date)


@app.route("/add", methods=["GET", "POST"])
def add_habit():
    if request.method == "POST":
        habit = request.form.get("habit")
        if habit:
            habits.append(habit)
            return redirect(url_for("index"))  # Перенаправлення на основну сторінку
    return render_template("add_habit.html", title="HTracker - Add habit", selected_date=datetime.date.today())


@app.route("/complete", methods=["POST"])
def complete_habit():
    date_str = request.form.get("date")
    habit = request.form.get("habitName")
    date = datetime.date.fromisoformat(date_str)
    completions[date].append(habit)

    return redirect(url_for("index", date=date_str))
