import logging
import os

from DataManager import DataManager
from repository import GameRepository, PokemonRepository, EncounterRepository, SyncStateRepository
from PokeApiClient import PokeApiClient
from utils.models import Config

def setup_logging():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(base_dir, Config.logging.logging_file_name)
    logging.basicConfig(filename=str(log_path), level=Config.logging.logging_level,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)
    
    client = PokeApiClient()
    game_repo = GameRepository()
    poke_repo = PokemonRepository()
    encounter_repo = EncounterRepository()
    sync_repo = SyncStateRepository()
    
    manager = DataManager(api_client=client, game_repo=game_repo, poke_repo=poke_repo, encounter_repo=encounter_repo, sync_repo=sync_repo)


    logger.info("Starting the Pokemon Game Sync...")
    manager.sync_pokemon_games()
    logger.info("Syncing Pokemon Games completed successfully!")
    
    logger.info("Starting the Pokemon Info Sync...")
    manager.sync_pokemon_info()
    logger.info("Syncing Pokemon Info completed successfully!")
    
    logger.info("Starting the Pokemon Encounter Sync...")
    manager.sync_pokemon_encounters()
    logger.info("Syncing Pokemon Encounters completed successfully!")
    logger.info("")
