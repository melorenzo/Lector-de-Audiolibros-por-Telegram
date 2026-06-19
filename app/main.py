import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Bot de audiolibros activo. Enviame un PDF o EPUB.")


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document

    if not file:
        await update.message.reply_text("❌ No recibí un archivo.")
        return

    file_obj = await file.get_file()

    os.makedirs("app/storage/books", exist_ok=True)

    file_path = f"app/storage/books/{file.file_name}"
    await file_obj.download_to_drive(file_path)

    await update.message.reply_text(f"📥 Archivo recibido: {file.file_name}")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    print("🤖 Bot corriendo...")
    app.run_polling()


if __name__ == "__main__":
    main()