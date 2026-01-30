from BaseRepository import BaseRepository

class GameRepository(BaseRepository):
    """ This class handles the games table in the database.
    It adds the games to the games table, as well as the
    region_id and ruleset_id columns."""

    def upsert_game(self, name: str, ruleset_id: int, api_version_id: int, region_id: int | None):
        """
        Inserts a game or updates it if the api_version_id already exists.
        :param name: The name of the game.
        :param ruleset_id: The ruleset id of the game.
        :param api_version_id: The api version id of the game.
        :param region_id: The region id of the game.
        """
        self.logger.debug(">> upsert_game")

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
            self.logger.debug("<< upsert_game")

        except Exception as e:
                self.logger.error(f"Failed to upsert game {name}: {e}")
                self.logger.debug("<< upsert_game")
                self.db.conn.rollback()
                raise
