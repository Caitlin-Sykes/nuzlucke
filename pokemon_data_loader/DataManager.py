import logging

import GameRepository
import PokeApiClient
import PokemonRepository
from utils.Constants import group_to_ruleset, GEN_VERSION_MAP
from utils.models import GameVersion, Config
from utils.models.Poke_Models import Pokemon


class DataManager:

    def __init__(self, api_client: PokeApiClient, game_repo: GameRepository, poke_repo: PokemonRepository):
        self.api_client = api_client
        self.game_repo = game_repo
        self.poke_repo = poke_repo
        self.logger = logging.getLogger(__name__)

    def sync_pokemon_games(self):
        """
        Processes game versions, applies region overrides, 
        and saves them to the database.
       """

        self.logger.debug(">> sync_pokemon_games")

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
                self.logger.debug(
                    f"Upserted game {game.name} with ruleset id {ruleset_id}, api version id {game.id}, region id {region_id}")
            else:
                self.logger.warning(f"Skipping game {game.name} as it has no ruleset.")

        self.logger.debug("<< sync_pokemon_games")

    def sync_pokemon_info(self):
        """For each generation defined, fills the
        Pokémon and Pokémon game stats table with Pokémon information.
        This includes information like abilities, encounter routes,
        and types. """
        self.logger.debug(">> sync_pokemon_info")

        valid_methods = Config.ruleset.valid_encounter_methods

        for gen in Config.ruleset.target_generations:
            self.logger.debug(f"Processing generation {gen}...")
            valid_api_version_ids = GEN_VERSION_MAP.get(gen, [])            # Gets the version ids for the generation
            version_ids = GEN_VERSION_MAP.get(gen, [])
            
            # Keeps track of Pokémon already discovered in this gen 
            discovered_in_gen = set()
            
            # Gets all the Pokémon and their regions from the api
            all_data = self.api_client.fetch_all_pokemon_from_gen(
                gen=gen,
                version_ids=version_ids,
                valid_methods=valid_methods
            )

            for pokemon in all_data.data.pokemon:
                self.logger.debug(f"--- POKÉMON: {pokemon.name.upper()} (ID: {pokemon.id}) ---")
                self.poke_repo.upsert_pokemon_data(pokemon, gen)
                discovered_in_gen.add(pokemon.id)
                
                # we check the family tree for its evolutions and prevolutions
                if pokemon.pokemonspecy.evolution_chain:
                    for evo in pokemon.pokemonspecy.evolution_chain.pokemonspecies:
                        if evo.id not in discovered_in_gen:
                            self.logger.debug(f"Evo ID {evo.id}, corresponding to {evo.name} not found in gen {gen}. Adding placeholder")
                            self.poke_repo.insert_placeholder_id(evo.id)
                            discovered_in_gen.add(evo.id)

                # Filter the encounters list to only include games from THIS generation
                relevant_encounters = [
                    e for e in pokemon.encounters
                    if e.version_id in valid_api_version_ids
                ]
    
                if relevant_encounters:
                    for v_id in valid_api_version_ids:

                        # get all encounters grouped by game (ie, red, yellow..)
                        game_specific = [e for e in relevant_encounters if e.version_id == v_id]
                    
                        if game_specific:
                            
                            # the api returns multiple entries for the same pokemon for the same area
                            # so we group them
                            summary = {}
                            for enc in game_specific:
                                key = (enc.location_area.id, enc.method.encountermethod.name)
                    
                                if key not in summary:
                                    summary[key] = {
                                        "min": enc.min_level,
                                        "max": enc.max_level,
                                        "obj": enc
                                    }
                                else:
                                    # we get the minimum and maximum level 
                                    summary[key]["min"] = min(summary[key]["min"], enc.min_level)
                                    summary[key]["max"] = max(summary[key]["max"], enc.max_level)
                    
                            # then we insert them
                            for data in summary.values():
                                self.poke_repo.upsert_encounters(
                                    pokemon.id,
                                    v_id,
                                    data["min"],
                                    data["max"],
                                    data["obj"]
                                )
                                
            self.logger.debug(f"Processing {len(all_data.data.pokemon)} Pokémon from generation {gen}...")

            # This goes back and will update all the "placeholder" pokemon with their actual details 
            self._update_pokemon_placeholder(gen)
            
            self.logger.debug("<< sync_pokemon_info")

   

    """ 
    ----------------------------------------
    Helper Functions
    ----------------------------------------
    """

    def _resolve_region_name(self, version: GameVersion) -> str | None:
        """Internal helper to handle the logic for missing API regions.
            :param version: GameVersion object from the api response
            :returns: region name as string or None if not found."""

        self.logger.debug(">> _resolve_region_name")
        # Checks the api response for the region name.
        if version.versiongroup.versiongroupregions:
            self.logger.debug("<< _resolve_region_name")
            return version.versiongroup.versiongroupregions[0].region.name

        # Overrides for games that don't have a region in the api response.
        overrides = {
            'xd': 'orre',
            'colosseum': 'orre',
            'legends-za': 'kalos',
            'mega-dimension': 'kalos'
        }

        if version.name in overrides:
            self.logger.debug("<< _resolve_region_name")
            return overrides[version.name]

        self.logger.debug(f"<< _resolve_region_name. No region found for {version.name}. Defaulting to None.")
        return None
    
    def _update_pokemon_placeholder(self, current_gen):
        """Orchestrates the logic that replaces
         placeholder Pokémon with the actual Pokémon details
         :param current_gen: The current generation to update for
         """
        
        self.logger.debug(">> _update_pokemon_placeholder")
        
        # Gets all the placeholder Pokémon ids
        placeholder_ids = self.poke_repo.get_placeholder_ids()
        
        if not placeholder_ids:
            self.logger.info("No placeholder Pokémon found. Skipping update.")
            self.logger.debug("<< _update_pokemon_placeholder")
            return
        
        placeholder_pokemon_data = self.api_client.fetch_pokemon_data(placeholder_ids)
        
        # For each placeholder Pokémon, update it with the actual data
        for pokemon in placeholder_pokemon_data.data.pokemon:
            self.logger.debug(f"Updating placeholder Pokémon: {pokemon}")
            self.poke_repo.upsert_pokemon_data(pokemon, current_gen)
        
        self.logger.debug("<< _update_pokemon_placeholder")

