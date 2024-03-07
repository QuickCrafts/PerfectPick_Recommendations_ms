from fastapi import APIRouter
from models.recommendations import Recommendation
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()

# GET Request Method
@router.get("/")
async def get_all_recommendations():
    recommendations = list_serial(collection_name.find())
    return recommendations


# POST Request Method
@router.post("/")
async def post_recommendation(recommendation: Recommendation):
    collection_name.insert_one(dict(recommendation))
    return {
        "data": "recommendation added successfully"
    }

""" 

# PUT Request Method
@router.put("/{id}")
async def update_recommendation(id: str, recommendation: R):
    collection_name.update_one({"_id": ObjectId(id)}, {"$set": dict(recommendation)})
    return {
        "data": "recommendation updated successfully"
    }
 

# DELETE Request Method
@router.delete("/{id}")
async def delete_recommendation(id: str):
    collection_name.delete_one({"_id": ObjectId(id)})
    return {
        "data": "recommendation deleted successfully"
    }

 """