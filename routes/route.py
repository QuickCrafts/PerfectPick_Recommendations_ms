from fastapi import APIRouter
from models.recommendations import ItemRemovalModel, RecommendationModel, RecommendationUpdateModel
from config.database import collection_name
from recommendationModels.book_recommender import get_book_ids, get_book_titles, recommend_books
from recommendationModels.movie_recommender import get_movie_ids, get_movie_titles, recommend_movies
from schema.schemas import list_serial
from bson import ObjectId
from fastapi import HTTPException
import json

router = APIRouter()

# GET Request Method for specific user's recommendation
@router.get("/recommendation/{id_user}")
async def get_recommendation_for_user(id_user: int):
    recommendation = list_serial(collection_name.find({"id_user": id_user}))
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return recommendation


# POST Request Method to create a new recommendation
@router.post("/recommendation/")
async def create_recommendation(recommendation: RecommendationModel):
    user_id = recommendation.id_user
    liked_movie_ids = recommendation.movies
    liked_book_ids = recommendation.books
    liked_song_ids = recommendation.songs

    existing_recommendation = collection_name.find_one({"id_user": user_id})

    movie_titles = get_movie_titles(liked_movie_ids)
    recommended_movies = []
    for title in movie_titles:
        recommended_movies.extend(recommend_movies(title))
    recommended_movies = list(set(recommended_movies))
    recommended_movie_ids = get_movie_ids(recommended_movies)

    book_titles = get_book_titles(liked_book_ids)
    recommended_books = []
    for title in book_titles:
        recommended_books.extend(recommend_books(title))
    recommended_books = list(set(recommended_books))
    recommended_book_ids = get_book_ids(recommended_books)

    recommended_song_ids = []

    recommendation_data = {
        "id_user": user_id,
        "movies": recommended_movie_ids,
        "books": recommended_book_ids,
        "songs": recommended_song_ids,
    }

    if existing_recommendation:
        collection_name.update_one(
            {"id_user": user_id},
            {"$set": recommendation_data}
        )
        return {"data": "Recommendation updated successfully"}
    else:
        collection_name.insert_one(recommendation_data)
        return {"data": "Recommendation added successfully"}

# PUT Request Method to update a recommendation for a specific user
@router.put("/recommendation/{id_user}")
async def update_recommendation_for_user(id_user: int, recommendation: RecommendationUpdateModel):
    updated_recommendation = {k: v for k, v in recommendation.model_dump(exclude_unset=True).items() if v is not None}
    collection_name.update_one({"id_user": id_user}, {"$set": updated_recommendation})
    return {"data": "Recommendation updated successfully"}


# DELETE Request Method to delete all the recommendatios for a specific user
@router.delete("/recommendation/{id_user}")
async def delete_recommendation(id_user: int):
    collection_name.delete_one({"id_user": id_user})
    return {
        "data": "recommendation deleted successfully"
    }

# PUT Request Method to remove an item from a user's recommendation, to be used after a user likes an item from the recommendation list
@router.put("/recommendation/remove/{id_user}")
async def remove_item_from_recommendation(id_user: int, removal_info: ItemRemovalModel):
    if removal_info.section not in ["movies", "books", "songs"]:
        raise HTTPException(status_code=400, detail="Invalid section specified")

    update_result = collection_name.update_one(
        {"id_user": id_user},
        {"$pull": {removal_info.section: removal_info.id_to_remove}}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found or item not in list")
    
    return {"message": "Item removed successfully"}