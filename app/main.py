import os
import logging

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)

from bot.commands import start
from bot.handlers import handle_file

TOKEN = os.getenv(
    "TELEGRAM_TOKEN"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


def main():

    app = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        MessageHandler(
            filters.Document.ALL,
            handle_file
        )
    )

    logging.info(
        "🤖 Bot corriendo..."
    )

    app.run_polling()


if __name__ == "__main__":
    main()