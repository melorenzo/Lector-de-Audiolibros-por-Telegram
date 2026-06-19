from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot.commands import start
from bot.handlers import handle_file
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    print("🤖 Bot corriendo...")
    app.run_polling()


if __name__ == "__main__":
    main()