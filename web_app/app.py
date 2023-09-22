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
recipes_path = r"db\220923-1000 Final cocktails.txt"

app = Flask(__name__, template_folder='quiz_app')
arduino_msg = ""
last_arduino_msg = ""
asked_questions = []
receive_file_path = "from_arduino.txt"
drink_index = 1


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
quiz_questions_gen = questions_db.get_random_questions(4)
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
    chosen_drink = 1


@app.route('/')
def index():
    global questions_db
    global quiz_question
    global current_quest
    global chosen_drink

    questions_db = QuestionsDb(questions_file_path)
    quiz_questions_gen = questions_db.get_random_questions(2)
    current_question = dict()
    chosen_drink = 1

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
        try:
            speak.say(random.choice(
                current_question["answers"][selected_option_index]["responses"]), block=True)
            asked_questions.append(
                {"question": current_question['question'], "answer": current_question["answers"][selected_option_index]["answer"]})
            print(asked_questions)
        except KeyError:
            return redirect('/')
        current_question = next(quiz_questions_gen)
        speak.say(current_question["question"])
        return render_template('quiz.html', question=current_question)
    except StopIteration:
        return redirect("/calculate_drink", code=302)


@app.route('/calculate_drink/', methods=['get'])
def calculate_drink():
    # speak.minion_sound("minion_speak", block=False)
    return render_template('proc.html')


@app.route('/calculate_drink/proc/', methods=['get'])
def proc():
    making_the_drink()
    return redirect('/drink_ready_disp/')

# @app.context_processor
# def custom_template_context():


def making_the_drink():
    global drink_index
    drink_index = get_final_drink()
    print(drink_index)

    # return dict(making_the_drink=making_the_drink)


@app.route('/random/', methods=['POST', 'GET'])
def random_drink():
    with open(recipes_path, 'rb') as f:
        recipes = json.load(f)
    # print(recipes['cockt  ails'])

    recipe = random.choice(recipes['cocktails'])['ingredients']
    text = ""
    last_pos = 5
    for ing in recipe:
        pos = int(ing['id'] - 1)
        pour_drink(pos, int(ing['amount']) * 1000)
        distance_to_pos = abs(last_pos - pos)
        if (pos <= 14):
            time.sleep((1*distance_to_pos) + 5)
        last_pos = pos
    pour_drink(20, 100)  # end
    speak.minion_sound("tada", block=False)
    return render_template('rand-test.html')


@app.route('/drink_ready_disp/', methods=['get'])
def drink_ready_mid():
    with open(recipes_path, 'rb') as f:
        recipes = json.load(f)
    # print(recipes['cockt  ails'])
    recipe = recipes['cocktails'][drink_index - 1]['ingredients']
    text = ""
    for ing in recipe:
        text += ing['name'] + " "
    return render_template('disp.html', drink_ing=text)


def parse_final_response(response):
    print("\n\nresponse start " + response[:5])
    index = response.split(r'\n')[0].split('.')[1].lstrip()
    print(f"index : {index}")
    if (index[1].isdigit()):
        return int(index[0] + index[1])
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
    # print(recipes['cockt  ails'])
    recipe = recipes['cocktails'][drink_index - 1]
    last_pos = 5
    for ing in recipe['ingredients']:
        pos = int(ing['id']-1)
        pour_drink(pos, int(ing['amount']) * 1000)
        distance_to_pos = abs(last_pos - pos)
        if (pos <= 14):
            time.sleep((1*distance_to_pos) + 5)
        last_pos = pos


@app.route('/drink_ready_disp/drink_ready/', methods=['get'])
def drink_ready():
    global drink_index
    make_drink(drink_index)
    speak.minion_sound("tada", block=False)
    # send cmd
    # wait for finish
    return redirect('/')


def pour_drink(dispenser_index, amount):
    arduino_msg = f"t{dispenser_index} {amount}"
    print(f"pouring {arduino_msg}")
    msg_file_path = "to_arduino.txt"
    with open(msg_file_path, 'w') as file:
        file.write(arduino_msg)
    # msg_from_arduino = ''
    # while not msg_from_arduino:
    #     with open(receive_file_path, 'r') as file:
    #         msg_from_arduino = file.read()
    #     if msg_from_arduino and msg_from_arduino[0] != "$":
    #         msg_from_arduino = ''


if __name__ == '__main__':
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(host="0.0.0.0", port=5000, debug=True)
