from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from modules import InfoProteco, Reader, utils
import pandas as pd

# Constantes
TOKEN: Final = '6583577828:AAFOvhzQdsnnJFPWvtE8HIAZ0XaOk9MQ0JY' 
BOT_USERNAME: Final = '@proteco_telegram_bot'

TEMAS_ASESORIA: Final = ("Arduino", "Analísis de Circuitos", "Bases de Datos", "C", "C#", "C++", 
                         "Ciberseguridad", "Desarrollo Web", "Electrónica", "Ensamblador Z80", "Excel",
                         "Flutter", "Fundamentos de Programación", "Git-GitHub", "Instalación de Software",
                         "Java", "JavaScript", "Kubernetes", "LaTeX", "Linux", "Machine Learning",
                         "Mantenimiento de computadoras", "Matlab", "Office", "POO", "Python", "R",
                         "RaspberryPI", "React", "Redes de datos", "UML"
                         )
lector = Reader.Reader()

# Comandos
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Función para el comando /start
    Responde al usuario con un mensaje de bienvenida.
    --- Encargada de gestionar el comando /start ---
    Keywords arguments: 
    update -- primer argumento, objeto que representa la actualizacion recibida del bot, contiene informacion sobre -> mensaje, chat, usuario
    context -- parametro para almacenar datos y pasar informacion entre las diferentes funciones del bot -> Estado del usuario, historial, acceso a funcionalidades
    """
    await update.message.reply_text(' Hola, Gracias por comunicarte conmigo, yo soy PROTECO BOT')
    await update.message.reply_text('Comandos disponibles:\n\n'
                                    '/start - Inicializa el bot\n'
                                    '/help - Muestra los comandos disponibles\n'
                                    '/info - Muestra información sobre PROTECO\n'
                                    '/horarios_asesoria - Muestra los horarios de asesoría\n')
	

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Funcioń para el comando /help
    Responde al usuario una lista de comandos disponibles.
    --- Encargada de gestionar el comando /help ---
    Keyword arguments:
    Update -- primer argumento, objeto que representa la actualizacion recibida del bot, contiene informacion sobre -> mensaje, chat, usuario
    context -- parametro para almacenar datos y pasar informacion entre las diferentes funciones del bot -> Estado del usuario, historial, acceso a funcionalidades
    """
    await update.message.reply_text('Comandos disponibles:\n\n'
                                    '/start - Inicializa el bot\n'
                                    '/help - Muestra los comandos disponibles\n'
                                    '/info - Muestra información sobre PROTECO\n'
                                    '/horarios_asesoria - Muestra los horarios de asesoría\n')

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Función para el comando /info
    Activa el modo de información sobre el programa al usuario.
    -- Encargada de gestionar el comando /info --
    Keywords arguments:
    Update -- primer argumento, objeto que representa la actualización recibida del bot, contiene información sobre -> mensaje, chat, usuario
    context -- parámetro para almacenar datos y pasar información entre las diferentes funciones del bot -> Estado del usuario, historial, acceso a funcionalidades
    """
    context.user_data['option'] = 'info'
    await update.message.reply_text('Elige una opción:\n\n0. Salir\n1. Objetivo\n2. Misión')

async def view_schedules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Función para el comando /horarios_asesoria
    --- Encargada de gestionar el comando /horarios_asesoria ---
    Keywords arguments:
    Update -- primer argumento, objeto que representa la actualizacion recibida del bot, contiene informacion sobre -> mensaje, chat, usuario
    context -- parametro para almacenar datos y pasar informacion entre las diferentes funciones del bot -> Estado del usuario, historial, acceso a funcionalidades
    """
    context.user_data['option'] = 'schedule'
    await update.message.reply_text('Elige un tema de asesoría: \n' + '\n'.join([f'{i+1}. {tema}' for i, tema in enumerate(TEMAS_ASESORIA)]))
    return



# Manejadores de opciones
def schedule_reader(input):
    """
    Función que permite leer los horarios de asesoría especificados por el usuario.
    --- Encargada de gestionar las opciones de horarios de asesoría ---
    Keywords arguments:
    input -- texto de entrada especifico
    """
    if input.isdigit() and int(input) > 0 and int(input) <= len(TEMAS_ASESORIA):
        index = int(input) - 1
        if index < len(TEMAS_ASESORIA):
            return TEMAS_ASESORIA[index]
    elif input == '0':
        return 'menu'
    return False



# respuestas
def handle_response(text: str) -> str:
    """
    Funcion que procesa un texto de entrada especifico y devuelve una respuesta determinada a dicho texto
    --- Encargada de gestionar las respuestas del bot ---
    Keywords arguments:
    text -- texto de entrada especifico
    """
    # TODO: Implementar NLP para manejar respuestas más complejas
    processed: str = text.lower()

    if 'Hola' in processed:
        return 'Hola!'
    if '¿Como estas?' in processed:
        return 'Muy bien'
    
    return 'Lo sentimos, el bot por el momento no entiende mensajes de texto, sólo comandos. Por favor, intenta con un comando.'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Función encargada de gestionar los mensajes de texto del bot
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
            # Lectura de horarios
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
                    asesoria = utils.to_snake_case(asesoria)
                    df_online = lector.getHorarioAsesoriaEnLinea(asesoria)
                    df_presencial = lector.getHorarioAsesoriaPresencial(asesoria)

                    await update.message.reply_text(f'Horarios en línea:\n\n{lector.show_horarios(df_online)}')
                    await update.message.reply_text(f'Horarios presenciales:\n\n{lector.show_horarios(df_presencial)}')
                    context.user_data['option'] = None
                    return
            # Información
            case 'info':
                if text == '1':
                    await update.message.reply_text( InfoProteco.objetivo() )
                    response = 'Elige una opción:\n\n0. Salir\n1. Objetivo\n2. Misión'

                    
                elif text == '2':
                    await update.message.reply_text( InfoProteco.mision() )
                    response = 'Elige una opción:\n\n0. Salir\n1. Objetivo\n2. Misión'
                
                elif text == '0':
                    context.user_data['option'] = None
                    response = ('Comandos disponibles:\n\n'
                                    '/start - Inicializa el bot\n'
                                    '/help - Muestra los comandos disponibles\n'
                                    '/info - Muestra información sobre PROTECO\n'
                                    '/horarios_asesoria - Muestra los horarios de asesoría\n')

                else:
                    response = 'Por favor, elige una opción válida' 

    elif message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text) + '\n\n' + ('Comandos disponibles:\n\n'
                                    '/start - Inicializa el bot\n'
                                    '/help - Muestra los comandos disponibles\n'
                                    '/info - Muestra información sobre PROTECO\n'
                                    '/horarios_asesoria - Muestra los horarios de asesoría\n')
        else:
            return
    else:
        response: str = handle_response(text) + '\n\n' + ('Comandos disponibles:\n\n'
                                    '/start - Inicializa el bot\n'
                                    '/help - Muestra los comandos disponibles\n'
                                    '/info - Muestra información sobre PROTECO\n'
                                    '/horarios_asesoria - Muestra los horarios de asesoría\n')



    print('Bot: ', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Funcion encargada de gestionar los errores dentro del bot e imprimir el mensaje en consola
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
    app.add_handler(CommandHandler('info', info_command))
    app.add_handler(CommandHandler('horarios_asesoria', view_schedules_command))

    #Mensajes
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errores
    app.add_error_handler(error)
    
    # Polling
    app.run_polling(poll_interval=3)
    
