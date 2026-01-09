import logging

import requests

import db_utils
from config.queries import NUZLOCKE_VALIDATION_QUERY, GENERATION_DATA_QUERY, ENCOUNTER_QUERY, FETCH_ALL_VERSIONS_QUERY
from errors.errors import PokeAPIError
from config.config import POKEAPI_GRAPHQL_URL, VALID_ENCOUNTER_METHODS

logger = logging.getLogger(__name__)


def fetch_valid_pokemon_forms(version_ids: list) -> set:
    """Fetches a set of unique pokemon_id (Form IDs) that are catchable via valid methods.
    :param version_ids: A list of version IDs to check against
    :return: A set of pokemon_id values that are obtainable in some way.
    """
    logger.info(">> fetch_valid_pokemon_forms")

    variables = {
        "versionIds": version_ids,
        "validMethods": VALID_ENCOUNTER_METHODS
    }

    response = requests.post(
        POKEAPI_GRAPHQL_URL,
        json={'query': NUZLOCKE_VALIDATION_QUERY, 'variables': variables}
    )
    response.raise_for_status()
    json_data = response.json()

    if 'errors' in json_data:
        raise PokeAPIError(f"GraphQL Errors: {json_data['errors']}")

    # Return a set of unique IDs for fast lookup
    valid_ids = {e['pokemon_id'] for e in json_data['data']['encounter']}
    logger.debug(f"Valid Pokemon IDs: {valid_ids}")
    logger.info("<< fetch_valid_pokemon_forms")

    return valid_ids


def fetch_pokemon_data(gen_id: int):
    """Fetches combined Pokémon data for a specific generation.
    :param gen_id: The generation ID to fetch data for
    :returns data about every pokemon in the generation. Abiltities, types, names, etc. """
    
    logger.info(">> fetch_pokemon_data")

    variables = {"genId": gen_id}

    response = requests.post(
        POKEAPI_GRAPHQL_URL,
        json={'query': GENERATION_DATA_QUERY, 'variables': variables}
    )

    response.raise_for_status()
    json_data = response.json()

    if 'errors' in json_data:
        raise PokeAPIError(f"GraphQL Errors: {json_data['errors']}")
    logger.info("<< fetch_pokemon_data")
    return json_data['data']['pokemonspecies']


def process_abilities(raw_abilities: list, ability_map: dict, db_conn):
    """
    Extracts and maps abilities. If an ability is missing from the map, 
    it inserts it into the DB and updates the map.
    """
    logger.info(">> process_abilities")

    # Store the names from the API for each slot
    ability_names = {1: None, 2: None, 3: None}

    for a_data in raw_abilities:
        slot = a_data.get('slot')
        ability_info = a_data.get('ability')
        if ability_info:
            name = ability_info.get('name', '').lower()
            flavor_text = ability_info['abilityflavortexts'][0]['flavor_text']
            if slot in ability_names:
                ability_names[slot] = name

    def get_or_create_id(name):
        if not name:
            return None

        # 1. Check if it exists in our dictionary
        ability_id = ability_map.get(name)

        # 2. If not found, insert into DB and update the dictionary
        if ability_id is None:
            logger.warning(f"Ability '{name}' not found. Inserting into DB...")
            # We call the new upsert_ability method on the db_conn instance
            ability_id = db_conn.upsert_ability(name, flavor_text)
            ability_map[name] = ability_id

        return ability_id

    # Resolve IDs for all slots
    a1 = get_or_create_id(ability_names[1])
    a2 = get_or_create_id(ability_names[2])
    a3 = get_or_create_id(ability_names[3])

    logger.info("<< process_abilities")
    return a1, a2, a3


def process_types(raw_types: list, type_map: dict, gen_id: int):
    """
    Extracts and maps types, applying Generation fixes (Fairy->Normal in Gen 1-5, excluding Steel in Gen 1).
    :param raw_types: The raw types data from the API
    :param type_map: The type map to use for lookups
    :param gen_id: The current generation ID being processed
    Returns (type_1_id, type_2_id)
    """
    
    logger.info(">> process_types")
    
    if not isinstance(type_map, dict):
        raise TypeError(f"type_map must be dict, got {type(type_map)}")

    # If it doesn't return anything, and its below gen6,
    # the type is likely fairy. The api doesn't support 
    # historical data, so we set it to normal here (the
    # old pre-fairy type.)
    if not raw_types and gen_id <= 5:
        return type_map.get("normal"), None

    type_names = {1: None, 2: None}
    for t_data in raw_types:
        slot = t_data['slot']
        t_name = t_data['type']['name'].lower()
        logger.debug(f"Slot is: {slot}, Type is: {t_name}")

        if slot in type_names:
            type_names[slot] = t_name

    type_1_id = type_map.get(type_names[1])
    type_2_id = type_map.get(type_names[2]) if type_names[2] else None
    logger.debug(f"Mapped types: Primary={type_names[1]}, Secondary={type_names[2]}")
    logger.info("<< process_types")
    return type_1_id, type_2_id


def fetch_version_encounters(url: str, version_ids: list, methods: list):
    variables = {"versionIds": version_ids, "validMethods": methods}
    response = requests.post(url, json={'query': ENCOUNTER_QUERY, 'variables': variables})
    response.raise_for_status()
    return response.json()['data']['pokemon']


def fetch_all_versions():
    """
    Fetches all game versions from PokeAPI to populate the local games table.
    """
    logger.info(">> fetch_all_versions")
    response = requests.post(POKEAPI_GRAPHQL_URL, json={'query': FETCH_ALL_VERSIONS_QUERY})

    if response.status_code == 200:
        logger.debug(f"PokeAPI response:  {response.json()}.")
        logger.info("<< fetch_all_versions")
        return response.json()
    else:
        logger.error("Failed to fetch versions from PokeAPI")
        raise PokeAPIError(f"Failed to fetch versions: {response.status_code}")
