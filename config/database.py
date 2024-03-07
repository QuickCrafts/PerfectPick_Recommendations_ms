from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(f"mongodb+srv://{DB_USER}:{DB_PASS}@perfectpick-recommendat.eic4adp.mongodb.net/?retryWrites=true&w=majority&appName=PerfectPick-Recommendations-MS")
db = client[DB_NAME]



collection_name = db['recommendation_collection']