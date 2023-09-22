from typing import Dict
from flask import Flask, render_template, request, redirect
from db_access import QuestionsDb
from gpt_api_tts import ask_gpt4, ask_gpt

import speak
import webbrowser
import os
import time
import random
import serial
import threading
import json

from gpt.prompts import FINAL_PROMPT, USER_Q_AND_A
recipes_path = r"db\recipes.json"

app = Flask(__name__, template_folder='quiz_app')
arduino_msg = ""
last_arduino_msg = ""
asked_questions = []


def update_arduino():
    global arduino_msg
    ser = serial.Serial('COM50', 9600, timeout=1)
    if not ser.isOpen():
        ser.open()

    try:
        while True:
            if last_arduino_msg != arduino_msg:
                ser.write(arduino_msg.encode())
                last_arduino_msg = arduino_msg
            print(f"Sent: {arduino_msg}")
    finally:
        ser.close()


questions_file_path = r"db\questions\prod_questions.json"

questions_db = QuestionsDb(questions_file_path)
quiz_questions_gen = questions_db.get_random_questions(1)
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
        global arduino_serial
        global asked_questions
        # arduino_serial.open()
        global current_question
        selected_option_index = int(request.form.get('selected_option'))

        speak.say(random.choice(
            current_question["answers"][selected_option_index]["responses"]), block=True)
        asked_questions.append(
            {"question": current_question['question'], "answer": current_question["answers"][selected_option_index]["answer"]})
        print(asked_questions)
        current_question = next(quiz_questions_gen)
        speak.say(current_question["question"])
        return render_template('quiz.html', question=current_question)
    except StopIteration:
        return redirect("/calculate_drink", code=302)


@app.route('/calculate_drink/', methods=['get'])
def calculate_drink():
    speak.minion_sound("minion_speak", block=False)
    making_the_drink()
    return render_template('calc_drink.html')


# @app.context_processor
# def custom_template_context():
def making_the_drink():
    drink_index = get_final_drink()
    print(drink_index)
    make_drink(drink_index)
    # return dict(making_the_drink=making_the_drink)


def parse_final_response(response):
    print("\n\nresponse start " + response[:5])
    index = response.split(r'\n')[0].split('.')[1].lstrip()
    print(f"index : {index}")
    if (index[1].isdigit()):
        return int(index[1] + index[0])
    else:
        return int(index[0])


def get_final_drink():
    FULL_Q_AND_A = ""
    global asked_questions
    for question in asked_questions:
        FULL_Q_AND_A += USER_Q_AND_A.format(
            question['question'], question['answer'])
    final_prompt = FINAL_PROMPT.format(FULL_Q_AND_A)
    response = ask_gpt4(final_prompt)
    return parse_final_response(response)


def make_drink(drink_index):
    with open(recipes_path, 'rb') as f:
        recipes = json.load(f)
    recipe = recipes['cocktails'][drink_index]
    for ing in recipe:
        pour_drink(ing['id'], ing['amount'])


@app.route('/drink_ready/', methods=['get'])
def drink_ready():
    speak.minion_sound("tada", block=True)
    # send cmd
    # wait for finish
    return render_template('calc_drink.html')


def pour_drink(dispenser_index, amount):
    global arduino_msg
    arduino_msg = f"t{dispenser_index} {amount}"
    msg_file_path = "arduino_msg.txt"
    with open(msg_file_path, 'w') as file:
        file.write(arduino_msg)


if __name__ == '__main__':
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(host="0.0.0.0", port=5000, debug=True)
