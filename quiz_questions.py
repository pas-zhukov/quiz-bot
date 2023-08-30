from argparse import ArgumentParser
import os
import random
import logging
import sqlite3

from tqdm import tqdm

from questions_db import QuestionsDatabase

logger = logging.getLogger(__name__)


def main():
    parser = ArgumentParser()
    parser.add_argument('path', help='Path to folder with questions', type=str)
    args = parser.parse_args()
    questions_path = args.path
    db = QuestionsDatabase()
    questions = read_folder(questions_path)
    with db:
        for index, question in enumerate(tqdm(questions, desc='Uploading questions.')):
            try:
                db.insert_question(question)
            except sqlite3.OperationalError:
                tqdm.write(f'Unable to import question #{index} into database. Question will be skipped.')


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
            questions.append(text_part[10:].replace('\n', ' '))
        elif text_part.lower().strip().startswith('ответ'):
            answers.append(text_part[7:].replace('\n', ' '))

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
        for filename in tqdm(files, desc='Parsing texts.'):
            questions_with_answers += read_questions_file(os.path.join(path, filename))
    return questions_with_answers


if __name__ == '__main__':
    main()

