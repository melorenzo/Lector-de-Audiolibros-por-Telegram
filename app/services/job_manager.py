from models.job import Job

jobs = {}


def create_job(filename, chunks, chat_id, book_name):

    job = Job(
        filename=filename,
        chunks=chunks,
        chat_id=chat_id,
        book_name=book_name
    )

    jobs[chat_id] = job

    return job


def get_job(chat_id):

    return jobs.get(chat_id)


def delete_job(chat_id):

    jobs.pop(chat_id, None)


def list_jobs():

    return jobs