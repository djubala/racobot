import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
import raco

imga5 = 'https://api.fib.upc.edu/v2/laboratoris/imatges/A5.png/?client_id=zN7ikID1R4aBfNIhZ0tgFogSXKdF348NnXzFbl6F'
imgb5 = 'https://api.fib.upc.edu/v2/laboratoris/imatges/B5.png/?client_id=zN7ikID1R4aBfNIhZ0tgFogSXKdF348NnXzFbl6F'
imgc6 = 'https://api.fib.upc.edu/v2/laboratoris/imatges/C6.png/?client_id=zN7ikID1R4aBfNIhZ0tgFogSXKdF348NnXzFbl6F'

def test(bot, update):
    mensaje = 'Esto es una *prueba*'
    bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)

def imagen(bot, update, args):
    if len(args) == 0:
        bot.send_photo(chat_id=update.message.chat_id, photo=imga5)
        bot.send_photo(chat_id=update.message.chat_id, photo=imgb5)
        bot.send_photo(chat_id=update.message.chat_id, photo=imgc6)
    for a in args:
        if a.lower().startswith('a5'):
            bot.send_photo(chat_id=update.message.chat_id, photo=imga5) 
        elif a.lower().startswith('b5'):
            bot.send_photo(chat_id=update.message.chat_id, photo=imgb5)
        elif a.lower().startswith('c6'):
            bot.send_photo(chat_id=update.message.chat_id, photo=imgc6)
        else:
            mensaje = 'Erconoror: no se reconoce ' + a
            bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)

# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()

# crea objectes per treballar amb Telegram
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# respuesta a los comandos
dispatcher.add_handler(CommandHandler('test', test))
dispatcher.add_handler(CommandHandler('imagen', imagen, pass_args=True))

# arranca el bot
updater.start_polling()
