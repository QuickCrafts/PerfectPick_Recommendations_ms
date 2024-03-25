from pydantic import BaseModel, Field
from typing import List, Optional

class RecommendationModel(BaseModel):
    id_user: int
    movies: List[str]  
    books: List[int]  
    songs: List[int]
 

class RecommendationUpdateModel(BaseModel):
    movies: Optional[List[str]] = Field(None)
    books: Optional[List[int]] = Field(None)
    songs: Optional[List[int]] = Field(None)

class ItemRemovalModel(BaseModel):
    section: str 
    id_to_remove: int