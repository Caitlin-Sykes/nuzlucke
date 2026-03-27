import json

from .BaseRepository import BaseRepository
from utils.Constants import GAME_METADATA


class GameRepository(BaseRepository):
    """ This class handles the games table in the database.
    It adds the games to the games table, as well as the
    region_id and ruleset_id columns."""

    def upsert_game(self, name: str, ruleset_id: int, region_id: int | None):
        """
        Inserts a game or updates it
        :param name: The name of the game.
        :param ruleset_id: The ruleset id of the game.
        :param region_id: The region id of the game.
        """
        self.logger.debug(">> upsert_game")

        self.logger.debug(f"Upserting game {name} with ruleset id {ruleset_id}, region id {region_id}")
        sql = """
              INSERT INTO games (name, ruleset_id, region_id)
              VALUES (%s, %s, %s)
              ON CONFLICT (name, ruleset_id) 
                  DO UPDATE SET
                                region_id = EXCLUDED.region_id; 
              """

        try:
            self.db.cursor.execute(sql, (name, ruleset_id, region_id))
            self.db.conn.commit()
            self.logger.debug("<< upsert_game")

        except Exception as e:
                self.logger.error(f"Failed to upsert game {name}: {e}")
                self.logger.debug("<< upsert_game")
                self.db.conn.rollback()
                raise

    def insert_game_metadata(self):
        """ This adds data to the games table that I can't get through the api
        images, release dates, etc"""
        
        self.logger.debug(">> insert_game_metadata")
        CREATOR = "Game Freak"
        RIGHTS = "Nintendo/Creatures Inc./GAME FREAK inc."
        SOURCE = "Source: Bulbapedia / Wiki Commons"
    
        sql = """
             UPDATE games
             SET release_dates = %s,
              platform = %s, 
              illustration = %s, 
              game_credits = %s,
              generations_included = %s, 
              is_dlc = %s
             WHERE name ILIKE %s;
              """

        for g in GAME_METADATA:
            img_path = f"/assets/boxart/{g['slug']}.png"
            generations_included = g['gens']
            release_dates = {
                "jp": g.get('jp'),
                "us": g.get('us'),
                "eu": g.get('eu'),
                "au": g.get('au')
            }
            illustration = {
                "image_rights": RIGHTS,
                "image_author": CREATOR,
                "image_source": SOURCE,
                "image_url": img_path
            }
            game_credits = {
                "game_creator": CREATOR,
                "game_rights": RIGHTS,
            }

            self.db.cursor.execute(sql, (
                json.dumps(release_dates),  # %s for release_dates
                g['platform'],  # %s for platform
                json.dumps(illustration),  # %s for illustration
                json.dumps(game_credits),  # %s for game_credits
                list(generations_included),  # %s for generations_included
                g['is_dlc'],  # %s for is_dlc
                g['slug']  # %s for WHERE name ILIKE
            ))
            self.db.conn.commit()
        
        self.logger.debug("<< insert_game_metadata")
