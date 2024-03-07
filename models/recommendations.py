from pydantic import BaseModel

class Recommendation(BaseModel):
    id_user: int
    movies: str
    books: str
    songs: str
    created_at: str