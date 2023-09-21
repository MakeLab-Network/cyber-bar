import json
import os
import random


class QuestionsDb:
    def __init__(self, json_file_path: str) -> None:
        self._load_json_file(json_file_path)

    def _load_json_file(self, json_file_path):
        if os.path.exists(json_file_path):
            self._json_file_path = json_file_path
        else:
            raise Exception(f"cant find question file {json_file_path}")

        with open(self._json_file_path, 'r', encoding="utf-8") as json_file:
            data = json.load(json_file)
            self._unused_questions: list = data["questions"]

    def get_random_questions(self, amount):
        for i in range(amount):
            base_question = self.get_random_question()
            base_question["question_number"] = i
            yield base_question

    def get_random_question(self) -> dict:
        random_question = random.choice(self._unused_questions)
        self._unused_questions.remove(random_question)
        return random_question
