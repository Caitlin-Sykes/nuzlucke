from pickle import TUPLE2

from pydantic_core.core_schema import IncExDictSerSchema

from BaseRepository import BaseRepository
from utils.models.Poke_Models import Pokemon


class PokemonRepository(BaseRepository):
    def upsert_pokemon_data(self, pokemon: "Pokemon", ruleset_id: int):
        """Handles the insertion of a Pokémon and its version-specific encounter data.
        :param ruleset_id: The ruleset ID to insert data for.
        :param pokemon: The Pokémon object to insert.
        """
        self.logger.debug(">> upsert_pokemon_data")

        try:
            self.logger.debug(f"Saving data for {pokemon.name} (ID: {pokemon.id})")
            
            evolves_from_id = pokemon.pokemonspecy.evolves_from_species_id
            
            # If it exists, check the thing it evolves from exists in the db
            if evolves_from_id:
                self.logger.debug(f"Checking if evolves_from_id ({evolves_from_id}) exists in the database.")
                self.db.cursor.execute("SELECT id FROM pokemon WHERE id = %s", (evolves_from_id,))
                result = self.db.cursor.fetchone()
            
                # if it can't be found, insert a placeholder
                if not result:
                    self.logger.warning(
                        f"Parent species with ID {evolves_from_id} not found. Inserting placeholder record."
                    )
                    # Insert placeholder for the parent Pokémon
                    placeholder_query = """
                                        INSERT INTO pokemon (id, name, national_dex_number, slug, form_name, is_official_form)
                                        VALUES (%s, %s, %s, %s, %s, %s)
                                        ON CONFLICT (id) DO NOTHING; \
                                        """
                    self.db.cursor.execute(
                        placeholder_query,
                        (evolves_from_id, f"placeholder-{evolves_from_id}", -1, None, None, False),
                    )
                    self.db.conn.commit()
                    
            # Inserts into the Pokémon table,
            # these are generally things that do not change per generation
            pokemon_query = """
                            INSERT INTO pokemon (
                                id, name, national_dex_number, slug, form_name, is_official_form, evolves_from_id
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (id) DO UPDATE SET
                                                           name = EXCLUDED.name,
                                                           national_dex_number = EXCLUDED.national_dex_number,
                                                           slug = EXCLUDED.slug,
                                                           form_name = EXCLUDED.form_name,
                                                           is_official_form = EXCLUDED.is_official_form,
                                                           evolves_from_id = EXCLUDED.evolves_from_id; \
                            """
            self.db.cursor.execute(pokemon_query, (
                pokemon.id,                              
                pokemon.clean_name,                       
                pokemon.pokemonspecy.national_dex_number,  
                pokemon.raw_name,                        
                pokemon.form_label,                        
                True,                                 
                pokemon.pokemonspecy.evolves_from_species_id 
            ))

            t1, t2 = self._get_validate_types(pokemon.types, ruleset_id)
         

            a1 = self._get_ability_id_from_slot(pokemon.pokemonabilities, 1)
            a2 = self._get_ability_id_from_slot(pokemon.pokemonabilities, 2)
            hidden = self._get_ability_id_from_slot(pokemon.pokemonabilities, 3)
            self.logger.debug(f"Abilities: {a1}/{a2}/{hidden}")
            
            # We insert a copy of the stats per Pokémon, per generation
            # As there may be changes in types, etc., per generation
            # Example: Clefairy being normal in Gen 1, but Fairy in Gen 6
            stats_query = """
                          INSERT INTO pokemon_game_stats (
                              pokemon_id, ruleset_id,
                              type_1_id, type_2_id,
                              ability_1_id, ability_2_id, hidden_ability_id
                          )
                          VALUES (%s, %s, %s, %s, %s, %s, %s)
                          ON CONFLICT (pokemon_id, ruleset_id) DO UPDATE SET
                                                                             type_1_id = EXCLUDED.type_1_id,
                                                                             type_2_id = EXCLUDED.type_2_id; \
                          """

            self.db.cursor.execute(stats_query, (
                pokemon.id,
                ruleset_id,  
                t1, t2,
                a1, a2, hidden
            ))

            self.db.conn.commit()

        except Exception as e:
            self.db.conn.rollback()
            self.logger.error(f"Failed to save {pokemon.name}: {e}")
            raise
        self.logger.debug("<< upsert_pokemon_data")
    
    def upsert_evolutions_links(self):
        """ This function gets the placeholder ids from the db
        and updates with the correct information
        """
      
    
    """
     ----------------------------------------
     Helper Functions
     ----------------------------------------
     """
    def _get_ability_id_from_slot(self, abilities, slot):
        """Helper to find or create ability ID from the slot data.
        :param: abilities: List of ability slots
        :param: slot: The slot number to check
        :returns: The ability ID for the slot, or None if not found.
        """

        self.logger.debug(">> _get_ability_id_from_slot")
        
        match = next((a for a in abilities if a.slot == slot), None)
        if not match:
            self.logger.info("<< _get_ability_id_from_slot")
            return None
    
        ability_name = match.ability.name
        flavor_text = ""
        if match.ability.abilityflavortexts:
            flavor_text = match.ability.abilityflavortexts[0].flavor_text
        
        self.logger.info("<< _get_ability_id_from_slot")
        return self.get_or_create_ability(ability_name, flavor_text)

    def _get_validate_types(self, types_data, ruleset_id):
        """Helper to validate the types.
        :param types_data: The Pokémon types data to validate.
        :param ruleset_id: The ruleset ID to validate for/the generation to use.
        :returns: A tuple of type IDs."""
    
        self.logger.info(">> _get_validate_types")
    
        if not types_data:
            self.logger.warning("No types found for this Pokémon. Defaulting to None.")
            return None, None
    
        t1 = self._type_map.get(types_data[0].type.name.lower())
        t2 = self._type_map.get(types_data[1].type.name.lower()) if len(types_data) > 1 else None

        # get fairy and normal type ids
        fairy_id = self._type_map.get('fairy')
        normal_id = self._type_map.get('normal')
    
        # Handle pre-generation 6 fixes
        # (Fairy didn't exist in gen 6)
        if ruleset_id < 6:
            if t1 == fairy_id:
                self.logger.debug("Retroactive change: Fairy -> Normal (Type 1)")
                t1 = normal_id
            if t2 == fairy_id:
                self.logger.debug("Retroactive change: Fairy -> None (Type 2)")
                t2 = None 
    
        self.logger.debug(f"Types: {t1}, {t2}")
        self.logger.info("<< _get_validate_types")
        return t1, t2

    def get_placeholder_ids(self):
        """Returns a list of IDs that are currently placeholders in the DB.
        This is used for filling in placeholders created by the first initial run
        :returns: A list of placeholder IDs."""
        self.logger.debug(">> get_placeholder_ids")
        query = "SELECT id FROM pokemon WHERE name LIKE '%placeholder%' OR slug LIKE '%placeholder%';"
        self.db.cursor.execute(query)
        ids = self.db.cursor.fetchall()
        self.logger.debug(f"Placeholder Ids: {ids}")

        self.logger.debug("<< get_placeholder_ids")
        return [row[0] for row in ids]
