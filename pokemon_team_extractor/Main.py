import re
import logging
import os

import Loaders;
from Helpers import get_slot, get_level

DATA_DIR = "./data"
OUTPUT_DIR = "output"
logger = logging.getLogger(__name__)
Loaders = Loaders.Loaders()
RIVAL_STARTER_CONDITIONS = {
    # Rival has Charizard/Charmeleon/Charmander -> Player must have picked Bulbasaur
    'CHARMANDER': "bulbasaur",
    'CHARMELEON': "bulbasaur",
    'CHARIZARD':   "bulbasaur",

    # Rival has Blastoise/Wartortle/Squirtle -> Player must have picked Charmander
    'SQUIRTLE':   "charmander",
    'WARTORTLE':  "charmander",
    'BLASTOISE':  "charmander",

    # Rival has Venusaur/Ivysaur/Bulbasaur -> Player must have picked Squirtle
    'BULBASAUR':  "squirtle",
    'IVYSAUR':    "squirtle",
    'VENUSAUR':   "squirtle",

    # Rival has CYNDAQUIL/QUILAVA/TYPHLOSION -> Player must have picked chikorita
    'CYNDAQUIL': "chikorita",
    'QUILAVA': "chikorita",
    'TYPHLOSION':   "chikorita",
    
    # Rival has TOTODILE/CROCONAW/FERALIGATR -> Player must have picked cyndaquil
    'TOTODILE':   "cyndaquil",
    'CROCONAW':  "cyndaquil",
    'FERALIGATR':  "cyndaquil",
    
    # Rival has CHIKORITA/BAYLEAF/MEGANIUM -> Player must have picked totodile
    'CHIKORITA':  "totodile",
    'BAYLEAF':    "totodile",
    'MEGANIUM':   "totodile",

    # Rival has TORCHIC/COMBUSKEN/BLAZIKEN -> Player must have picked treecko
    'TORCHIC': "treecko",
    'COMBUSKEN': "treecko",
    'BLAZIKEN':   "treecko",

    # Rival has MUDKIP/MARSHTOMP/SWAMPERT -> Player must have picked torchic
    'MUDKIP':   "torchic",
    'MARSHTOMP':  "torchic",
    'SWAMPERT':  "torchic",

    # Rival has TREECKO/GROVYLE/SCEPTILE -> Player must have picked mudkip
    'TREECKO':  "mudkip",
    'GROVYLE':    "mudkip",
    'SCEPTILE':   "mudkip",

    # Rival has CHIMCHAR/MONFERNO/INFERNAPE -> Player must have picked turtwig
    'CHIMCHAR': "turtwig",
    'MONFERNO': "turtwig",
    'INFERNAPE':   "turtwig",

    # Rival has PIPLUP/PRINPLUP/EMPOLEON -> Player must have picked chimchar
    'PIPLUP':   "chimchar",
    'PRINPLUP':  "chimchar",
    'EMPOLEON':  "chimchar",

    # Rival has TURTWIG/GROTLE/TORTERRA -> Player must have picked piplup
    'TURTWIG':  "piplup",
    'GROTLE':    "piplup",
    'TORTERRA':   "piplup"
}

def calculate_moves(species, level, moves_db, base_db):
    """Calculates the moves for a given Pokemon at a given level.
    :param species: The Pokemon's species name.
    :param level: The Pokemon's level.
    :param moves_db: A dictionary mapping species names to a list of (level, move) tuples.
    :param base_db: A dictionary mapping species names to a list of base moves.
    @return: A list of the Pokemon's moves, sorted by level."""
    
    spec = species.upper().strip()

    # Start with base moves, or an empty list if not found
    current_moves = list(base_db.get(spec, []))

    # Overlay level-up moves
    if spec in moves_db:
        for m_lvl, m_name in moves_db[spec]:
            if m_lvl <= level:
                if m_name not in current_moves:
                    current_moves.append(m_name)
            else:
                break

  
    final = current_moves[-4:]

    return final if final else ['no-data']


# --- TRAINER SCANNING ---




def get_mandatory_labels(scripts_folder, constant_file):
    """
   Extracts Trainer Classes (e.g., Rocket) from map scripts.
   Matches dw_const or TrainerHeader usage.
   :param scripts_folder: Folder containing map scripts.
   :param constant_file: file containing trainer ids
   :return: Set of mandatory trainer classes
   """

    # loads all trainer ids based on the file
    id_map = Loaders.load_trainer_constants(constant_file)
    logger.debug(f"All trainer_ids {id_map}")
    mandatory = set()

    # for every script in the scripts folder
    for root, _, files in os.walk(scripts_folder):
        for file in files:
            if file.endswith('.asm'):
                with open(os.path.join(root, file), 'r', errors='ignore') as f:
                    content = f.read()

                    #  looks for all events like:
                    # trainer EVENT_BEAT_ROUTE_24_TRAINER_0,
                    # compares the id with the id map and adds it
                    ids = re.findall(r'trainer\s+EVENT_[A-Z0-9_]+,\s*(\d+)', content)
                    for fid in ids:
                        if int(fid) in id_map: mandatory.add(id_map[int(fid)])

                    # Fetches all the rival fights
                    rivals = re.findall(r'OPP_([A-Z0-9_]+)', content)
                    logger.debug(f"rival: {rivals}")

                    for b in rivals:
                        mandatory.add("".join([p.lower() for p in b.split('_')]) + "Data")

                    # This regex looks for:
                    # 1. Something ending in 'Gym'
                    # 2. The NAME (Captured)
                    # 3. Something starting with 'PostBattle'
                    # Example: CeladonGymErikaPostBattleScript -> Erika
                    gym_leader = re.findall(r'(?:\w+Gym)?(\w+?)(?:PostBattle)', content)
                    logger.debug(f"Gym leaders: {gym_leader}")
                    for leader in gym_leader:
                        mandatory.add("".join([p.lower() for p in leader.split('_')]) + "Data")
                        
                
                    # this looks for the elite four, by looking for the suffixes EndBattle|AfterBattle
                    e4 = re.findall(r'(?:\w+Room|\w+Gym)?([A-Z][a-z]+)(?:EndBattle|AfterBattle)Script', content)
                    logger.debug(f"E4: {e4}")
                    for elite in e4:
                        mandatory.add("".join([p.lower() for p in elite.split('_')]) + "Data")

                        
    logger.debug(f"Mandatory Trainers: {mandatory}")
    return mandatory


# --- CORE PROCESSING ---

def process(mandatory, moves_db, base_db, parties_path):
    """
   Processes parties data and generates SQL tuples.
   :param mandatory: probable mandatory trainer battles
   :param moves_db: the dict of moves 
   :param base_db: 
   :param parties_path: the path to the parties file
   :return: tuple of SQL tuples
   """
    tuples = []

    with open(parties_path, 'r') as f:
        sections = re.split(r'(\w+Data):', f.read())
    
    mandatory_lower = {m.lower() for m in mandatory}
    for i in range(1, len(sections), 2):
        label = sections[i].lower()
        
        logger.debug(f"Processing label: {label}")
        logger.debug(f"Mandatory classes: {mandatory_lower}")
        if label not in mandatory_lower:
            logger.debug(f"Skipping label: {label}")
            continue

        teams = sections[i + 1].strip().split('\n')
        team_index = 1

        for line in teams:
            line = line.split(';')[0].strip()
            if not line.startswith('db'): continue
            parts = [p.strip() for p in line.replace('db', '').split(',') if p.strip()]

            mon_list = []

            # if it contains $FF it basically means each pokemon has its own level
            #example: db $FF, 18, PIDGEOTTO, 15, ABRA, 15, RATTATA, 17, SQUIRTLE, 0
            if parts[0] == '$FF':
                for j in range(1, len(parts) - 1, 2):
                    if parts[j] == '0': break
                    mon_list.append({'lvl': int(parts[j]), 'spec': parts[j + 1].upper()})

            # If it doesn't, and its only db, it means all pokemon have the same level
            else:
                lvl = int(parts[0])
                for j in range(1, len(parts)):
                    if parts[j] == '0' or not parts[j]: break
                    mon_list.append({'lvl': lvl, 'spec': parts[j].upper()})

            # Converts it into useful sql, 
            # Result format: (TrainerLabel, Species, Slot, Level, isAce, Moves, Condition)
            # Example: ('Cerulean City - Gym 2', 'staryu', 1, 18, FALSE, ARRAY['tackle', 'water-gun'], NULL),
            for idx, mon in enumerate(mon_list):
                condition = 'NULL'

                # if label contains rival, we need to set a condition for the team
                # ie, if the starter they have is Charmander, then the condition must be the player picked bulbasaur
                if 'rival' in label.lower() and mon['spec'] in RIVAL_STARTER_CONDITIONS:
                    team_species = [m['spec'] for m in mon_list]
                
                    for spec, cond_text in RIVAL_STARTER_CONDITIONS.items():
                        if spec in team_species:
                            condition = f"'{cond_text}'"
                            break
                                
                m = calculate_moves(mon['spec'], mon['lvl'], moves_db, base_db)
                ace = 'TRUE' if (idx + 1) == len(mon_list) else 'FALSE'
                m_sql = "ARRAY[" + ", ".join([f"'{move}'" for move in m]) + "]"
                tuples.append(
                    f"('{label}_{team_index}', '{mon['spec'].lower().replace('_', '-')}', {idx + 1}, {mon['lvl']}, {ace}, {m_sql}, {condition})")
            team_index += 1
    return tuples


def setup_logging(cwd):
    """Sets up logging to a file.
    :param cwd: The current working directory."""
    log_path = os.path.join(cwd, "pokemon_team_extractor.log")
    logging.basicConfig(filename=str(log_path), level="DEBUG",
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    setup_logging(os.getcwd())
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for gen_folder in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, gen_folder)
        if not os.path.isdir(path): continue
    
        logger.info(f"Processing folder: {gen_folder}")

        all_files = os.listdir(path)
        moves_f = next((f for f in all_files if 'moves' in f.lower() and f.endswith('.asm')), None)
        parties_f = next((f for f in all_files if 'parties' in f.lower() and f.endswith('.asm')), None)
        const_f = next((f for f in all_files if 'constants' in f.lower() and f.endswith('.asm')), None)
        logger.debug(f"Moves file: {moves_f}, Parties file: {parties_f}, Constants file: {const_f}")
        
        # File Paths
        base_stats_dir = os.path.join(path, "poke_stats")
        moves_dir = os.path.join(path, moves_f)
        scripts_dir = os.path.join(path, "scripts")
        const_dir = os.path.join(path, const_f)
        logger.debug(f"Base stats dir: {base_stats_dir}, Moves dir: {moves_dir}, Scripts dir: {scripts_dir}, Constants dir: {const_dir}")
        
        # Load libraries
        b_dict = Loaders.load_all_base_stats(base_stats_dir)
        m_dict = Loaders.load_moves(moves_dir)
        m_list = get_mandatory_labels(scripts_dir, const_dir)
        logger.debug(f"Loaded {len(m_list)} mandatory labels")

        # Process results
        results = process(m_list, m_dict, b_dict, os.path.join(path, parties_f))

        if results:
            # Map every UNIQUE milestone (e.g., 'Rival1Data_7') to its minimum level
            milestone_min_levels = {}
            for entry in results:
                # Get 'Rival1Data_7' instead of just 'Rival1Data'
                milestone_id = re.search(r"\('([^']+)'", entry).group(1)
                lvl = get_level(entry)

                if milestone_id not in milestone_min_levels or lvl < milestone_min_levels[milestone_id]:
                    milestone_min_levels[milestone_id] = lvl

            # Sort the milestone teams by level, then by ID, then by position
            results.sort(key=lambda x: (
                milestone_min_levels.get(re.search(r"\('([^']+)'", x).group(1), 0), 
                re.search(r"\('([^']+)'", x).group(1),                        
                get_slot(x)                                                     
            ))


        # Outputs our results into a sql file
        if results:
            game_names = gen_folder.split('_')
            names_formatted = ", ".join([f"'{name}'" for name in game_names])
            milestone_team_file = f"{OUTPUT_DIR}/xx_pokemon_{gen_folder}_milestone_teams_table.sql"

            with open(milestone_team_file, 'w') as f:
                f.write("-- Generated for games: " + ", ".join(game_names) + "\n")
                f.write(
                    "INSERT INTO milestone_teams (milestone_id, pokemon_id, slot, level, is_ace, moves, condition)\n")
                f.write("SELECT m.id, p.id, t.slot, t.lvl, t.ace, t.moves_arr, t.condition\n")
                f.write("FROM (VALUES\n")
                f.write(",\n".join(results))
                f.write(f"\n) AS t(stage_search, p_name, slot, lvl, ace, moves_arr, condition)\n")
                f.write("JOIN pokemon p ON p.name = t.p_name\n")
                f.write("JOIN milestones m ON m.stage_name = t.stage_search\n")
                f.write("JOIN games g ON m.game_id = g.id\n")
                f.write(f"WHERE (g.name IN ({names_formatted}) OR g.name IS NULL);\n")

            print(f"Success: {milestone_team_file} created with {len(results)} records.")
