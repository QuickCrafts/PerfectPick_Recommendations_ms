from pydantic import BaseModel
from typing import List

class Recommendation(BaseModel):
    id_user: int
    movies: List[str]
    books: List[str]
    songs: List[str]
    created_at: str