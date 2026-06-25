import os
import logging

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

from bot.commands import start, next_chunk, status
from bot.handlers import handle_file, handle_replace_callback

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
        .connect_timeout(120)
        .write_timeout(120)
        .read_timeout(120)
        .pool_timeout(120)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CommandHandler(
            "next",
            next_chunk
        )
    )

    app.add_handler(
        CommandHandler(
            "status",
            status
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            handle_replace_callback,
            pattern="^replace:"
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