from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='quiz_app')

questions = [
    {
        'question_number': 1,
        'question_text': 'Who was the first King of the Vikings?',
        'correct_answer': 'Harald Fairhair',
        'options': ['Ragnar Lothbrok', 'Leif Erikson', 'Harald Fairhair', 'Ivar the Boneless']
    },
    {
        'question_number': 2,
        'question_text': 'Who was the first King of the Vikings?',
        'correct_answer': 'Harald Fairhair',
        'options': ['1', '2', '3', '4']
    },
    {
        'question_number': 3,
        'question_text': 'Who was the first King of the Vikings?',
        'correct_answer': 'Harald Fairhair',
        'options': ['Ragnar Lothbrok', 'Leif Erikson', 'Harald Fairhair', 'Ivar the Boneless']
    },
    # Add more questions here
]

current_question_index = 0

@app.route('/')
def index():
    current_question = questions[current_question_index]
    return render_template('quiz.html', question=current_question)

@app.route('/handle_button_press/', methods=['POST'])
def handle_button_press():
    global current_question_index  # Use the global variable
    
    selected_option = request.form.get('selected_option')
    print(selected_option)
    # current_question = questions[current_question_index]
    
    # if selected_option == current_question['correct_answer']:
        # current_question_index += 1
    
    # if current_question_index < len(questions):
        # next_question = questions[current_question_index]
        # return render_template('quiz.html', question=next_question)
    # else:
        # return render_template('quiz_complete.html')

if __name__ == '__main__':
    app.run(debug=True)
