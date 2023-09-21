from flask import Flask, render_template, request
from db_access import QuestionsDb
from gpt_api_tts import ask_gpt4, ask_gpt

from speak import speak
import webbrowser
import os
import time

from gpt.prompts import ASK_GPT_FOR_RESPONSE_ON_1_ANSWER_FORMAT, get_response_format
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
        
        # this doesn't work yet...
        render_template('quiz_between_questions.html', question=current_question)

        selected_option = request.form.get('selected_option')

        print("you selected: " + selected_option)
        # response = ask_gpt4(ASK_GPT_FOR_RESPONSE_ON_1_ANSWER_FORMAT.format(current_question["question"], selected_option)) # ask gpt for a response, and read it
        response = ask_gpt4(get_response_format().format(current_question["question"], selected_option))
        print(ASK_GPT_FOR_RESPONSE_ON_1_ANSWER_FORMAT)
        # response = ask_gpt(ASK_GPT_FOR_RESPONSE_ON_1_ANSWER_FORMAT) # ask gpt for a response, and read it
        print(response)
        # time.sleep(2) # little sleep for a small buffer after stop speaking
        # todo: show the answer
        current_question = next(quiz_questions_gen)
        # time.sleep(0.5) # wait a bit so the screen will show before talking
        speak(current_question["question"])
        return render_template('quiz.html', question=current_question)
    except StopIteration:
        return render_template('quiz_end.html')


if __name__ == '__main__':
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(host="127.0.0.1", port=5000, debug=True)
