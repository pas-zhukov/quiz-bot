import logging
import os
import random

from environs import Env
import redis
import vk_api as vk
from vk_api.keyboard import VkKeyboard
from vk_api.longpoll import VkLongPoll, VkEventType

from questions_db import QuestionsDatabase


logger = logging.getLogger('VKBot')


def main():
    """Main function."""
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    env = Env()
    env.read_env()
    vk_bot_token = os.getenv('VK_BOT_TOKEN')

    redis_db = redis.Redis(host=env.str('REDIS_DB_HOST'),
                           port=env.int('REDIS_DB_PORT'),
                           password=env.str('REDIS_DB_PASSWORD'),
                           decode_responses=True)
    questions_db = QuestionsDatabase()

    vk_session = vk.VkApi(token=vk_bot_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer_msg(event, vk_api, redis_db, questions_db)


def answer_msg(event, vk_api, redis_db, questions_db):
    """Reply to users message."""
    keyboard_btns = [['Новый вопрос', 'Сдаться'], ['Мой счёт']]
    keyboard = None

    if event.text == 'Начать':
        text = 'Привет! Да начнётся викторина!'
        keyboard = get_keyboard(keyboard_btns).get_keyboard()
    elif event.text == 'Новый вопрос':
        text = handle_new_question_request(event.user_id, redis_db, questions_db)
    elif event.text == 'Сдаться':
        text = give_up(event.user_id, vk_api, redis_db, questions_db)
    else:
        text = handle_solution_attempt(event.text, event.user_id, redis_db, questions_db)

    vk_api.messages.send(
        user_id=event.user_id,
        message=text,
        random_id=random.randint(1, 1000),
        keyboard=keyboard
    )


def handle_new_question_request(user_id, redis_db, questions_db):
    with questions_db:
        question = questions_db.get_random_question()
    redis_db.set(user_id, question['id'])
    return question['question']


def give_up(user_id, vk_api, redis_db, questions_db):
    question_id = redis_db.get(user_id)
    with questions_db:
        ans = questions_db.get_question(question_id)['answer']
    vk_api.messages.send(
        user_id=user_id,
        message=f'Правильный ответ: {ans}',
        random_id=random.randint(1, 1000),
    )
    return handle_new_question_request(user_id, redis_db, questions_db)


def handle_solution_attempt(user_ans, user_id, redis_db, questions_db):
    question_id = redis_db.get(user_id)
    with questions_db:
        ans = questions_db.get_question(question_id)['answer']
    if ans.split('.')[0] in user_ans:
        return 'Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»'
    else:
        return 'Неправильно… Попробуешь ещё раз?'


def get_keyboard(buttons: list[list[str]]):
    keyboard = VkKeyboard()
    for index, btn_line in enumerate(buttons):
        for btn in btn_line:
            keyboard.add_button(btn)
        if index < len(buttons) - 1:
            keyboard.add_line()
    return keyboard


if __name__ == '__main__':
    main()
