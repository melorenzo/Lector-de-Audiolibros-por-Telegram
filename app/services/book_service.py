import os
import logging

from parsers.pdf_parser import extract_text

logger = logging.getLogger(__name__)


async def save_book(document):

    filename = document.file_name

    if not filename.lower().endswith((".pdf", ".epub")):
        logger.warning(
            f"Archivo rechazado | nombre={filename}"
        )
        return False, "❌ Solo acepto PDF o EPUB."

    os.makedirs("app/storage/books", exist_ok=True)

    telegram_file = await document.get_file()

    destination = f"app/storage/books/{filename}"

    await telegram_file.download_to_drive(destination)

    logger.info(
        f"📚 Libro guardado | nombre={filename} | ruta={destination}"
    )

    text = ""
    pages = 0

    if filename.lower().endswith(".pdf"):

        pdf_data = extract_text(destination)

        text = pdf_data["text"]
        pages = pdf_data["pages"]

        logger.info(
            f"📖 Texto extraído | paginas={pages} | caracteres={len(text)}"
        )

    return True, {
        "filename": filename,
        "pages": pages,
        "text_length": len(text)
    }