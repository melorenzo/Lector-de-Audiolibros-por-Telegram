import asyncio
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from services.book_service import save_book
from services.audio_worker import process_job
from services.job_manager import get_job, delete_job

logger = logging.getLogger(__name__)


async def handle_file(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    chat_id = update.effective_chat.id
    document = update.message.document

    if not document:

        await update.message.reply_text(
            "❌ No recibí un archivo."
        )

        return

    active_job = get_job(chat_id)

    if active_job:

        context.user_data["pending_document"] = document

        keyboard = [
            [
                InlineKeyboardButton(
                    "✅ Sí, cancelar y empezar nuevo",
                    callback_data="replace:yes"
                )
            ],
            [
                InlineKeyboardButton(
                    "❌ No, mantener el actual",
                    callback_data="replace:no"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"Ya tienes '{active_job.filename}' en proceso.\n"
            f"¿Cancelarlo y empezar con '{document.file_name}'?",
            reply_markup=reply_markup
        )

        return

    success, result = await save_book(document, chat_id)

    if not success:

        await update.message.reply_text(result)

        return

    await update.message.reply_text(

        f"📥 Archivo recibido: {result['filename']}\n"
        f"📄 Páginas: {result['pages']}\n"
        f"📖 Caracteres: {result['text_length']}\n"
        f"🎧 Chunks: {result['chunks']}\n"
        f"🚀 Comenzando generación..."

    )

    job = result["job"]

    asyncio.create_task(
        process_job(job, context.bot, chat_id)
    )


async def handle_replace_callback(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    decision = query.data.split(":")[1]
    chat_id = update.effective_chat.id

    if decision == "yes":

        document = context.user_data.get(
            "pending_document"
        )

        if not document:

            await query.edit_message_text(
                "❌ El archivo original ya no está disponible. "
                "Vuelve a enviarlo."
            )

            return

        delete_job(chat_id)

        success, result = await save_book(
            document,
            chat_id
        )

        if not success:

            await query.edit_message_text(result)

            return

        await query.edit_message_text(
            f"📥 Nuevo libro: {result['filename']}\n"
            f"📄 Páginas: {result['pages']}\n"
            f"📖 Caracteres: {result['text_length']}\n"
            f"🎧 Chunks: {result['chunks']}\n"
            f"🚀 Comenzando generación..."
        )

        job = result["job"]

        asyncio.create_task(
            process_job(job, context.bot, chat_id)
        )

    else:

        await query.edit_message_text(
            "Ok, el libro actual sigue en proceso."
        )

    context.user_data.pop("pending_document", None)