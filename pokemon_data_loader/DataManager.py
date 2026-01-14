import logging

import GameRepository
import PokeApiClient
from utils.Constants import group_to_ruleset
from utils.models import GameVersion


class DataManager:

    def __init__(self, api_client: PokeApiClient, game_repo: GameRepository):
        self.api_client = api_client
        self.game_repo = game_repo
        self.logger = logging.getLogger(__name__)
        
    def sync_pokemon_games(self):
        """
        Processes game versions, applies region overrides, 
        and saves them to the database.
       """

        self.logger.info(">> sync_pokemon_games")
        
        # Gets all the games and their regions from the api
        games = self.api_client.fetch_all_game_versions()

        # Gets all the pre-existing regions from the db.
        region_map = self.game_repo.get_all_from('regions')
        
        for game in games:
            # Get the region name from the api response.
            region_name = self._resolve_region_name(game)
            
            # Gets the id of the region by looking up the region from the response to the list in the db
            region_id = region_map.get(region_name) if region_name else None

            # Gets the ruleset id from the group_to_ruleset dict
            ruleset_id = group_to_ruleset.get(game.version_group_id)
            
            # If the game has a ruleset
            if ruleset_id is not None:
                self.game_repo.upsert_game(game.name, ruleset_id, game.id, region_id)
                self.logger.debug(f"Upserted game {game.name} with ruleset id {ruleset_id}, api version id {game.id}, region id {region_id}")
            else:
                self.logger.warning(f"Skipping game {game.name} as it has no ruleset.")

        self.logger.info("<< sync_pokemon_games")



    """ 
    ----------------------------------------
    Helper Functions
    ----------------------------------------
    """
    def _resolve_region_name(self, version: GameVersion) -> str | None:
        """Internal helper to handle the logic for missing API regions.
            :param version: GameVersion object from the api response
            :returns: region name as string or None if not found."""

        self.logger.info(">> _resolve_region_name")
        # Checks the api response for the region name.
        if version.versiongroup.versiongroupregions:
            return version.versiongroup.versiongroupregions[0].region.name
    
        # Overrides for games that don't have a region in the api response.
        overrides = {
            'xd': 'orre',
            'colosseum': 'orre',
            'legends-za': 'kalos',
            'mega-dimension': 'kalos'
        }
    
        if version.name in overrides:
            self.logger.info("<< _resolve_region_name")
            return overrides[version.name]
    
        self.logger.warning(f"No region found for {version.name}. Defaulting to None.")
        self.logger.info("<< _resolve_region_name")

        return None