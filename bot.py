import logging

from environs import Env
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    env = Env()
    env.read_env()
    tg_bot_token = env.str('TG_BOT_TOKEN')

    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & ~Filters.command, reply_to_msg)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    updater.idle()


def start(update: Update, _: CallbackContext):
    """Send hello message when `/start` command is passed."""
    update.message.reply_text("Здравствуйте!")


def reply_to_msg(update: Update, _: CallbackContext):
    """Reply to a user message."""
    update.message.reply_text(update.message.text)


if __name__ == '__main__':
    main()
