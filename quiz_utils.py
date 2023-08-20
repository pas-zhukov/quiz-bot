

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
        questions_with_answers[index] = {
            'question': questions[index],
            'answer': answers[index]
        }
    return questions_with_answers
