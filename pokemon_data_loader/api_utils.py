import requests

# This uses the genId variable to determine what generation to fetch data for
# It also uses this for filtering, such as where there are differences in Pokemon's
# Types between generations
QUERY = """
query GenData($genId: Int!) {
  pokemonspecies(
    where: { generation_id: { _lte: $genId } } 
    order_by: { id: asc }
  ) {
    id
    name
    evolves_from_species_id

    pokemons {
      id
      name

      pokemontypes(
        where: { type: { generation_id: { _lte: $genId } } } 
        order_by: { slot: asc }
      ) {
        slot
        type {
          name
        }
      }

      pokemonabilities(order_by: { slot: asc }) {
        slot
        ability {
          name
        }
      }
    }
  }
}
"""

# This is used to try and filter out Pokemon that are obtainable, versus those that are not
# For example, where a previous form is only obtainable via breeding, or by trading with another game
# It does this by checking the encounter methods, such as whether it is obtained by running in grass, etc
# This is changeable in the .env
NUZLOCKE_VALIDATION_QUERY = """
query NuzlockeCatchableForms($versionIds: [Int!]!, $validMethods: [String!]!) {
  encounter( 
    where: {
      version_id: {_in: $versionIds},
      encounterslot: {
        encountermethod: { 
          name: {_in: $validMethods} 
        }
      }
    }
    distinct_on: [pokemon_id] 
    order_by: {pokemon_id: asc}
  ) {
    pokemon_id 
  }
}
"""


def fetch_valid_pokemon_forms(url: str, version_ids: list, valid_methods: list) -> set:
    """Fetches a set of unique pokemon_id (Form IDs) that are catchable via valid methods."""
    print(f"Fetching Nuzlocke-valid catchable Forms from PokeAPI GraphQL at {url}...")
    
    variables = {
        "versionIds": version_ids,
        "validMethods": valid_methods
    }

    response = requests.post(
        url, 
        json={'query': NUZLOCKE_VALIDATION_QUERY, 'variables': variables}
    )
    response.raise_for_status()
    json_data = response.json()
    
    if 'errors' in json_data:
        raise Exception(f"GraphQL Errors: {json_data['errors']}")
        
    # Return a set of unique IDs for fast lookup
    valid_ids = {e['pokemon_id'] for e in json_data['data']['encounter']}
    return valid_ids
    
def fetch_pokemon_data(url: str, gen_id: int):
    """Fetches combined Pokémon data for a specific generation."""
    print(f"Fetching Gen {gen_id} data from PokeAPI GraphQL at {url}...")
    
    variables = {"genId": gen_id}

    response = requests.post(
        url, 
        json={'query': QUERY, 'variables': variables}
    )
    
    response.raise_for_status()
    json_data = response.json()
    
    if 'errors' in json_data:
        raise Exception(f"GraphQL Errors: {json_data['errors']}")
        
    return json_data['data']['pokemonspecies']


def process_abilities(raw_abilities: list, ability_map: dict):
    """
    Extracts and maps abilities based on slot (1 and 2 are standard, 3 is hidden).
    Returns (ability_1_id, ability_2_id, hidden_ability_id)
    """
    if not isinstance(ability_map, dict):
        raise TypeError(f"ability_map must be dict, got {type(ability_map)}")
    
    ability_names = {1: None, 2: None, 3: None}
    
    for a_data in raw_abilities:
        slot = a_data['slot']
        a_name = a_data['ability']['name'].lower()
        
        if slot in ability_names:
            ability_names[slot] = a_name
    
    ability_1_id = ability_map.get(ability_names[1])
    ability_2_id = ability_map.get(ability_names[2])
    hidden_ability_id = ability_map.get(ability_names[3])
    
    return ability_1_id, ability_2_id, hidden_ability_id


def process_types(raw_types: list, type_map: dict, gen_id: int):
    """
    Extracts and maps types, applying Generation fixes (Fairy->Normal in Gen 1-5, excluding Steel in Gen 1).
    :param raw_types: The raw types data from the API
    :param type_map: The type map to use for lookups
    :param gen_id: The current generation ID being processed
    Returns (type_1_id, type_2_id)
    """
    if not isinstance(type_map, dict):
        raise TypeError(f"type_map must be dict, got {type(type_map)}")

    # If it doesn't return anything, and its below gen1,
    # the type is likely fairy. The api doesn't support 
    # historical data, so we set it to normal here (the
    # old pre-fairy type.
    if not raw_types and gen_id <= 5:
        return type_map.get("normal"), None
    
    type_names = {1: None, 2: None}
    for t_data in raw_types:
        slot = t_data['slot']
        t_name = t_data['type']['name'].lower()
        print(f"Slot is: {slot}")
        print(f"Type is: {t_name}")
      
        if slot in type_names:
             type_names[slot] = t_name

    type_1_id = type_map.get(type_names[1])
    type_2_id = type_map.get(type_names[2]) if type_names[2] else None
    
    return type_1_id, type_2_id