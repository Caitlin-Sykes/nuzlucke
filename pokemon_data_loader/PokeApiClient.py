import logging
import os
from typing import List

import requests

from utils.errors.Errors import PokeAPIError
from utils.models import GameVersion, Config


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
        :returns: JSON response of all game versions
        """
        self.logger.info(">> fetch_all_game_versions")
        query = self._load_query("fetch_all_games.graphql")
        
        response = requests.post(self.url, json={'query': query})
    
        if response.status_code == 200:
            raw_data = response.json()
            # Extract the version list from the expected response structure
            version_list = raw_data.get("data", {}).get("version", [])

            # Validate using the Pydantic model 
            validated = [GameVersion(**item) for item in version_list]

            self.logger.info(f"<< fetch_all_game_versions (Total: {len(validated)})")
            self.logger.debug(f"Versions: {validated}")
            return validated
        else:
            self.logger.error("Failed to fetch versions from PokeAPI")
            raise PokeAPIError(f"Failed to fetch versions: {response.status_code}")