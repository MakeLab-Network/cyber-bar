from flask import Flask, render_template
from db_access import QuestionsDb
from speak import speak
import webbrowser
import os

questions_file_path = r"db\questions\prod_questions.json"


app = Flask(__name__, template_folder='quiz_app')


questions_db = QuestionsDb(questions_file_path)
quiz_questions_gen = questions_db.get_random_questions(20)


@app.route('/')
def index():
    next_question = next(quiz_questions_gen)
    speak(next_question["question"])
    return render_template('quiz.html', question=next_question)


@app.route('/handle_button_press/', methods=['POST'])
def handle_button_press():
    try:
        next_question = next(quiz_questions_gen)
        speak(next_question["question"])
        return render_template('quiz.html', question=next_question)
    except StopIteration:
        return render_template('quiz_end.html')


if __name__ == '__main__':
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(host="127.0.0.1", port=5000, debug=True)
