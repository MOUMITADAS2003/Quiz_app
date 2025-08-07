
from flask import Flask, render_template, request, redirect, url_for
import json
import csv
import os

app = Flask(__name__)

QUIZ_FILE = "quizzes.json"
LEADERBOARD_FILE = "leaderboard.csv"

def load_quizzes():
    with open(QUIZ_FILE, "r") as f:
        return json.load(f)

@app.route("/")
def index():
    quizzes = load_quizzes()
    return render_template("index.html", quizzes=quizzes.keys())

@app.route("/quiz/<topic>", methods=["GET", "POST"])
def quiz(topic):
    quizzes = load_quizzes()
    questions = quizzes.get(topic, [])

    if request.method == "POST":
        name = request.form.get("name")
        score = 0
        for i, q in enumerate(questions):
            user_answer = request.form.get(f"q{i}")
            if user_answer == q["answer"]:
                score += 1

        # Save to leaderboard
        with open(LEADERBOARD_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, topic, score])

        return render_template("result.html", name=name, score=score, total=len(questions))

    return render_template("quiz.html", topic=topic, questions=questions)

@app.route("/leaderboard")
def leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return render_template("leaderboard.html", leaderboard=[])

    with open(LEADERBOARD_FILE, "r") as f:
        reader = csv.reader(f)
        data = sorted(reader, key=lambda x: int(x[2]), reverse=True)
    return render_template("leaderboard.html", leaderboard=data[:10])

if __name__ == "__main__":
    app.run(debug=True)
