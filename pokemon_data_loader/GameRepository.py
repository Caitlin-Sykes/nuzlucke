import logging
from DatabaseConfig import DatabaseConfig


class GameRepository:
    def __init__(self):
        self.db = DatabaseConfig()
        self.logger = logging.getLogger(__name__)

    def get_all_from(self, table):
        """Fetches all names and id from a provided table.
        :param table: The table to fetch from.
        :return: A dictionary mapping lowercase names to IDs.
        """
        self.logger.info(">> get_all_from")
        self.db.cursor.execute(f"SELECT id, name FROM {table}")
        results = self.db.cursor.fetchall()
        self.logger.debug(f"Fetched {table} from database. Result: {results}")
        self.logger.info("<< get_all_from")
        return {name.lower(): region_id for region_id, name in results}


    def upsert_game(self, name: str, ruleset_id: int, api_version_id: int, region_id: int | None):
        """
        Inserts a game or updates it if the api_version_id already exists.
        :param name: The name of the game.
        :param ruleset_id: The ruleset id of the game.
        :param api_version_id: The api version id of the game.
        :param region_id: The region id of the game.
        """
        self.logger.info(f">> upsert_game")

        self.logger.debug(f"Upserting game {name} with ruleset id {ruleset_id}, api version id {api_version_id}, region id {region_id}")
        sql = """
              INSERT INTO games (name, ruleset_id, api_version_id, region_id)
              VALUES (%s, %s, %s, %s)
              ON CONFLICT (api_version_id)
                  DO UPDATE SET
                                name = EXCLUDED.name,
                                ruleset_id = EXCLUDED.ruleset_id,
                                region_id = EXCLUDED.region_id; \
              """

        try:
            self.db.cursor.execute(sql, (name, ruleset_id, api_version_id, region_id))
            self.db.conn.commit()
            self.logger.info(f"<< upsert_game")

        except Exception as e:
                self.logger.error(f"Failed to upsert game {name}: {e}")
                self.db.conn.rollback()
                raise