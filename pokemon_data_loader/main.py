import os

from config.config import LOGGING_LEVEL, POKEAPI_GRAPHQL_URL, GEN_VERSION_MAP, \
    VALID_ENCOUNTER_METHODS, group_to_ruleset, TARGET_GENS
from db_utils import DBConnection
from api_utils import fetch_pokemon_data, process_types, process_abilities, fetch_valid_pokemon_forms, \
    fetch_version_encounters, fetch_all_versions
import logging

logger = logging.getLogger(__name__)

EVOLUTION_LINKS_TO_RESOLVE = []


def populate_database_for_gen(gen_id, db_conn, type_map, ability_map, local_id_map):
    """
    Ensures every species gets a new stats record for the current ruleset_id.
    :param gen_id: The generation ID to process
    :param db_conn: The database connection object
    :param type_map: The type map to use for lookups
    :param local_id_map: A map of API species IDs to local IDs

    """
    logger.info(" >> populate_database_for_gen")
    ruleset_id = gen_id

    version_ids = GEN_VERSION_MAP.get(gen_id)
    
    # Get all Pokemon ids that are catchable in the current generation
    if not version_ids:
        logger.warning(f"No version mapping for Gen {gen_id}. Skipping Nuzlocke filter.")
        valid_form_ids = set()
    else:
        # This is just an array of Pokemon Ids to cross compare against
        valid_form_ids = fetch_valid_pokemon_forms(
            version_ids
        )

    # Get the total list of pokemon available in a generation
    species_list = fetch_pokemon_data(gen_id)

    # Set to track species inserted *in this ruleset* for evolution chain checks
    inserted_species_ids = set()

    for species in species_list:
        
        # Gets the current id, pokemon name, and evolves_from_species_id
        api_species_id = species['id']
        species_name = species['name']
        evolves_from_species_id = species['evolves_from_species_id']
        logger.debug(f"Processing species {species_name} (ID {api_species_id}, evolves from {evolves_from_species_id})")

        # --- Form Data Retrieval ---
        base_form_data = next((p for p in species['pokemons'] if p['name'] == species_name), None)
        if not base_form_data:
            base_form_data = species['pokemons'][0] if species['pokemons'] else None

        local_pokemon_id = local_id_map.get(api_species_id)

        # If local_pokemon_id is None, this species has never been inserted before.
        if local_pokemon_id is None:
            
            # Check if the species is catchable in the current generation
            is_species_catchable = any(p['id'] in valid_form_ids for p in species['pokemons'])
            # Checks if the pokemon it evolves from is already inserted
            is_valid_evolution = evolves_from_species_id and (evolves_from_species_id in inserted_species_ids)

            # Gen 9 is buggy at the moment so we have to handle it specially
            is_gen_9_processing = (gen_id == 9)

            # Allow it if it's catchable, an evolution, OR if we are processing Gen 9
            if not is_species_catchable and not is_valid_evolution and not is_gen_9_processing:
                # If it's new AND not Nuzlocke-valid/part of chain, skip insertion entirely.
                logger.warning(f"Skipping {species_name} (ID {api_species_id}): New but not catchable/required for chain.")
                continue

        # If local_pokemon_id is None, this is a new species that passed the filter above.
        if local_pokemon_id is None:
            evolves_from_local_id = local_id_map.get(evolves_from_species_id) if evolves_from_species_id else None

            local_pokemon_id = db_conn.insert_pokemon(
                api_species_id, species_name, species_name, evolves_from_local_id
            )
            local_id_map[api_species_id] = local_pokemon_id

        inserted_species_ids.add(api_species_id)

        # Checks the types
        type_1_id, type_2_id = process_types(
            base_form_data['pokemontypes'], type_map, gen_id
        )
        
        # Checks the abilities
        ability_1_id, ability_2_id, hidden_ability_id = process_abilities(
            base_form_data['pokemonabilities'], ability_map, db_conn
        )

        print(f"DEBUG: Inserting Stats: Local ID={local_pokemon_id}, Ruleset ID={ruleset_id}, Species={species_name}, Types={type_1_id}/{type_2_id}, Abilities={ability_1_id}/{ability_2_id}/{hidden_ability_id}")

        # This will create a unique entry for (pokemon_id, ruleset_id)
        db_conn.insert_game_stats(
            local_pokemon_id, ruleset_id, type_1_id, type_2_id, 
            ability_1_id, ability_2_id, hidden_ability_id
        )

        next_api_species_id = None
        evolution_chain_data = species.get('evolutionchain')

        if evolution_chain_data:
            chain_species = evolution_chain_data.get('pokemonspecies')

            if chain_species:
                current_species_id = species['id']
                current_index = next((i for i, s in enumerate(chain_species) if s['id'] == current_species_id), -1)

                if current_index != -1 and current_index + 1 < len(chain_species):
                    next_api_species_id = chain_species[current_index + 1]['id']

        if next_api_species_id:
            EVOLUTION_LINKS_TO_RESOLVE.append({
                'from_local_id': local_pokemon_id,
                'to_api_species_id': next_api_species_id,
                'gen_id': gen_id
            })


    encounter_data = fetch_version_encounters(
        POKEAPI_GRAPHQL_URL, version_ids, VALID_ENCOUNTER_METHODS
    )
    for p in encounter_data:
        local_poke_id = local_id_map.get(p['id'])
        if not local_poke_id: continue

        for enc in p['encounters']:
            # 1. Map version to your local game_id
            local_game_id = db_conn.get_game_id_by_version(enc['version_id'])
            if not local_game_id: continue

            # 2. Upsert Location and Area
            loc_data = enc['location_area']['location']
            area_data = enc['location_area']

            # Get min and max level
            min_lvl = enc['min_level']
            max_lvl = enc['max_level']

            loc_id = db_conn.upsert_location(loc_data['id'], loc_data['name'], loc_data['region_id'])
            area_id = db_conn.upsert_area(area_data['id'], area_data['name'], loc_id)

            # 3. Insert specific encounter
            method_name = enc['method']['encountermethod']['name']
            db_conn.insert_encounter(local_game_id, loc_id, area_id, local_poke_id, method_name, max_lvl, min_lvl)
    logger.info(" << populate_database_for_gen")
    return inserted_species_ids


def seed_games_from_api_json(json_data, db_conn):
    """
    Iterates through the API version list and uses the group_to_ruleset 
    map to populate the games table while keeping developer comments intact.
    :param json_data: The JSON data from the API
    :param db_conn: The database connection object
    """

    logger.info(" >> seed_games_from_api_json")
    versions = json_data['data']['version']
    region_map = db_conn.get_all_from('regions')

    for v in versions:
        ruleset_id = group_to_ruleset.get(v['version_group_id'])
        regions_list = v.get('versiongroup', {}).get('versiongroupregions', [])

        logger.debug(f"Version: {v['name']}, Ruleset: {ruleset_id}, Regions: {regions_list}")

        if regions_list and len(regions_list) > 0:
            region_name = regions_list[0].get('region', {}).get('name')
        # The API doesn't return the region for Colosseum, XD, LegendsZa and Mega Dimension
        # so we manually add it.
        elif v['name'] in ['xd', 'colosseum']:
            region_name = 'orre'
        elif v['name'] in ['legends-za', 'mega-dimension']:
            region_name = 'kalos'
        else:
            logger.warning(
                f"No regions found for game {v['name']}, version group {v['version_group_id']}. Setting to null by default.")

        if ruleset_id:
            db_conn.upsert_game(
                name=v['name'].replace('-', ' ').title(),
                ruleset_id=ruleset_id,
                api_version_id=v['id'],
                region_id=region_map.get(region_name) if region_name else None
            )
    db_conn.commit()
    logger.info("<< seed_games_from_api_json")


def populate_database():
    db_conn = None
    try:
        db_conn = DBConnection()

        # Getting and seeding games table
        version_data = fetch_all_versions()
        seed_games_from_api_json(version_data, db_conn)

        # Gets all Types from the DB
        type_map = db_conn.get_all_from('types')
        
        local_id_map = {}
        ability_map = db_conn.get_all_from('abilities')
       

        # For each generation, add the Pokemon to the DB
        for gen_id in TARGET_GENS:
            logger.info(f"Processing generation {gen_id}...")
            # Receive the set of species IDs inserted in this gen
            inserted_ids_this_gen = populate_database_for_gen(gen_id, db_conn, type_map, ability_map, local_id_map)
            # all_inserted_species_ids.update(inserted_ids_this_gen)

        db_conn.commit()
        print("\nAll database populations complete.")

    except Exception as e:
        print(f"An error occurred during population: {e}")
        if db_conn:
            db_conn.rollback()
    finally:
        if db_conn:
            db_conn.close()


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(base_dir, 'pokemon_data_loader.log')
    logging.basicConfig(filename=log_path, level=LOGGING_LEVEL,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    populate_database()
