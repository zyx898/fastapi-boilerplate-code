from datetime import datetime
import os

from core.config import settings
from core.loggerConfig import setup_logger
from database.mongodb import DatabaseManager
from database.redis import RedisManager


logger = setup_logger(__name__, settings.LOG_FILE)

def ensure_log_directory_exists():
    os.makedirs('logs', exist_ok=True)
    # Create and test if the log file is writable
    test_log_files = [
        settings.LOG_FILE,
    ]
    for log_file in test_log_files:
        with open(log_file, 'a') as f:
            f.write(f"Log file test at {datetime.now()}\n")


async def initialize_database():
    await DatabaseManager.get_client()
    logger.info("MongoDB connection successful")
    await RedisManager.get_client()
    logger.info("Redis connection successful")


async def uninitialize_database():
    await DatabaseManager.close()
    logger.info("MongoDB connection closed")
    await RedisManager.close()
    logger.info("Redis connection closed")


async def initialize_app():
    ensure_log_directory_exists()
    await initialize_database()
    logger.info("App startup complete")

async def uninitialize_app():
    await uninitialize_database()
    logger.info("App shutdown complete")