from enum import Enum
import functools
import logging

from environs import Env
import redis
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

from questions_db import QuestionsDatabase


logger = logging.getLogger(__name__)

State = Enum('State', ['START', 'ANSWERING'])


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    env = Env()
    env.read_env()
    tg_bot_token = env.str('TG_BOT_TOKEN')

    redis_db = redis.Redis(host=env.str('REDIS_DB_HOST'),
                           port=env.int('REDIS_DB_PORT'),
                           password=env.str('REDIS_DB_PASSWORD'),
                           decode_responses=True)
    questions_db = QuestionsDatabase()

    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data['redis_db'] = redis_db
    dispatcher.bot_data['questions_db'] = questions_db

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            State.START: [
                MessageHandler(
                    Filters.regex('^Новый вопрос'), handle_new_question_request
                ),
            ],
            State.ANSWERING: [
                MessageHandler(
                    Filters.text & ~Filters.command, handle_solution_attempt
                ),
            ],
        },
        fallbacks=[],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


def start(update: Update, _: CallbackContext):
    custom_keyboard = [['Новый вопрос', 'Сдаться'],
                       ['Мой счёт']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text("Здравствуйте!", reply_markup=reply_markup)
    return State.START


def handle_new_question_request(update: Update, context: CallbackContext):
    redis_db = context.bot_data['redis_db']
    questions_db = context.bot_data['questions_db']
    user = update.message.from_user.id
    with questions_db:
        question = questions_db.get_random_question()
    update.message.reply_text(question['question'])
    redis_db.set(user, question['id'])
    return State.ANSWERING


def handle_solution_attempt(update: Update, context: CallbackContext):
    redis_db = context.bot_data['redis_db']
    questions_db = context.bot_data['questions_db']
    user = update.message.from_user.id
    question_id = redis_db.get(user)
    with questions_db:
        ans = questions_db.get_question(question_id)['answer']
    if ans.split('.')[0] in update.message.text:
        update.message.reply_text('Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»')
        return State.START
    else:
        update.message.reply_text('Неправильно… Попробуешь ещё раз?')
        return State.ANSWERING


if __name__ == '__main__':
    main()
