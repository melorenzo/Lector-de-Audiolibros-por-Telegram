import json
import sqlite3
import logging
import os

from models.job import Job

logger = logging.getLogger(__name__)

DB_PATH = "app/storage/metadata/jobs.db"


def _get_connection():

    os.makedirs(
        os.path.dirname(DB_PATH),
        exist_ok=True
    )

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = _get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            chat_id INTEGER PRIMARY KEY,
            filename TEXT NOT NULL,
            book_name TEXT NOT NULL,
            chunks TEXT NOT NULL,
            generated TEXT NOT NULL DEFAULT '[]',
            current_chunk INTEGER NOT NULL DEFAULT 0,
            sent_up_to INTEGER NOT NULL DEFAULT 0,
            finished INTEGER NOT NULL DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

    logger.info("🗄️ Base de datos inicializada")


def save_job(job):

    conn = _get_connection()

    conn.execute("""
        INSERT OR REPLACE INTO jobs
            (chat_id, filename, book_name, chunks,
             generated, current_chunk, sent_up_to, finished)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        job.chat_id,
        job.filename,
        job.book_name,
        json.dumps(job.chunks),
        json.dumps(job.generated),
        job.current_chunk,
        job.sent_up_to,
        1 if job.finished else 0
    ))

    conn.commit()
    conn.close()


def delete_job(chat_id):

    conn = _get_connection()

    conn.execute(
        "DELETE FROM jobs WHERE chat_id = ?",
        (chat_id,)
    )

    conn.commit()
    conn.close()


def load_all_jobs():

    conn = _get_connection()

    rows = conn.execute(
        "SELECT * FROM jobs"
    ).fetchall()

    conn.close()

    jobs = {}

    for row in rows:

        job = Job(
            filename=row["filename"],
            chunks=json.loads(row["chunks"]),
            chat_id=row["chat_id"],
            book_name=row["book_name"],
            generated=json.loads(row["generated"]),
            current_chunk=row["current_chunk"],
            sent_up_to=row["sent_up_to"],
            finished=bool(row["finished"])
        )

        jobs[row["chat_id"]] = job

    return jobs
