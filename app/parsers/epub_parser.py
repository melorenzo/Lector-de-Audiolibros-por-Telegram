from ebooklib import epub
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


def extract_text(epub_path):

    book = epub.read_epub(epub_path)

    text = ""

    for item in book.get_items():

        if item.get_type() == 9:

            soup = BeautifulSoup(
                item.get_content(),
                "html.parser"
            )

            text += soup.get_text(separator=" ")

    logger.info(
        f"📝 EPUB caracteres extraídos: {len(text)}"
    )

    return {
        "text": text,
        "pages": 0
    }