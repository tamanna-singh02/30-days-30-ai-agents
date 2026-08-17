from pydantic import BaseModel


class WordCountArgs(BaseModel):
    text: str


def word_count(text: str) -> str:

    count = len(text.split())

    return str(count)