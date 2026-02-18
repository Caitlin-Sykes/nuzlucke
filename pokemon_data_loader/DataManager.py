import logging

from PokeApiClient import PokeApiClient
from repository import PokemonRepository, GameRepository
from repository.EncounterRepository import EncounterRepository
from utils.Constants import GROUP_TO_RULESET, GEN_VERSION_MAP
from utils.models import GameVersion, Config
from utils.models.Poke_Models import Pokemon


def _filter_relevant_encounters(valid_api_version_ids, pokemon):
    """Filters encounters to only include those relevant for the valid API version IDs.
    :param valid_api_version_ids: The list of valid API version IDs to filter encounters for.
    :returns: A list of relevant encounters."""
    return [e for e in pokemon.encounters if e.version_id in valid_api_version_ids]


def _summarise_encounters(game_specific):
    """
    Aggregates encounter data by location and encounter method,
    calculating minimum and maximum levels for each group.
    :param game_specific: A list of encounters relevant to a specific game version.
    :returns: A dictionary mapping (location_id, encounter_method) to a summary object.
    """
    summary = {}
    for enc in game_specific:
        key = (enc.location_area.id, enc.method.encountermethod.name)
        if key not in summary:
            summary[key] = {"min": enc.min_level, "max": enc.max_level, "obj": enc}
        else:
            summary[key]["min"] = min(summary[key]["min"], enc.min_level)
            summary[key]["max"] = max(summary[key]["max"], enc.max_level)
    return summary


def _filter_game_specific_encounters(relevant_encounters, version_id):
    """Filters encounters specific to a given game version.
    :param relevant_encounters: A list of all relevant encounters.
    :param version_id: The ID of the game version to filter encounters for.
    :returns: A list of encounters relevant to the given game version."""
    return [e for e in relevant_encounters if e.version_id == version_id]


class DataManager:
    """Manages data synchronisation and retrieval for Pokémon game data."""
    def __init__(self, api_client: PokeApiClient, game_repo: GameRepository, poke_repo: PokemonRepository, encounter_repo: EncounterRepository):
        self.api_client = api_client
        self.game_repo = game_repo
        self.poke_repo = poke_repo
        self.encounter_repo = encounter_repo
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
            ruleset_id = GROUP_TO_RULESET.get(game.version_group_id)

            # If the game has a ruleset
            if ruleset_id is not None:
                self.game_repo.upsert_game(game.name, ruleset_id, game.id, region_id)
                self.logger.debug(
                    f"Upserted game {game.name} with ruleset id {ruleset_id}, api version id {game.id}, region id {region_id}")
            else:
                self.logger.warning(f"Skipping game {game.name} as it has no ruleset.")

        # inserts metadata about each game
        self.game_repo.insert_game_metadata()
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
                
                # we check the family tree for its evolutions and pre-evolutions
                if pokemon.pokemonspecy.evolution_chain:
                    for evo in pokemon.pokemonspecy.evolution_chain.pokemonspecies:
                        if evo.id not in discovered_in_gen:
                            self.logger.debug(f"Evo ID {evo.id}, corresponding to {evo.name} not found in gen {gen}. Adding placeholder")
                            self.poke_repo.insert_placeholder_id(evo.id)
                            discovered_in_gen.add(evo.id)

                self._update_pokemon_locations(valid_api_version_ids, pokemon)
                    
                                
            self.logger.debug(f"Processing {len(all_data.data.pokemon)} Pokémon from generation {gen}...")

            # This goes back and will update all the "placeholder" Pokémon with their actual details 
            self._update_pokemon_placeholder(gen)
            
            self.logger.debug("<< sync_pokemon_info")

    def sync_pokemon_encounters(self):
        """
        Syncs encounter methods and data for all Pokémon in the database.
        """
        self.logger.debug(">> sync_pokemon_encounters")
        
        # inserts the encounter methods based off the encounter table
        self.encounter_repo.insert_encounter_methods()

        for gen in Config.ruleset.target_generations:
            # Gets all the games and their regions from the api
            version_ids = GEN_VERSION_MAP.get(gen, [])

            for version in version_ids:
                self.logger.debug(f"Mapping encounters for {version}...")
                # maps land encounters to milestones based on the game version
                self.encounter_repo.map_encounters_to_milestones(version)
                
                # Depending on what version we are loading, apply overrides for specific areas
                match version:
                    # Red,Blue,Yellow,FireRed,LeafGreen,let's go eevee let's go Pikachu 
                    case 1 | 2 | 3 | 10 | 11 | 31 | 32:
                        self.encounter_repo.kanto_overrides()
                    
            # Add the surf encounters based on the config
            self.encounter_repo.sync_surf_milestones()
        self.logger.debug("<< sync_pokemon_encounters")

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

    def _update_pokemon_locations(self, valid_api_version_ids, pokemon=Pokemon):
        """ Aggregates encounter data by location and encounter method and adds to the database.
        :param valid_api_version_ids: The list of valid API version IDs to filter encounters for.
        :param pokemon: The Pokémon for which encounter data is being updated."""
        self.logger.debug(">> _update_pokemon_locations")

        relevant_encounters = _filter_relevant_encounters(valid_api_version_ids, pokemon)
        if not relevant_encounters:
            self.logger.debug("No relevant encounters found. Exiting.")
            self.logger.debug("<< _update_pokemon_locations")
            return
    
        for v_id in valid_api_version_ids:
            game_specific = _filter_game_specific_encounters(relevant_encounters, v_id)
            if game_specific:
                summary = _summarise_encounters(game_specific)
                self._insert_encounter_summary(pokemon.id, v_id, summary)
    
        self.logger.debug("<< _update_pokemon_locations")

    def _insert_encounter_summary(self, pokemon_id, version_id, summary):
        """
        Inserts aggregated encounter data into the repository.
        :param pokemon_id: The ID of the Pokémon for which encounter data is being inserted.
        :param version_id: The ID of the game version for which encounter data is being inserted.
        :param summary: A dictionary containing encounter summary data.
        """
        self.logger.debug(">> _insert_encounter_summary")
        for data in summary.values():
            self.poke_repo.upsert_encounters(
                pokemon_id,
                version_id,
                data["min"],
                data["max"],
                data["obj"]
            )
            self.logger.debug(f"Inserted summary for {pokemon_id} in version {version_id}")
        self.logger.debug("<< _insert_encounter_summary")
    
