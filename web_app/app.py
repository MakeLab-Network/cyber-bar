from flask import Flask, render_template, request, jsonify, redirect, url_for
from db_access import QuestionsDb
from gpt_api_tts import ask_gpt4

from speak import speak
import webbrowser
import os
import time

from gpt.prompts import ASK_GPT_FOR_RESPONSE_ON_1_ANSWER_FORMAT
questions_file_path = r"db\questions\questions_hebrew.json"


app = Flask(__name__, template_folder='quiz_app')


questions_db = QuestionsDb(questions_file_path)
quiz_questions_gen = questions_db.get_random_questions(20)
current_question = ""

@app.route('/')
def index():
    global current_question
    current_question = next(quiz_questions_gen)
    speak(current_question["question"])
    return render_template('quiz.html', question=current_question)


@app.route('/handle_button_press/', methods=['POST'])
def handle_button_press():
    try:
        # todo: load some intermidiate screen
        global current_question
        render_template('quiz_between_questions.html', question=current_question)
        # response = ask_gpt4(ASK_GPT_FOR_RESPONSE_ON_1_ANSWER_FORMAT.format(current_question["question"], current_question["answers"])) # ask gpt for a response, and read it
        print(ASK_GPT_FOR_RESPONSE_ON_1_ANSWER_FORMAT)
        response = ask_gpt4(ASK_GPT_FOR_RESPONSE_ON_1_ANSWER_FORMAT) # ask gpt for a response, and read it
        print(response)
        time.sleep(2)
        # todo: show the answer
        # todo: wait for response answer to finish
        current_question = next(quiz_questions_gen)
        speak(current_question["question"])
        return render_template('quiz.html', question=current_question)
    except StopIteration:
        return render_template('quiz_end.html')


if __name__ == '__main__':
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(host="127.0.0.1", port=5000, debug=True)
