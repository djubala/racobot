import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler

def test(bot, update):
    mensaje = "Esto es una *prueba* "
    bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)


# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()

# crea objectes per treballar amb Telegram
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# respuesta a los comandos
dispatcher.add_handler(CommandHandler('test', test))

# arranca el bot
updater.start_polling()
