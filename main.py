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
    await update.message.reply_text(' Hola, Gracias por comunicarte conmigo, yo soy PROTECO BOT ')

async def view_schedules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['option'] = 'schedule'
    
    s = "0. Regresar al menú principal\n"
    for i, tema in enumerate(TEMAS_ASESORIA):
        s += f'{i+1}. {tema}\n'
    await update.message.reply_text('Estas son las asesorías disponibles:\n\n' + s)
    await update.message.reply_text('¿Cuál es el tema de tu interés?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(' Hola, soy PROTECO BOT, escribe algo para que te pueda responder')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    processed: str = text.lower()

    if 'Hola' in processed:
        return 'Hola'
    if '¿Como estas?' in processed:
        return 'Muy bien'
    
    return 'No entiendo lo que escribiste... '

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    
