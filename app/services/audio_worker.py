import logging

from services.audio_service import generate_audio_from_chunk
from services.job_manager import update_job

logger = logging.getLogger(__name__)


async def process_job(job, bot, chat_id):

    logger.info(
        f"🎧 Comenzando trabajo {job.filename}"
    )

    while job.current_chunk < len(job.chunks):

        chunk = job.chunks[job.current_chunk]

        audio_path = await generate_audio_from_chunk(
            chunk,
            job.book_name,
            chunk["index"]
        )

        job.generated.append(audio_path)

        if audio_path:

            logger.info(
                f"✅ Chunk {chunk['index']} generado"
            )

            if chunk["index"] == 0:

                try:
                    await bot.send_audio(
                        chat_id=chat_id,
                        audio=open(audio_path, "rb"),
                        caption=(
                            f"🎧 Fragmento 1 de {len(job.chunks)} "
                            f"— {job.filename}\n\n"
                            "Usa /next para recibir más "
                            "(hasta 10 por vez)."
                        )
                    )
                    job.sent_up_to = 1

                except Exception as e:
                    logger.error(
                        f"Error enviando primer chunk: {e}"
                    )

        job.current_chunk += 1
        update_job(job)

    job.finished = True
    update_job(job)

    logger.info(
        f"🏁 Trabajo terminado {job.filename}"
    )

    try:
        await bot.send_message(
            chat_id=chat_id,
            text=(
                f"✅ Todos los fragmentos de "
                f"'{job.filename}' han sido generados.\n"
                "Usa /next para recibirlos."
            )
        )
    except Exception as e:
        logger.error(
            f"Error notificando finalización: {e}"
        )