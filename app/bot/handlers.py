from telegram import Update
from telegram.ext import ContextTypes

from services.book_service import save_book


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    document = update.message.document

    if not document:
        await update.message.reply_text(
            "❌ No recibí un archivo."
        )
        return

    success, result = await save_book(document)

    if not success:
        await update.message.reply_text(result)
        return

    await update.message.reply_text(
    f"📥 Archivo recibido: {result['filename']}\n"
    f"📄 Páginas: {result['pages']}\n"
    f"📖 Caracteres extraídos: {result['text_length']}"
)