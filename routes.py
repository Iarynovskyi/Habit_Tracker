from dateutil.utils import today
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from collections import defaultdict
import datetime
import uuid

pages = Blueprint("habits", __name__, template_folder="templates", static_folder="static")


@pages.context_processor
def add_calc_date_range():
    def date_range(start: datetime.datetime):
        return [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]

    return {"date_range": date_range}


def today_at_midnight():
    today = datetime.datetime.today()
    return today - datetime.timedelta(hours=today.hour, minutes=today.minute, seconds=today.second)


@pages.route("/")
def index():
    print([e for e in current_app.db.habits.find({})])  # Changed pages.db to current_app.db
    date_str = request.args.get("date")
    selected_date = datetime.datetime.fromisoformat(date_str) if date_str else datetime.datetime.today()

    habits_on_date = current_app.db.habits.find({"added": {"$lte": selected_date}})
    completions = [
        habit["habit"]
        for habit in current_app.db.completions.find({"date": selected_date})
    ]

    return render_template("index.html", title="HTracker - Home", habits=habits_on_date, completions=completions,
                           selected_date=selected_date)


@pages.route("/add", methods=["GET", "POST"])
def add_habit():
    today = today_at_midnight()
    if request.method == "POST":
        try:
            current_app.db.habits.insert_one(
                {
                    "_id": uuid.uuid4().hex,
                    "added": today,
                    "name": request.form.get("habit")
                }
            )
            return redirect(url_for("habits.index"))  # Ensure to redirect after adding a habit
        except Exception as e:
            print(f"Error adding habit: {e}")  # Add error logging here

    return render_template("add_habit.html", title="HTracker - Add habit", selected_date=today)


@pages.route("/complete", methods=["POST"])
def complete_habit():
    date_str = request.form.get("date")
    habit = request.form.get("habitId")
    date = datetime.datetime.fromisoformat(date_str)
    current_app.db.completions.insert_one({"habit": habit, "date": date})
    return redirect(url_for("habits.index", date=date_str))
