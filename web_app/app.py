from flask import Flask, render_template, request, jsonify, session
from db_access import Questions as DBQuestions
from speak import speak


app = Flask(__name__, template_folder='quiz_app')
app.secret_key = 'asdflkj'  # Change this to a secure secret key

question_generator = DBQuestions.get_random_questions(20)
# def get_question_generator():
#     if 'question_generator_index' not in session:
#         session['question_generator_index'] = 0
#     if 'question_generator' not in session:
#         session['question_generator'] = list(
#             DBQuestions.get_random_questions(20))
#     return session['question_generator']


@app.route('/')
def index():
    # question_generator = get_question_generator()
    # current_index = session['question_generator_index']
    # current_question = question_generator?
    return render_template('quiz.html', question=next(question_generator))


@app.route('/handle_button_press/', methods=['POST'])
def handle_button_press():
    try:
        next_question = next(question_generator)
        speak(next_question["question"])
        return render_template('quiz.html', question=next_question)
    except StopIteration:
        return render_template('quiz_end.html')


if __name__ == '__main__':
    app.run(debug=True)
