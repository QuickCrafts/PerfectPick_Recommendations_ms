from fastapi import APIRouter
from models.recommendations import ItemRemovalModel, RecommendationModel, RecommendationUpdateModel
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId
from fastapi import HTTPException

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
    collection_name.insert_one(dict(recommendation))
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