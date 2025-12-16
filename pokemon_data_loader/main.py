# main.py

import os
import ast
# Assuming DBConnection and API functions are imported from these files
from db_utils import DBConnection 
from api_utils import fetch_pokemon_data, process_types, process_abilities, fetch_valid_pokemon_forms
from dotenv import load_dotenv

load_dotenv()

# GEN_VERSION_MAP
GEN_VERSION_MAP = {
    1: [1, 2, 3], 2: [4, 5, 6], 3: [7, 8, 9, 10, 11], 4: [12, 13, 14, 15, 16],
    5: [17, 18, 21, 22], 6: [23, 24, 25, 26], 7: [27, 28, 29, 30],
    8: [31, 32, 33, 34], 9: [35, 36]
}
POKEAPI_GRAPHQL_URL = os.getenv("POKEAPI_GRAPHQL_URL", 'https://graphql.pokeapi.co/v1beta2')
GENERATIONS_TO_LOAD = os.getenv("GENERATIONS_TO_LOAD")
VALID_METHODS_ENV = os.getenv("VALID_ENCOUNTER_METHODS")

# Tries to get the target gens from the env file, defaults to [1, 2]
try:
    TARGET_GENS = ast.literal_eval(GENERATIONS_TO_LOAD)
    if not isinstance(TARGET_GENS, list): raise ValueError("Not a list.")
except (ValueError, SyntaxError, TypeError):
    print("Warning: GENERATIONS_TO_LOAD environment variable is malformed. Defaulting to [1, 2].")
    TARGET_GENS = [1, 2] 
    
# Tries to get the valid encounter methods from the env file, defaults to Nuzlocke list
try:
    VALID_ENCOUNTER_METHODS = ast.literal_eval(VALID_METHODS_ENV)
    if not isinstance(VALID_ENCOUNTER_METHODS, list): raise ValueError("Not a list.")
except (ValueError, SyntaxError, TypeError):
    print("Warning: VALID_ENCOUNTER_METHODS env var is malformed or missing. Using default list.")
    VALID_ENCOUNTER_METHODS = [
            "walk", "surf", "rock-smash", "old-rod", "good-rod", "super-rod", 
            "headbutt", "grass-chasing", "fishing", "gift", "devon-scope", 
            "gift-egg", "seaweed", "only-one", "feebas-tile-fishing", "roaming-water" 
        ]

EVOLUTION_LINKS_TO_RESOLVE = []


def populate_database_for_gen(gen_id, db_conn, type_map, ability_map, local_id_map):
    """
    Handles the ETL process for a single generation (Pass 1: Insertion and Link Recording).
    Ensures every species gets a new stats record for the current ruleset_id.
    todo: make less complex
    """

    ruleset_id = gen_id 
    
    version_ids = GEN_VERSION_MAP.get(gen_id)
    if not version_ids:
        print(f"Warning: No version mapping for Gen {gen_id}. Skipping Nuzlocke filter.")
        valid_form_ids = set()
    else:
        valid_form_ids = fetch_valid_pokemon_forms(
            POKEAPI_GRAPHQL_URL, version_ids, VALID_ENCOUNTER_METHODS
        )
        print(f"Found {len(valid_form_ids)} Nuzlocke-valid Pokémon Forms for Gen {gen_id}.")
    
    species_list = fetch_pokemon_data(POKEAPI_GRAPHQL_URL, gen_id)
    
    print(f"\nProcessing Gen {gen_id}: Checking {len(species_list)} species...")

    processed_count = 0
    # Set to track species inserted *in this ruleset* for evolution chain checks
    inserted_species_ids = set() 
    
    for species in species_list:
        api_species_id = species['id']
        species_name = species['name']
        evolves_from_species_id = species['evolves_from_species_id']
        
        # --- Form Data Retrieval ---
        base_form_data = next((p for p in species['pokemons'] if p['name'] == species_name), None)
        if not base_form_data:
             base_form_data = species['pokemons'][0] if species['pokemons'] else None
        if not base_form_data:
            print(f"Warning: No form data found for species {species_name}. Skipping.")
            continue
            
        local_pokemon_id = local_id_map.get(api_species_id)
        
        
        # If local_pokemon_id is None, this species has never been inserted before.
        if local_pokemon_id is None:
            is_species_catchable = any(p['id'] in valid_form_ids for p in species['pokemons'])
            is_valid_wild = is_species_catchable
            is_valid_evolution = evolves_from_species_id and (evolves_from_species_id in inserted_species_ids)

            if not is_valid_wild and not is_valid_evolution:
                # If it's new AND not Nuzlocke-valid/part of chain, skip insertion entirely.
                print(f"Skipping {species_name} (ID {api_species_id}): New but not catchable/required for chain.")
                continue


        # If local_pokemon_id is None, this is a new species that passed the filter above.
        if local_pokemon_id is None:
            evolves_from_local_id = local_id_map.get(evolves_from_species_id) if evolves_from_species_id else None

            local_pokemon_id = db_conn.insert_pokemon(
                api_species_id, species_name, species_name, evolves_from_local_id
            )
            local_id_map[api_species_id] = local_pokemon_id
        
        inserted_species_ids.add(api_species_id) 


        # This executes for *every* species (new or existing) in the current generation.
        type_1_id, type_2_id = process_types(
            base_form_data['pokemontypes'], type_map, gen_id
        )
        ability_1_id, ability_2_id, hidden_ability_id = process_abilities(
            base_form_data['pokemonabilities'], ability_map
        )
        
        print(f"DEBUG: Inserting Stats: Local ID={local_pokemon_id}, Ruleset ID={ruleset_id}, Species={species_name}")

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
            
        processed_count += 1
        
    print(f"Successfully inserted {processed_count} species and stats records for Gen {gen_id}.")
    return inserted_species_ids
    

def populate_database():
    db_conn = None
    try:
        db_conn = DBConnection() 
        type_map = db_conn.get_map('types')
        ability_map = db_conn.get_map('abilities')
        local_id_map = {} 
        
        all_inserted_species_ids = set() 

        # Loop over all target generations (Pass 1 execution)
        for gen_id in TARGET_GENS:
            # Receive the set of species IDs inserted in this gen
            inserted_ids_this_gen = populate_database_for_gen(gen_id, db_conn, type_map, ability_map, local_id_map)
            all_inserted_species_ids.update(inserted_ids_this_gen)
 
        
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
    populate_database()