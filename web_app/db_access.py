import json
import os
import random

sketch_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(sketch_dir, "..", "db")
questions_dir_path = os.path.join(db_path, "questions")


class Questions:
    @classmethod
    def get_random(cls):
        random_question_file = cls._get_random_question_json_file()
        with open(random_question_file) as file:
            data = json.load(file)
            questions = data["questions"]
            return dict(random.choice(questions))

    @classmethod
    def _get_random_question_json_file(cls):
        if os.path.exists(questions_dir_path) and os.path.isdir(questions_dir_path):
            json_files = [f for f in os.listdir(
                questions_dir_path) if f.endswith(".json")]

            return os.path.join(questions_dir_path, random.choice(json_files))
