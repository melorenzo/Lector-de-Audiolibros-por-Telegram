import os


async def save_book(document):

    filename = document.file_name

    if not filename.lower().endswith((".pdf", ".epub")):
        return False, "❌ Solo acepto PDF o EPUB."

    os.makedirs("app/storage/books", exist_ok=True)

    telegram_file = await document.get_file()

    destination = f"app/storage/books/{filename}"

    await telegram_file.download_to_drive(destination)

    print(f"📚 Libro guardado: {destination}")

    return True, filename