import random
import logging

logger = logging.getLogger(__name__)


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
    logger.critical(str([len(questions), len(answers)]))

    questions_with_answers = []
    for index in range(len(questions)):
        questions_with_answers.append({
            'question': questions[index],
            'answer': answers[index]
        })
    return questions_with_answers


def read_folder(path: str) -> list[dict]:
    pass


def get_random_question():
    # TEMPORARY
    questions = read_questions_file('1vs1200.txt')
    random_question = random.choice(questions)
    return random_question


if __name__ == '__main__':
    print(get_random_question())