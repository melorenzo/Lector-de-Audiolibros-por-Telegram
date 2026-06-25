import os
import logging

from tts.kokoro_engine import KokoroEngine

logger = logging.getLogger(__name__)

engine = KokoroEngine()


async def generate_audio_from_chunk(chunk, book_name, index):

    os.makedirs("app/storage/audio", exist_ok=True)

    safe_name = book_name.replace(".", "_")

    output_path = (
        f"app/storage/audio/"
        f"{safe_name}_chunk_{index}.mp3"
    )

    audio_file = await engine.synthesize(
        chunk["content"],
        output_path
    )

    return audio_file