from telegram.ext import Application, CommandHandler, MessageHandler, filters
from typing import Final
from routes.Commands import start_command, help_command, info_command, view_schedules_command, handle_message, error

# Constantes
TOKEN: Final = '6583577828:AAFOvhzQdsnnJFPWvtE8HIAZ0XaOk9MQ0JY' 

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
    
