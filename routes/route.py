from fastapi import APIRouter
from models.recommendations import ItemRemovalModel, RecommendationModel, RecommendationUpdateModel
from config.database import collection_name
from recommendationModels.movie_recommender import recommend_movies
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




def get_movie_title_from_json(movie_id):
    # Load the movie data from the JSON file
    with open("C:/Users/dmriv/Documents/GitHub/PerfectPick_Recommendations_ms/recommendationModels/movies.json") as file:
        movie_data = json.load(file)
    
    # Search for the movie with the given ID
    for movie in movie_data:
        if movie["id_movie"] == movie_id:
            return movie["title"]
    
    # If the movie ID is not found, return None or raise an exception
    return None

def get_movie_titles(movie_ids):
    movie_titles = []
    for movie_id in movie_ids:
        # Retrieve the movie title based on the movie ID from your JSON file
        movie_title = get_movie_title_from_json(movie_id)
        movie_titles.append(movie_title)
    return movie_titles

def get_movie_ids(movie_titles):
    movie_ids = []
    for movie_title in movie_titles:
        # Retrieve the movie ID based on the movie title from your JSON file
        movie_id = get_movie_id_from_json(movie_title)
        movie_ids.append(movie_id)
    return movie_ids

def get_movie_id_from_json(movie_title):
    # Load the movie data from the JSON file
    with open("C:/Users/dmriv/Documents/GitHub/PerfectPick_Recommendations_ms/recommendationModels/movies.json") as file:
        movie_data = json.load(file)
    
    # Search for the movie with the given title
    for movie in movie_data:
        if movie["title"] == movie_title:
            return movie["id_movie"]
    
    # If the movie title is not found, return None or raise an exception
    return None

# POST Request Method to create a new recommendation
@router.post("/recommendation/")
async def create_recommendation(recommendation: RecommendationModel):
    print
    user_id = recommendation.id_user
    liked_movie_ids = recommendation.movies
    liked_book_ids = recommendation.books
    liked_song_ids = recommendation.songs

    movie_titles = get_movie_titles(liked_movie_ids)

    recommended_movies = []
    for title in movie_titles:
        recommended_movies.extend(recommend_movies(title))

    recommended_movies = list(set(recommended_movies))

    recommended_movie_ids = get_movie_ids(recommended_movies)

    recommended_book_ids = []
    recommended_song_ids = []

    recommendation_data = {
        "id_user": user_id,
        "movies": recommended_movie_ids,
        "books": recommended_book_ids,
        "songs": recommended_song_ids,

    }

    collection_name.insert_one(recommendation_data)
    return {
        "data": "recommendation added successfully"
    }


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