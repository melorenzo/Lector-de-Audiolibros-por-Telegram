@echo off
echo ==========================
echo Creando estructura proyecto
echo ==========================
echo.

REM Carpetas

mkdir app 2>nul
mkdir app\bot 2>nul
mkdir app\parsers 2>nul
mkdir app\tts 2>nul
mkdir app\services 2>nul
mkdir app\models 2>nul
mkdir app\storage 2>nul
mkdir app\storage\books 2>nul
mkdir app\storage\audio 2>nul

REM Archivos Python

type nul > app\__init__.py

type nul > app\bot\__init__.py
type nul > app\bot\handlers.py
type nul > app\bot\commands.py

type nul > app\parsers\__init__.py
type nul > app\parsers\pdf_parser.py
type nul > app\parsers\epub_parser.py

type nul > app\tts\__init__.py
type nul > app\tts\kokoro_engine.py

type nul > app\services\__init__.py
type nul > app\services\book_service.py
type nul > app\services\audio_service.py

type nul > app\models\__init__.py
type nul > app\models\database.py

type nul > app\main.py

REM Archivos raíz

type nul > .env
type nul > .env.example
type nul > requirements.txt
type nul > Dockerfile
type nul > docker-compose.yml
type nul > README.md
type nul > .gitignore

REM Gitkeep

type nul > app\storage\books\.gitkeep
type nul > app\storage\audio\.gitkeep

echo python-telegram-bot >> requirements.txt
echo python-dotenv >> requirements.txt
echo.
echo ==========================
echo Estructura creada
echo ==========================
pause