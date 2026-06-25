import logging

from models.job import Job
from models.database import (
    save_job as db_save,
    delete_job as db_delete,
    load_all_jobs
)

logger = logging.getLogger(__name__)

jobs = {}


def load_jobs():

    global jobs

    jobs = load_all_jobs()

    logger.info(
        f"🗄️ Cargados {len(jobs)} jobs de la base de datos"
    )


def create_job(filename, chunks, chat_id, book_name):

    job = Job(
        filename=filename,
        chunks=chunks,
        chat_id=chat_id,
        book_name=book_name
    )

    jobs[chat_id] = job
    db_save(job)

    return job


def get_job(chat_id):

    return jobs.get(chat_id)


def delete_job(chat_id):

    jobs.pop(chat_id, None)
    db_delete(chat_id)


def update_job(job):

    db_save(job)


def list_jobs():

    return jobs