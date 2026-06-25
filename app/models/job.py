from dataclasses import dataclass, field


@dataclass
class Job:

    filename: str

    chunks: list

    chat_id: int

    book_name: str

    generated: list = field(default_factory=list)

    current_chunk: int = 0

    sent_up_to: int = 0

    finished: bool = False