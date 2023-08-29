import functools
import logging

from environs import Env
import redis
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from quiz_questions import get_random_question


logger = logging.getLogger(__name__)


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

    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data['redis_db'] = redis_db

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & ~Filters.command, reply_to_msg)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    updater.idle()


def start(update: Update, _: CallbackContext):
    custom_keyboard = [['Новый вопрос', 'Сдаться'],
                       ['Мой счёт']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text("Здравствуйте!", reply_markup=reply_markup)


def reply_to_msg(update: Update, context: CallbackContext):
    redis_db = context.bot_data['redis_db']
    user = update.message.from_user.id
    if update.message.text == 'Новый вопрос':
        question = get_random_question()
        update.message.reply_text(question['question'])
        redis_db.set(user, question['question'])
    else:
        ans = redis_db.get(user)
        update.message.reply_text(ans)


if __name__ == '__main__':
    main()
