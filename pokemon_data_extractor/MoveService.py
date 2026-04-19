import logging
import requests
import DatabaseConfig

class MoveService:
    """Handles checking the DB for moves and falling back to PokeAPI."""
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_moves(self, pokemon_slug, game_slug, level):
        """ Gets moves from the database and caches them if not present
        :param pokemon_slug: The slug of the Pokemon
        :param game_slug: The slug of the game
        :param level: The level of the move
        :return: list of moves from the database, or the API if the database is empty"""

        self.logger.debug(f">> get_moves: {pokemon_slug} ({game_slug}) at level {level}")

        conn = DatabaseConfig.Database.get_connection()
        cursor = conn.cursor()

        #Check local database cache
        cursor.execute(
            "SELECT move_name, level_learned FROM pokemon_learnsets WHERE pokemon_slug = %s AND game_slug = %s",
            (pokemon_slug, game_slug))
        data = cursor.fetchall()

        # 2. API Fallback if DB is empty
        if not data:
            try:
                self.logger.info(f"Fetching API data for {pokemon_slug} ({game_slug})...")

                # TODO: make neater
                if pokemon_slug == "farfetch-d":
                    pokemon_slug="farfetchd"

                resp = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_slug}")
                resp.raise_for_status()
                api_data = resp.json()

                for move_item in api_data['moves']:
                    for detail in move_item['version_group_details']:
                        if detail['version_group']['name'] == game_slug and detail['move_learn_method']['name'] == 'level-up':
                            m_name = move_item['move']['name']
                            m_lvl = detail['level_learned_at']
                            cursor.execute(
                                "INSERT INTO pokemon_learnsets (pokemon_slug, game_slug, move_name, level_learned) VALUES (%s, %s, %s, %s)",
                                (pokemon_slug, game_slug, m_name, m_lvl))
                            data.append((m_name, m_lvl))
                conn.commit()
            except Exception as e:
                self.logger.error(f"API Error for {pokemon_slug}: {e}")

        #Filter top 4 moves by level
        learned = [m for m in data if m[1] <= level]
        learned.sort(key=lambda x: x[1], reverse=True)

        self.logger.debug(f"<< get_moves")
        return [m[0] for m in learned[:4]]