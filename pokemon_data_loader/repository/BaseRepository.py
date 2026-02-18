import logging
from typing import Any

from DatabaseConfig import DatabaseConfig
from utils.errors.Errors import FailedToCreateAbilityError


class BaseRepository:
    """Parent class providing shared database access logic."""
    def __init__(self):
        self.db = DatabaseConfig()
        self.logger = logging.getLogger(self.__class__.__name__)
        self._type_map = self.get_all_from("types")
        self._ability_map = self.get_all_from("abilities")
    
    def get_all_from(self, table):
        """Fetches all names and id from a provided table.
        :param table: The table to fetch from.
        :return: A dictionary mapping lowercase names to IDs.
        """
        self.logger.debug(">> get_all_from")
        self.db.cursor.execute(f"SELECT id, name FROM {table}")
        results = self.db.cursor.fetchall()
        self.logger.debug(f"Fetched {table} from database. Result: {results}")
        self.logger.debug("<< get_all_from")
        return {name.lower(): region_id for region_id, name in results}


    def get_or_create_ability(self, name: str, flavor_text: str = None) -> Any | None:
        """Finds an ability by name or creates it if it doesn't exist.
        :param name: The name of the ability to find or create.
        :param flavor_text: The flavour text of the ability.
        :return: The ID of the ability, or None if it couldn't be found or created."""
        self.logger.debug(">> get_or_create_ability")
        
        name_lower = name.lower()
        
        #Check if it already exists
        if name_lower in self._ability_map:
            self.logger.debug("<< get_or_create_ability")
            return self._ability_map[name_lower]

        # If it's not in the db, add it
        self.logger.debug(f"Ability '{name}' not found. Adding to database...")
        try:
            query = """
                    INSERT INTO abilities (name, description)
                    VALUES (%s, %s)
                    ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
                    RETURNING id; \
                    """
            self.db.cursor.execute(query, (name.title(), flavor_text))
            new_id = self.db.cursor.fetchone()[0]

            # update the local map
            self._ability_map[name_lower] = new_id
            self.logger.debug("<< get_or_create_ability")
            return new_id
        except Exception:
            raise FailedToCreateAbilityError
            return None
