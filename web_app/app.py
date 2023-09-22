from glob import glob
from tkinter.tix import Tree
from typing import Dict
from flask import Flask, render_template, request, redirect
from db_access import QuestionsDb
from gpt_api_tts import ask_gpt4, ask_gpt

import speak
import webbrowser
import os
import time
import random

questions_file_path = r"db\questions\prod_questions.json"


app = Flask(__name__, template_folder='quiz_app')


questions_db = QuestionsDb(questions_file_path)
quiz_questions_gen = questions_db.get_random_questions(2)
current_question = dict()
chosen_drink = -1


def init():
    global questions_db
    global quiz_question
    global current_quest
    global chosen_drink

    questions_db = QuestionsDb(questions_file_path)
    quiz_questions_gen = questions_db.get_random_questions(2)
    current_question = dict()
    chosen_drink = -1


# @app.context_processor
# def custom_template_context():
# def prepare_drink():
# global chosen_drink_drink
# gpt_api_tts.choose_drink()
# chosen_drink =

# Include the custom function in the template context
# return dict(print_hello=print_hello)


@app.route('/')
def index():
    init()
    global current_question
    current_question = next(quiz_questions_gen)
    speak.say(current_question["question"])
    return render_template('quiz.html', question=current_question)


@app.route('/quiz_question/', methods=['POST'])
def quiz_question():
    try:
        global current_question
        selected_option_index = int(request.form.get('selected_option'))

        speak.say(random.choice(
            current_question["answers"][selected_option_index]["responses"]), block=True)

        current_question = next(quiz_questions_gen)
        speak.say(current_question["question"])
        return render_template('quiz.html', question=current_question)
    except StopIteration:
        return redirect("/calculate_drink", code=302)


@app.route('/calculate_drink/', methods=['get'])
def calculate_drink():
    speak.minion_sound("minion_speak", block=False)
    return render_template('calc_drink.html')


@app.route('/drink_ready/', methods=['get'])
def drink_ready():
    speak.minion_sound("tada", block=True)
    return render_template('calc_drink.html')

def pourDrink(dispenser_index):
    # send command to arduino via serial
    pass

if __name__ == '__main__':
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(host="127.0.0.1", port=5000, debug=True)
