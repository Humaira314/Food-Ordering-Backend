import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def get_db():
    """Return MongoDB database instance using environment-driven URI."""
    try:
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        client = MongoClient(mongo_uri)
        # Test connection
        client.admin.command('ping')
        db_name = os.getenv("DB_NAME", "food_ordering")
        print(f"✅ MongoDB connected successfully! Database: {db_name}")
        return client[db_name]
    except ConnectionFailure as exc:
        print(f"❌ MongoDB connection failed: {exc}")
        return None
