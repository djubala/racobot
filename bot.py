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

def start(bot, update):
    try:
        mensaje = 'Bienvenido A Racobot!\nNecesitas Un Laboratorio Disponible?, Nosotros Te Ayudamos.\nEscriba */help* para ver los comandos disponibles'
        bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)
    except Exception as e:
        mensaje = "Ha ocurrido un error inesperado."
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)

def help(bot, update):
    """Envia un mensaje con la lista de posible comandos y sus explicaciones"""
    try:    
        mensaje = ("RacoBot facilitará la busqueda de laboratorios disponible en la Facultad de Informática de Barcelona.\n" +
                   "A continuación le facilitaremos los comandos disponibles:\n\n" +
                   "\"/help\" : Explicación del bot y comandos disponibles. Sin parámetros.\n" +
                   "\"/author\" : Nombre de los creadores del bot. Sin parámetros.\n" +
                   "\"/reset\" : Reinicia los valores cargados con los comandos edificio y filtrar a los valores por defecto. Sin parámetros.\n" +
                   "\"/edificio *nombre_edi*\" : El parametro *nombre_edi* es opcional. Si no tiene el parametro, listará los edificio y deseleccionará un edificio si se seleccionó anteriormente. Si se incluye parametro, se seleccionará ese edificio para los próximos comandos.\n" +
                   "\"/filtrar *tipo\s* *filtro\s*\" : Los parametros son opcionales. Si no tiene los parametros, listará los filtros disponibles. Si usa parametros, será necesario que incluya los dos en el siguiente formato: /filtrar *tipo1,tipo2,tipo3* *filtro1,filtro2,filtro3*\n" +
                    "\"/auladisp\" : Muestra las aulas que actualmente tienen sitios disponibles. Se ve afectado por los parámetros cambiados en edificio y filtra. Sin parámetros.\n" +
                   "\"/imagen\" : Enviará una imagen de las aulas disponibles en cada edificio. Si se ha utilizado el comando edificio, solo enviará la imagen del edificio seleccionado")
        bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)
    except Exception as e:
            print(e)
            mensaje = "Ha ocurrido un error inesperado."
            bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)

def author(bot, update):
    mensaje = "Bot creado por:\nDavid Jurado Balaer.\nVictor Vidal Rojas Condori"
    bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)

def auladisp(bot, update, user_data):
    try:    
        if 'edificio' not in user_data:
            eAux = None
        else:
            eAux = user_data['edificio'] 
        if 'aulas' not in user_data:
            aAux = None
        else:
            aAux = user_data['aulas']
        aux = raco.aules_disponibles(eAux, aAux)
        mensaje = "Las clases disponibles son:\n"
        for a in aux:
            mensaje = mensaje + a[0] + " : " + str(a[1]) + " sitios disponibles\n"
        bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)

    except Exception as e:
        print(e)
        mensaje = "Ha ocurrido un error inesperado."
        bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)

def reset(bot, update, user_data):
    try:    
        mensaje = "Se reiniciarán todos los valores por defecto"
        bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)
        user_data = None
    except Exception as e:
        print(e)
        mensaje = "Ha ocurrido un error inesperado."
        bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)
    

def edificio(bot, update, args, user_data):
    try:
        aux = raco.lista_edi()
        if len(args) == 0:
            mensaje = "La lista de edificio:\n"
            for x in aux:
                mensaje = mensaje + x + "\n"
            bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)
            user_data['edificio'] = None
        elif len(args) == 1:
            ind = aux.index(args[0])
            user_data['edificio'] = args[0].lower()
            mensaje = "Se ha seleccionado el edificio "+user_data['edificio']
            bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            mensaje = "El numero de argumentos no es correecto."
            bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN) 
    except ValueError as e:
        print(e)
        mensaje = "El edificio no existe."
        bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)
    except Exception as e:
        print(e)
        mensaje = "Ha ocurrido un error inesperado."
        bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)

def envia_imagen(bot, update, url):
    try:
        img = str(update.update_id)
        raco.descarga_imagen(img, url)
        bot.send_photo(chat_id=update.message.chat_id, photo=open(img, 'rb'))
        raco.borrar_imagen(img)
    except Exception as e:
            print(e)
            mensaje = "Ha ocurrido un error inesperado."
            bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)


def imagen(bot, update, user_data):
    try:
        if 'edificio' not in user_data:
            envia_imagen(bot, update, imga5)
            envia_imagen(bot, update, imgb5)
            envia_imagen(bot, update, imgc6)
        else:
            if user_data['edificio'].lower() == 'a5':
                envia_imagen(bot, update, imga5) 
            elif user_data['edificio'].lower() == 'b5':
                envia_imagen(bot, update, imgb5)
            elif user_data['edificio'].lower() == 'c6':
                envia_imagen(bot, update, imgc6)
            else:
                mensaje = "Error: no se reconoce el edificio " + a
                bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)
    except Exception as e:
        print(e)
        mensaje = "Ha ocurrido un error inesperado."
        bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)


def filtrar(bot, update, args, user_data):
    try:
        if len(args) == 0:
            mensaje =  ("Filtros disponibles:\n" +
                       "- cpu: tipo de cpu [i3, i5, i7]\n" +
                       "- cpugen: generacion de la CPU\n" +
                       "- pantalla_grande: [True, False]\n" +
                       "- mac: si tiene PCs o Macs [True, False]\n" +
                       "- so: si es aula de sistemas [True, False]\n")
            bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.HTML)
        elif len(args) != 2:
            mensaje = "Error: numero de parametros incorrecto. Debe ser 0 o 2"
            bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            filtros = args[0].split(',')
            valores = args[1].split(',')
            if len(filtros) != len(valores):
                mensaje = "Error: el numero de filtros debe ser igual al de valores"
                bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                if 'edificio' not in user_data:
                    ret = raco.filtrar_aulas(filtros, valores, None)
                    user_data['aulas'] = ret                    
                else:
                    ret = raco.filtrar_aulas(filtros, valores, user_data['edificio'])
                    user_data['aulas'] = ret
                mensaje = "Las aulas filtradas son:\n"                
                for x in ret:
                    mensaje = mensaje + x + "\n"
                bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)                    
    except ValueError as ve:
        mensaje = str(ve)
        bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)      
    except Exception as e:
        print(e)
        mensaje = "Ha ocurrido un error inesperado."
        bot.send_message(chat_id=update.message.chat_id, text=mensaje, parse_mode=telegram.ParseMode.MARKDOWN)


# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()

# crea objectes per treballar amb Telegram
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# respuesta a los comandos
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('author', author))
dispatcher.add_handler(CommandHandler('edificio', edificio, pass_args=True, pass_user_data=True))
dispatcher.add_handler(CommandHandler('filtrar', filtrar, pass_args=True, pass_user_data=True))
dispatcher.add_handler(CommandHandler('imagen', imagen, pass_user_data=True))
dispatcher.add_handler(CommandHandler('auladisp', auladisp, pass_user_data=True))
dispatcher.add_handler(CommandHandler('reset', reset, pass_user_data=True))

# arranca el bot
updater.start_polling()
