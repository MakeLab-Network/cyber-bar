from flask import Flask, render_template, request, jsonify, redirect, url_for
from db_access import QuestionsDb
from gpt_api_tts import ask_gpt4

from speak import speak
import webbrowser
import os

from gpt.prompts import ASK_GPT_FOR_RESPONSE_ON_1_ANSWER_FORMAT
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
        question = "test"
        # todo: load some intermidiate screen
        render_template('quiz_between_questions.html', question=question)
        response = ask_gpt4(ASK_GPT_FOR_RESPONSE_ON_1_ANSWER_FORMAT.format(next_question, answer)) # ask gpt for a response, and read it
        # todo: show the answer
        # todo: wait for response answer to finish
        next_question = next(quiz_questions_gen)
        speak(next_question["question"])
        return render_template('quiz.html', question=next_question)
    except StopIteration:
        return render_template('quiz_end.html')


if __name__ == '__main__':
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(host="127.0.0.1", port=5000, debug=True)
