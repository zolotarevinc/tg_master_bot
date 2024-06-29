import os
import logging
from random import randint
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# Start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Привет! Я игровой бот. Давай сыграем в игру 'Угадай число'. Я загадываю число от 1 до 100, а ты попробуй его угадать. Напиши /play чтобы начать!"
    )


# Play command
def play(update: Update, context: CallbackContext) -> None:
    number = randint(1, 100)
    context.user_data['number'] = number
    update.message.reply_text("Я загадал число от 1 до 100. Попробуй угадать его!")


# Guess command
def guess(update: Update, context: CallbackContext) -> None:
    try:
        user_guess = int(update.message.text)
        number = context.user_data.get('number')

        if not number:
            update.message.reply_text("Напиши /play чтобы начать игру.")
            return

        if user_guess < number:
            update.message.reply_text("Моё число больше. Попробуй ещё раз!")
        elif user_guess > number:
            update.message.reply_text("Моё число меньше. Попробуй ещё раз!")
        else:
            update.message.reply_text(f"Поздравляю! Ты угадал число: {number}. Напиши /play чтобы сыграть снова.")
            context.user_data['number'] = None
    except ValueError:
        update.message.reply_text("Пожалуйста, введи число.")


def main() -> None:
    token = os.getenv("TELEGRAM_TOKEN")
    updater = Updater(token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("play", play))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, guess))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
