📖 README.md (versión limpia v0.4)

Te dejo una base lista:

# 📚 Audiobook Telegram Bot

Bot que convierte libros (PDF / EPUB) en chunks listos para audio.

---

## 🚀 Features (v0.4.0)

- 📥 Recepción de libros por Telegram
- 📄 Soporte PDF y EPUB
- 🧠 Extracción de texto automática
- 🎧 Segmentación en chunks (base para audio)
- 📊 Metadata del libro
- 🐳 Docker support

---

## ⚙️ Arquitectura


Libro → Parser → Texto → Chunk Builder → Metadata


---

## 🧩 Pipeline actual

```

PDF / EPUB
↓
Text extraction
↓
Chunk segmentation (20k chars)
↓
Telegram response

🐳 Run with Docker
docker compose up --build
📦 Tech Stack
Python 3.12
python-telegram-bot
PyMuPDF
ebooklib
BeautifulSoup4
Docker
🧠 Next version (v1.0.0)
🔊 TTS (Text to Speech)
🎧 Audio generation per chunk
📤 Audio delivery via Telegram
💾 Persistencia de libros

---

# 🧭 IMPORTANTE (esto te ordena el proyecto)

A partir de ahora tu sistema tiene 3 niveles claros:

```text id="r4"
v0.4.0 → ENTENDER LIBROS
v0.5.0 → CONVERTIR A AUDIO
v1.0.0 → ENTREGAR AUDIO COMPLETO