import asyncio
import logging

from telegram import Update
from telegram.ext import ContextTypes

from services.job_manager import get_job

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Bot de audiolibros activo.\n\n"
        "Envía un PDF o EPUB para convertirlo a audio.\n"
        "Usa /next para recibir más fragmentos "
        "(lotes de hasta 10 por vez).\n"
        "Usa /status para ver el progreso."
    )


async def next_chunk(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    chat_id = update.effective_chat.id
    job = get_job(chat_id)

    if not job:

        await update.message.reply_text(
            "📭 No tienes ningún libro en proceso. "
            "Envía un PDF o EPUB para empezar."
        )

        return

    total = len(job.chunks)
    next_idx = job.sent_up_to

    if next_idx >= total:

        await update.message.reply_text(
            "🏁 ¡Terminaste el libro completo! 🎉\n"
            "Puedes subir otro PDF o EPUB."
        )

        return

    generated_count = len(job.generated)

    if next_idx >= generated_count:

        if not job.finished:

            await update.message.reply_text(
                "⏳ Aún se están generando los fragmentos, "
                "espera unos segundos..."
            )

            waited = 0

            while waited < 30 and generated_count <= next_idx:

                await asyncio.sleep(3)
                waited += 3
                generated_count = len(job.generated)

        if next_idx >= generated_count:

            remaining = next_idx - generated_count + 1

            await update.message.reply_text(
                f"⏳ Aún no hay fragmentos listos. "
                f"Faltan ~{remaining} por generar.\n"
                "Intenta de nuevo en unos momentos."
            )

            return

    batch_end = min(next_idx + 9, total - 1)
    batch_end = min(batch_end, generated_count - 1)

    sent = 0

    for i in range(next_idx, batch_end + 1):

        audio_path = job.generated[i]

        if not audio_path:
            continue

        try:
            await context.bot.send_audio(
                chat_id=chat_id,
                audio=open(audio_path, "rb"),
                caption=(
                    f"🎧 Fragmento {i + 1} de {total} "
                    f"— {job.filename}"
                )
            )
            sent += 1
        except Exception as e:
            logger.error(
                f"Error enviando chunk {i}: {e}"
            )

    job.sent_up_to = batch_end + 1

    if sent > 0:

        remaining_after = total - job.sent_up_to

        if remaining_after > 0:

            await update.message.reply_text(
                f"📤 Enviados {sent} fragmento(s). "
                f"Quedan {remaining_after}.\n"
                "Usa /next para recibir más."
            )

        else:

            await update.message.reply_text(
                "🏁 ¡Terminaste el libro completo! 🎉"
            )


async def status(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    chat_id = update.effective_chat.id
    job = get_job(chat_id)

    if not job:

        await update.message.reply_text(
            "📭 No tienes ningún libro en proceso."
        )

        return

    total = len(job.chunks)
    generated = len(job.generated)
    sent = job.sent_up_to

    estado = (
        "✅ Completado" if job.finished
        else "⏳ En progreso..."
    )

    await update.message.reply_text(
        f"📖 {job.filename}\n"
        f"📄 Fragmentos generados: {generated} / {total}\n"
        f"📤 Enviados: {sent} / {total}\n"
        f"{estado}"
    )