import os
import random
import logging

from tqdm import tqdm

from questions_db import QuestionsDatabase

logger = logging.getLogger(__name__)


def main():
    # TODO: решить проблему с наличием одиночных кавычек в текстах (возможно и других кавычек...)
    db = QuestionsDatabase()
    q = read_folder('quiz-questions')
    with db:
        db.insert_questions(q)


def read_questions_file(path: str) -> list[dict]:
    """Read file, export questions and answers.

    Args:
        path (str): A path to a quiz file to be read.

    Returns:
        list[dict]: A list of dicts containing question-answer pair.

    """
    with open(path, 'r', encoding='koi8-r') as file:
        text = file.read().split('\n\n')
    questions = []
    answers = []
    for text_part in text:
        if text_part.lower().strip().startswith('вопрос'):
            questions.append(text_part)
        elif text_part.lower().strip().startswith('ответ'):
            answers.append(text_part)

    questions_with_answers = []
    for index in range(len(questions)):
        questions_with_answers.append({
            'question': questions[index],
            'answer': answers[index]
        })
    return questions_with_answers


def read_folder(path) -> list[dict]:
    questions_with_answers = []
    for _, _, files in os.walk(path):
        for filename in tqdm(files):
            questions_with_answers += read_questions_file(os.path.join(path, filename))
    return questions_with_answers


def get_random_question():
    # TODO: delete me
    questions = read_questions_file('1vs1200.txt')
    random_question = random.choice(questions)
    return random_question


if __name__ == '__main__':
    main()

