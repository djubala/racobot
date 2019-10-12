import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
import requests
from os import remove
import raco

imga5 = 'https://api.fib.upc.edu/v2/laboratoris/imatges/A5.png/?client_id=zN7ikID1R4aBfNIhZ0tgFogSXKdF348NnXzFbl6F'
imgb5 = 'https://api.fib.upc.edu/v2/laboratoris/imatges/B5.png/?client_id=zN7ikID1R4aBfNIhZ0tgFogSXKdF348NnXzFbl6F'
imgc6 = 'https://api.fib.upc.edu/v2/laboratoris/imatges/C6.png/?client_id=zN7ikID1R4aBfNIhZ0tgFogSXKdF348NnXzFbl6F'

def test(bot, update):
    mensaje = 'Esto es una *prueba*'
    bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)

def envia_imagen(bot, update, url):
    img = str(update.update_id)
    raco.descarga_imagen(img, url)
    bot.send_photo(chat_id=update.message.chat_id, photo=open(img, 'rb'))
    raco.borrar_imagen(img)

def imagen(bot, update, args):
    try:
        if len(args) == 0:
            envia_imagen(bot, update, imga5)
            envia_imagen(bot, update, imgb5)
            envia_imagen(bot, update, imgc6)
        for a in args:
            if a.lower().startswith('a5'):
                envia_imagen(bot, update, imga5) 
            elif a.lower().startswith('b5'):
                envia_imagen(bot, update, imgb5)
            elif a.lower().startswith('c6'):
                envia_imagen(bot, update, imgc6)
            else:
                mensaje = 'Error: no se reconoce ' + a
                bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)
    except Exception as e:
        print(e)
            
def hardware(bot, update, args):


# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()

# crea objectes per treballar amb Telegram
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# respuesta a los comandos
dispatcher.add_handler(CommandHandler('test', test))
dispatcher.add_handler(CommandHandler('imagen', imagen, pass_args=True))
dispatcher.add_handler(CommandHandler('hardware', hardware))

# arranca el bot
updater.start_polling()
