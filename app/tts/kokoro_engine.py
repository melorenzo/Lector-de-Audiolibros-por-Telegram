import edge_tts
import logging

logger = logging.getLogger(__name__)


class KokoroEngine:
    """
    Motor TTS (backend actual: edge-tts).
    """

    def __init__(self, voice="es-MX-JorgeNeural"):
        self.voice = voice

    async def synthesize(self, text: str, output_path: str):

        if not text.strip():
            logger.warning("Texto vacío, no se genera audio.")
            return None

        try:
            communicate = edge_tts.Communicate(
                text,
                self.voice
            )

            await communicate.save(output_path)

            logger.info(
                f"🔊 Audio generado | path={output_path}"
            )

            return output_path

        except Exception as e:
            logger.error(
                f"Error TTS: {str(e)}"
            )
            return None