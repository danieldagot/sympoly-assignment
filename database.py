from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.invoiceModelDetailed import  DetailedReportDetails 
  # Adjust the import path as necessary
import os
import logging

class Invoice(Document, DetailedReportDetails):
    pass

async def init():
    logging.basicConfig(level=logging.INFO)  # Optional here; Prefer setting this in your main app
    MONGO_URL = create_mongo_url() 
    DATABASE_NAME = os.getenv("DATABASE_NAME", "your_database_name")  # Ensure you have this environment variable set
    logging.info("Initializing database connection...")
    try:
        client = AsyncIOMotorClient(MONGO_URL)
        await init_beanie(database=client[DATABASE_NAME], document_models=[Invoice])
        logging.info("Database connection initialized successfully.")
    except Exception as e:
        logging.CRITICAL(f"Error initializing database connection: {e}")


def create_mongo_url():
    user_name = os.getenv("MONGO_USER", "rootuser") 
    password = os.getenv("MONGO_PASS", "rootpass")
    host = os.getenv("MONGO_HOST", "localhost")
    port = os.getenv("MONGO_PORT", "27017")
    MONGO_URL = f"mongodb://{user_name}:{password}@{host}:{port}/"
    return MONGO_URL