from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from schemas import MercuryEXRF, ReportDetails  # Adjust the import path as necessary
import os
import logging

class Invoice(Document, ReportDetails):
    pass

async def init():
    logging.basicConfig(level=logging.INFO)  # Optional here; Prefer setting this in your main app
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://rootuser:rootpass@localhost:27017/")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "your_database_name")  # Ensure you have this environment variable set
    logging.info("Initializing database connection...")
    try:
        client = AsyncIOMotorClient(MONGO_URL)
        await init_beanie(database=client[DATABASE_NAME], document_models=[Invoice])
        logging.info("Database connection initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing database connection: {e}")
