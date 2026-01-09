import ast
import os
from dotenv import load_dotenv

load_dotenv()
# ------------------------- Database Settings -------------------------
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("POSTGRES_DB", "nuzlucke")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
# ------------------------- API Settings -------------------------
POKEAPI_GRAPHQL_URL = os.getenv("POKEAPI_GRAPHQL_URL", 'https://graphql.pokeapi.co/v1beta2')

# Generations to load into the database
_target_gens_raw = os.getenv("TARGET_GENERATIONS")

try:
    # This converts the string "[8, 9]" into the list [8, 9]
    TARGET_GENS = ast.literal_eval(_target_gens_raw)
    if not isinstance(TARGET_GENS, list):
        raise ValueError
except (ValueError, SyntaxError, TypeError):
    # Fallback if the .env variable is missing or formatted incorrectly
    print("Warning: TARGET_GENERATIONS environment variable is malformed. Defaulting to [1, 2].")
    TARGET_GENS = [1, 2]

_valid_encounters_raw = os.getenv("VALID_ENCOUNTER_METHODS")
# Tries to get the valid encounter methods from the env file, defaults to a predefined list
try:
    VALID_ENCOUNTER_METHODS = ast.literal_eval(_valid_encounters_raw)
    if not isinstance(VALID_ENCOUNTER_METHODS, list): raise ValueError("Not a list.")
except (ValueError, SyntaxError, TypeError):
    print("Warning: VALID_ENCOUNTER_METHODS env var is malformed or missing. Using default list.")
    VALID_ENCOUNTER_METHODS = [
        "walk", "surf", "rock-smash", "old-rod", "good-rod", "super-rod",
        "headbutt", "grass-chasing", "fishing", "gift", "devon-scope",
        "gift-egg", "seaweed", "only-one", "feebas-tile-fishing", "roaming-water"
    ]


# ------------------------- Static Mappings -------------------------
# Mapping the games and their ids to their generation
GEN_VERSION_MAP = {
    1: [1, 2, 3],  # Red, Blue, Yellow
    2: [4, 5, 6],  # Gold, Silver, Crystal
    3: [7, 8, 9, 10, 11, 19, 20],  # Ruby, Sapphire, Emerald, FireRed, LeafGreen + Colosseum/XD
    4: [12, 13, 14, 15, 16],  # Diamond, Pearl, Platinum, HeartGold, SoulSilver
    5: [17, 18, 21, 22],  # Black, White, Black 2, White 2
    6: [23, 24, 25, 26],  # X, Y, Omega Ruby, Alpha Sapphire
    7: [27, 28, 29, 30, 31, 32],  # Sun, Moon, Ultra Sun, Ultra Moon, Let's Go P/E
    8: [33, 34, 35, 36, 37, 38, 39],  # Sword, Shield + DLCs (Armor/Tundra), BD/SP, Arceus
    9: [40, 41, 42, 43, 47, 48]  # Scarlet, Violet + DLCs (Teal/Indigo), ZA, Mega Dimension
}
# Mapping PokeAPI's version_group_id to rulesets
group_to_ruleset = {
    1: 1,  # Gen 1 (Red/Blue/Yellow)
    2: 1,
    3: 2,  # Gen 2 (Gold/Silver/Crystal)
    4: 2,
    5: 3,  # Gen 3 (Ruby/Sapphire/Emerald/FRLG)
    6: 3,
    7: 3,
    8: 4,  # Gen 4 (DPP/HGSS)
    9: 4,
    10: 4,
    11: 5,  # Gen 5 (Black/White)
    12: 3,  # Colosseum
    13: 3,  # XD
    14: 5,  # Gen 5 (B2W2)
    15: 6,  # Gen 6 (XY/ORAS)
    16: 6,
    17: 7,  # Gen 7 (Sun/Moon/USUM/LetsGo) 
    18: 7,
    19: 7,
    20: 8,  # Gen 8 (Sword/Shield)
    21: 8,  # Gen 8 (the-isle-of-armor)
    22: 8,  # Gen 8 (the-crown-tundra)
    23: 8,  # Gen 8 (BDSP/Arceus)
    24: 8,
    25: 9,  # Gen 9 (Scarlet/Violet)
    26: 9,  # Gen 9 (Teal-Mask)
    27: 9,  # Gen 9 (Indigo-Disk)
    30: 9,  # Legends (LegendsZA)
    31: 9  # Mega Dimension
}
# ------------------------- Logging -------------------------
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")