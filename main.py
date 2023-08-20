with open('1vs1200.txt', 'r', encoding='koi8-r') as file:
    text = file.read().split('\n\n')

questions = []
answers = []

for text_part in text:
    if text_part.lower().strip().startswith('вопрос'):
        questions.append(text_part)
    elif text_part.lower().strip().startswith('ответ'):
        answers.append(text_part)
