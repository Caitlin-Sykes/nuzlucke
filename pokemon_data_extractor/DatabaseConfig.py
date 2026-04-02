import os
import logging
from pathlib import Path
from dotenv import load_dotenv
import psycopg2

logger = logging.getLogger(__name__)

# --- Path Logic ---
# Get the directory of the current file (pokemon_data_extractor)
current_file = Path(__file__).resolve()
# .parent gets 'pokemon_data_extractor',
# .parent.parent gets 'Java/Nuzlucke'
project_root = current_file.parent.parent

# Define the path to the .env file
env_path = project_root / ".env"

# Load the environment variables
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    logger.info(f"Loaded environment variables from {env_path}")
else:
    logger.warning(f"Could not find .env file at {env_path}")

class Database:
    _instance = None

    @classmethod
    def get_connection(cls):
        if cls._instance is None or cls._instance.closed:
            try:
                # Read from os.environ (populated by load_dotenv)
                cls._instance = psycopg2.connect(
                    host=os.getenv("DB_HOST", "localhost"),
                    database=os.getenv("POSTGRES_DB"),
                    user=os.getenv("POSTGRES_USER"),
                    password=os.getenv("POSTGRES_PASSWORD"),
                )
                cls._instance.autocommit = True
                logger.info("Database connection established.")
            except Exception as e:
                logger.error(f"Failed to connect to DB: {e}")
                raise
        return cls._instance