import logging  # для ведения логов
import telegram as tg
import telegram.ext
import os
import requests
from dotenv import load_dotenv

logging.basicConfig(  # для ведения логов (оф. документация)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
# CHAT_ID = os.getenv('CHAT_ID')

updater = tg.ext.Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update: tg.Update, context: tg.ext.CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Введите код КН-24")


def echo(update: tg.Update, context: tg.ext.CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

echo_handler = tg.ext.MessageHandler(tg.ext.Filters.text & (~tg.ext.Filters.command), echo)
dispatcher.add_handler(echo_handler)


start_handler = tg.ext.CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()
