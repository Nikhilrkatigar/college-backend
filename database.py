from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise RuntimeError("MONGO_URL is not set")

client = MongoClient(MONGO_URL)

# Specify database name (can be customized via environment variable)
DB_NAME = os.getenv("DB_NAME", "college_scraper")
db = client[DB_NAME]

progress_collection = db["scrape_progress"]
pagination_collection = db["scrape_pagination"]
users_collection = db["users"]
colleges_collection = db["colleges"]
contacts_collection = db["contacts"]
logs_collection = db["activity_logs"]