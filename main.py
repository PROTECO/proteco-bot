from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from modules import reader
import pandas as pd

# Constantes
TOKEN: Final = '6583577828:AAFOvhzQdsnnJFPWvtE8HIAZ0XaOk9MQ0JY' 
BOT_USERNAME: Final = '@proteco_telegram_bot'

TEMAS_ASESORIA: Final = ("Arduino", "Analísis de Circuitos", "Bases de Datos", "C", "C#", "C++", 
                         "Ciberseguridad", "Desarrollo Web", "Electrónica", "Ensamblador Z80", "Excel",
                         "Flutter", "Fundamentos de Programación", "Git-GitHub", "Instalación de Software",
                         "Java", "JavaScript", "Kubernetes", "LaTeX", "Linux" "Machine Learning",
                         "Mantenimiento de computadoras", "Matlab", "Office", "POO", "Python", "R",
                         "Raspberyy PI", "React", "Redes de datos", "UML"
                         )
lector = reader.Reader()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Funcion asincronica que permite realizar operaciones de entrada y salida sin bloquear el hilo de ejecucion.
    --- Encargada de gestionar el comando /start ---
    Keywords arguments: 
    update -- primer argumento, objeto que representa la actualizacion recibida del bot, contiene informacion sobre -> mensaje, chat, usuario
    context -- parametro para almacenar datos y pasar informacion entre las diferentes funciones del bot -> Estado del usuario, historial, acceso a funcionalidades
    """
    await update.message.reply_text(' Hola, Gracias por comunicarte conmigo, yo soy PROTECO BOT ')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Funcion asincronica que permite realizar operaciones de entrada y salida sin bloquear el hilo de ejecucion.
    --- Encargada de gestionar el comando /help ---
    Keyword arguments:
    Update -- primer argumento, objeto que representa la actualizacion recibida del bot, contiene informacion sobre -> mensaje, chat, usuario
    context -- parametro para almacenar datos y pasar informacion entre las diferentes funciones del bot -> Estado del usuario, historial, acceso a funcionalidades
    """
    await update.message.reply_text(' Hola, soy PROTECO BOT, escribe algo para que te pueda responder')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Funcion asincronica que permite realizar operaciones de entrada y salida sin bloquear el hilo de ejecucion.
    --- Encargada de gestionar los comandos personalizados por el usuario ---
    Keywords arguments:
    Update -- primer argumento, objeto que representa la actualizacion recibida del bot, contiene informacion sobre -> mensaje, chat, usuario
    context -- parametro para almacenar datos y pasar informacion entre las diferentes funciones del bot -> Estado del usuario, historial, acceso a funcionalidades
    """
    await update.message.reply_text(' Este es un comando personalizado')

# Manejadores de opciones
def schedule_reader(input):
    if input.isdigit() and int(input) > 0 and int(input) <= len(TEMAS_ASESORIA):
        index = int(input) - 1
        if index < len(TEMAS_ASESORIA):
            return TEMAS_ASESORIA[index]
    elif input == '0':
        return 'menu'
    return False



# respuestas
    
def handle_response(text: str) -> str:
    """Funcion que procesa un texto de entrada especifico y devuelve una respuesta determinada a dicho texto"""
    processed: str = text.lower()

    if 'Hola' in processed:
        return 'Hola'
    if '¿Como estas?' in processed:
        return 'Muy bien'
    
    return 'No entiendo lo que escribiste... '

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Funcion asincronica que permite realizar operaciones de entrada y salida sin bloquear el hilo de ejecucion.
    --- Encargada de la gestion de mensajes dentro del bot --- 
    Extrae el tipo de chat (grupo, canal o chat privado)
    Extrae el texto del mensaje recibido
    Imprime informacion sobre el usuario que envio el mensaje
    Imprime la respuesta generada
    Envia la respuesta al usuario
    Keywords arguments:
    Update -- primer argumento, objeto que representa la actualizacion recibida del bot, contiene informacion sobre -> mensaje, chat, usuario
    context -- parametro para almacenar datos y pasar informacion entre las diferentes funciones del bot -> Estado del usuario, historial, acceso a funcionalidades
    """
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User({update.message.chat.id}) in {message_type}: "{text}')
    
    if context.user_data['option'] != None:
        match context.user_data['option']:
            case 'schedule':
                response = schedule_reader(text)
                while not response:
                    await update.message.reply_text('Por favor, elige una opción válida')
                    return
                if response == 'menu':
                    context.user_data['option'] = None
                    await update.message.reply_text('Regresando al menú principal')
                    return
                else:
                    asesoria = TEMAS_ASESORIA[int(text)-1].lower()
                    df_online = lector.getHorarioAsesoriaEnLinea(asesoria)
                    df_presencial = lector.getHorarioAsesoriaPresencial(asesoria)

                    await update.message.reply_text(f'Horarios en línea:')
                    # TODO: Mostrar horarios con formato
                    
                    await update.message.reply_text(f'Horarios en presencial:')
                    # TODO: Mostrar horarios con formato

                    context.user_data['option'] = None
                    return

    elif message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)



    print('Bot: ', response)
    await update.message.reply_text(response)

async def erro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Funcion asincronica que permite realizar operaciones de entrada y salida sin bloquear el hilo de ejecucion.
    --- Encargada de la gestion de errores dentro del bot ---
    Imprime en consola un mensaje que indica la actualizacion que causo el error y el error especifico que ocurrio 
    Keywords arguments:
    Update -- primer argumento, objeto que representa la actualizacion recibida del bot, contiene informacion sobre -> mensaje, chat, usuario
    context -- parametro para almacenar datos y pasar informacion entre las diferentes funciones del bot -> Estado del usuario, historial, acceso a funcionalidades
    """
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Inicializando bot...')
    app = Application.builder().token(TOKEN).build()

    #Comandos
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('horarios_asesoria', view_schedules_command))

    #Mensajes
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errores
    app.add_error_handler(error)
    
    #
    app.run_polling(poll_interval=3)
    
