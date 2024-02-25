from typing import Final
from telegram import Uptdate
from telegram.ext import Aplication, CommandHandler, MessageHandler, filters, ContextTypes


TOKEN: Final = '6583577828:AAFOvhzQdsnnJFPWvtE8HIAZ0XaOk9MQ0JY' 
BOT_USERNAME: Final = '@proteco_telegram_bot'

TEMAS_ASESORIA: Final = ("Arduino", "Analísis de Circuitos", "Bases de Datos", "C", "C#", "C++", 
                         "Ciberseguridad", "Desarrollo Web", "Electrónica", "Ensamblador Z80", "Excel",
                         "Flutter", "Fundamentos de Programación", "Git-GitHub", "Instalación de Software",
                         "Java", "JavaScript", "Kubernetes", "LaTeX", "Linux" "Machine Learning",
                         "Mantenimiento de computadoras", "Matlab", "Office", "POO", "Python", "R",
                         "Raspberyy PI", "React", "Redes de datos", "UML"
                         )

async def start_command(update: Uptdate, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(' Hola, Gracias por comunicarte conmigo, yo soy PROTECO BOT ')

async def help_command(update: Uptdate, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(' Hola, soy PROTECO BOT, escribe algo para que te pueda responder')

async def custom_command(update: Uptdate, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(' Este es un comando personalizado')

# respuestas
    
def handle_response(text: str) -> str:

    processed: str = text.lower()

    if 'Hola' in processed:
        return 'Hola'
    if '¿Como estas?' in processed:
        return 'Muy bien'
    
    return 'No entiendo lo que escribiste... '

async def handle_message(update: Uptdate, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User({update.message.chat.id}) in {message_type}: "{text}')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot: ', response)
    await update.message.reply_text(response)

async def erro(update: Uptdate, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Inicializando bot...')
    app = Application.builder().token(TOKEN).build()

    #Comandos
    app.add_handler(CommandHandler('Inicio', start_command))
    app.add_handler(CommandHandler('Ayuda', help_command))
    app.add_handler(CommandHandler('comando', custom_command))

    #Mensajes
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errores
    app.add_error_handler(error)
    
    #
    app.run_polling(poll_interval=3)
    
