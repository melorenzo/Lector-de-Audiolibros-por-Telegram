from ebooklib import epub
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

MIN_DOCUMENT_CHARS = 500


def extract_text(epub_path):

    book = epub.read_epub(epub_path)

    chapters = []

    for item in book.get_items():

        if item.get_type() != 9:
            continue

        soup = BeautifulSoup(
            item.get_content(),
            "html.parser"
        )

        text = soup.get_text(separator=" ").strip()

        if len(text) < MIN_DOCUMENT_CHARS:
            continue

        chapters.append({
            "name": item.get_name(),
            "content": text
        })

    logger.info(
        f"📖 EPUB documentos extraídos: {len(chapters)}"
    )

    return {
        "chapters": chapters,
        "pages": 0
    }
