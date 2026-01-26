import logging
import os
from typing import List

import requests

from utils.errors.Errors import PokeAPIError
from utils.models import GameVersion, Config
from utils.models.Poke_Models import FetchAllPokemon


class PokeApiClient:
    def __init__(self):
        self.url = Config.api.url
        self.logger = logging.getLogger(__name__)
        self.queries_dir = os.path.join(os.path.dirname(__file__), "utils", "graphql_queries")

    def _load_query(self, filename: str) -> str:
        """Reads a specific GraphQL file by name.
        :param filename: The name of the file to read.
        :returns: The contents of the file as a string."""
        path = os.path.join(self.queries_dir, filename)
        with open(path, "r") as f:
            return f.read()
    
    def fetch_all_game_versions(self) -> List[GameVersion]:
        """
        Fetches all game versions from PokeAPI to populate the local games table.
        :returns: JSON response of all game versions. See fetch_all_games.graphql for 
         the expected response structure.
        """
        self.logger.debug(">> fetch_all_game_versions")
        query = self._load_query("fetch_all_games.graphql")
        
        response = requests.post(self.url, json={'query': query})
    
        if response.status_code == 200:
            raw_data = response.json()
            # Extract the version list from the expected response structure
            version_list = raw_data.get("data", {}).get("version", [])

            # Validate using the Pydantic model 
            validated = [GameVersion(**item) for item in version_list]

            self.logger.debug(f"<< fetch_all_game_versions (Total: {len(validated)})")
            self.logger.debug(f"Versions: {validated}")
            return validated
        else:
            self.logger.error("Failed to fetch versions from PokeAPI")
            raise PokeAPIError(f"Failed to fetch versions: {response.status_code}")

    def fetch_all_pokemon_from_gen(self, version_ids: list[int], gen: int, valid_methods: list[str]) -> FetchAllPokemon:
        """
        Fetches all Pokémon from a specific generation
        :param version_ids: List of version IDs to filter by. (i.e. 1 red, 2, yellow. 
        See Constant.py for the full map)
        :param gen: Generation to filter by.
        :param valid_methods: List of valid methods to filter by.
        :returns: JSON response of all obtainable Pokémon
        from a given generation.
        See fetch_all_obtainable_pokemon.graphql for 
        the expected response structure.
        """
        self.logger.debug(">> fetch_all_pokemon_from_gen")
        query = self._load_query("fetch_all_obtainable_pokemon.graphql")
        
        payload = {
            'query': query,
            'variables': {
                'genId': gen,            # For Gen 1, this is 1
                'versionIds': version_ids,      # For Gen 1, this is [1, 2, 3]
                'validMethods': valid_methods
            }
        }
        response = requests.post(self.url, json=payload)

        if response.status_code == 200:
            raw_data = response.json()
            validated = FetchAllPokemon(**raw_data)
            
            self.logger.debug(f"<< fetch_all_pokemon_from_gen (Total: {len(validated.data.pokemon)})")
            return validated
        else:
            self.logger.error("Failed to fetch versions from PokeAPI")
            raise PokeAPIError(f"Failed to fetch versions: {response.status_code}")
        
    def fetch_pokemon_data(self, placeholder_ids: list[int]):
        """ This fetches all Pokémon placeholder data from the API
        :param placeholder_ids: List of Pokémon ids to fetch data for."""
        
        self.logger.debug(">> fetch_pokemon_data")

        query = self._load_query("fetch_placeholder_pokemon_data.graphql")

        payload = {
            'query': query,
            'variables': {
                'ids': placeholder_ids,       
            }
        }
        
        response = requests.post(self.url, json=payload)

        if response.status_code == 200:
            raw_data = response.json()
            
            validated = FetchAllPokemon(**raw_data)
        
            self.logger.debug(f"Fetched Data: {validated}")
            self.logger.debug("<< fetch_pokemon_data")
            return validated
        else:
            self.logger.error("Failed to fetch placeholder Pokemon data from PokeAPI")
            self.logger.debug("<< fetch_pokemon_data")
            raise PokeAPIError(f"Failed to fetch versions: {response.status_code}")
        
    