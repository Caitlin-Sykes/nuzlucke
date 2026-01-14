import logging
import os

from DataManager import DataManager
from GameRepository import GameRepository
from PokeApiClient import PokeApiClient
from utils.models import Config

def setup_logging():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(base_dir, Config.logging.logging_file_name)
    logging.basicConfig(filename=log_path, level=Config.logging.logging_level,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)
    
    client = PokeApiClient()
    game_repo = GameRepository()
    
    manager = DataManager(api_client=client, game_repo=game_repo)

    logger.info("Starting the Pokemon Game Sync...")
    manager.sync_pokemon_games()
    logger.info("Sync completed successfully!")