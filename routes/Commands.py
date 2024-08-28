from telegram import Update
from telegram.ext import ContextTypes
from typing import Final
from utils import NamingConventions, InfoProteco, InternReader
from utils.naming_conventions import NamingConventions

BOT_USERNAME: Final = '@proteco_telegram_bot'

TEMAS_ASESORIA: Final = (
    'poo', 'metodologias_agiles', 'excel', 'cloud', 'arduino', 'redes', 'plantuml', 'c++', 'git_&_github', 
    'java', 'python', 'fundamentos_de_programacion', 'estructuras_de_datos_y_algoritmos', 'css', 'diseno_bases_de_datos', 
    'machine_learning', 'matlab', 'c', 'docker', 'c#', 'valorant', 'html', 'r', 'javascript', 'raspberrypi', 
    'bases_de_datos', 'instalacion_de_software', 'js', 'ciberseguridad', 'sql', 'desarrollo_web', 'latex', 
    'powerbi', 'mantenimiento_de_computadoras', 'django.', 'inteligencia_artificial', 'linux', 'react'
)

TEMAS_ASESORIA_FORMATEADOS: Final = [NamingConventions.snake_to_capitalized(tema) for tema in TEMAS_ASESORIA]

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
    # Reiniciar el estado del usuario
    context.user_data['option'] = None
    
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
    # Setear la opción
    context.user_data['option'] = 'info'
    
    # Mostrar las opciones
    await update.message.reply_text('Elige una opción:\n\n0. Salir\n1. Objetivo\n2. Misión')

async def view_schedules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Función para el comando /horarios_asesoria
    --- Encargada de gestionar el comando /horarios_asesoria ---
    Keywords arguments:
    Update -- primer argumento, objeto que representa la actualizacion recibida del bot, contiene informacion sobre -> mensaje, chat, usuario
    context -- parametro para almacenar datos y pasar informacion entre las diferentes funciones del bot -> Estado del usuario, historial, acceso a funcionalidades
    """
    # Setear la opción
    context.user_data['option'] = 'schedule'
    
    # Mostrar quién solicitó la información
    print(f'Usuario: {update.message.from_user.username} Solicitó información sobre PROTECO\n\n')
    
    # Mostrar los temas de asesoría
    await update.message.reply_text('Elige un tema de asesoría: \n\n0. Cancelar' + '\n'.join([f'{i+1}. {tema}' for i, tema in enumerate(TEMAS_ASESORIA_FORMATEADOS)]))
    return



# Manejadores de opciones
def schedule_option_reader(input):
    """
    Función que permite leer los horarios de asesoría especificados por el usuario.
    --- Encargada de gestionar las opciones de horarios de asesoría ---
    Keywords arguments:
    input -- texto de entrada especifico
    """
    # Verificar si el input es un número y si está en el rango de los temas de asesoría
    if input.isdigit() and int(input) > 0 and int(input) <= len(TEMAS_ASESORIA):
        index = int(input) - 1
        if index < len(TEMAS_ASESORIA):
            return TEMAS_ASESORIA[index]
        
    # Verificar si se desea regresar al menú
    elif input == '0':
        return 'menu'
    
    # Si no se cumple ninguna condición, regresar False
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
    # Procesar el texto
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
    
    if context.user_data['option'] != None:
        match context.user_data['option']:
            
            
            # Lectura de horarios
            case 'schedule':
                response = schedule_option_reader(text)
                while not response:
                    await update.message.reply_text('Por favor, elige una opción válida')
                    return
                if response == 'menu':
                    context.user_data['option'] = None
                    await update.message.reply_text('Regresando al menú principal')
                    return
                else:
                    # Crear un lector de horarios
                    lector: InternReader = InternReader()
                    
                    # Obtener los horarios
                    horarios = lector.get_horarios(response)

                    # Mostrar los horarios
                    await update.message.reply_text(f'Horarios:\n\n{horarios}')
                    
                    # Regresar al menú principal
                    context.user_data['option'] = None
                    await update.message.reply_text('Regresando al menú principal...')
                    
                    # Mostrar en pantalla el usuario y el tema de asesoría
                    print(f'Usuario: {update.message.from_user.username}\nTema de asesoría: {response}\n\n')
                    
                    return
                
            # Información de PROTECO
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
                                    '/info - Da información sobre PROTECO\n'
                                    '/horarios_asesoria - Muestra los horarios de asesoría\n')

                else:
                    response = 'Por favor, elige una opción válida' 

    # Si el bot se encuentra en un grupo
    elif message_type == 'group':
        # Sólo responder si el bot es mencionado
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text) + '\n\n' + ('Comandos disponibles:\n\n'
                                    '/start - Inicializa el bot\n'
                                    '/help - Muestra los comandos disponibles\n'
                                    '/info - Da información sobre PROTECO\n'
                                    '/horarios_asesoria - Muestra los horarios de asesoría\n')
        else:
            return
        
    # Si el bot se encuentra en un chat privado
    else:
        response: str = handle_response(text) + '\n\n' + ('Comandos disponibles:\n\n'
                                    '/start - Inicializa el bot\n'
                                    '/help - Muestra los comandos disponibles\n'
                                    '/info - Muestra información sobre PROTECO\n'
                                    '/horarios_asesoria - Muestra los horarios de asesoría\n')


    # Log de la respuesta
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