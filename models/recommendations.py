from pydantic import BaseModel, Field
from typing import List, Optional

class RecommendationModel(BaseModel):
    id_user: int
    movies: List[int]  
    books: List[int]  
    songs: List[int]
    created_at: str

class RecommendationUpdateModel(BaseModel):
    movies: Optional[List[int]] = Field(None)
    books: Optional[List[int]] = Field(None)
    songs: Optional[List[int]] = Field(None)
    created_at: Optional[str] = Field(None)

class ItemRemovalModel(BaseModel):
    section: str 
    id_to_remove: int