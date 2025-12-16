# db_utils.py

import psycopg2
import os

class DBConnection:
    
    def __init__(self):
        # Reading ENV vars with defaults for safety
        DB_HOST = os.getenv("DB_HOST")
        DB_NAME = os.getenv("POSTGRES_DB", "nuzlucke")
        DB_USER = os.getenv("POSTGRES_USER", "postgres")
        DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")

        try:
            self.conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            self.cursor = self.conn.cursor()
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL: {e}")
            raise

    def close(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def get_map(self, table):
        """Fetches name-to-ID map for types or abilities."""
        self.cursor.execute(f"SELECT id, name FROM {table}")
        return {name.lower(): id for id, name in self.cursor.fetchall()}

    def insert_pokemon(self, dex_num, name, slug, evolves_from):
        """Inserts a Pokémon into the Pokémon table."""
        self.cursor.execute("""
                            INSERT INTO pokemon (national_dex_number, name, slug, form_name, evolves_from_id)
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT (national_dex_number, form_name)
                                DO UPDATE SET evolves_from_id = EXCLUDED.evolves_from_id
                            RETURNING id;
                            """, (dex_num, name, slug, '', evolves_from))

        return self.cursor.fetchone()[0]

    def insert_game_stats(self, pokemon_id, ruleset_id, t1, t2, a1, a2, a3):
        """Inserts the Game Stats for different Pokémon."""
        self.cursor.execute("""
                            INSERT INTO pokemon_game_stats
                            (pokemon_id, ruleset_id, type_1_id, type_2_id, ability_1_id, ability_2_id, hidden_ability_id)
                            VALUES (%s, %s, %s, %s, %s, %s,%s)
                            ON CONFLICT (pokemon_id, ruleset_id)
                                DO NOTHING;
                            """, (pokemon_id, ruleset_id, t1, t2, a1, a2, a3))