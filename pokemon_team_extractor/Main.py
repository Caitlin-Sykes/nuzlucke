import re
import logging
import os
from collections import defaultdict

import Loaders;
from Constants import RIVAL_STARTER_CONDITIONS
from GenerateSqlFunctions import OUTPUT_DIR, generate_milestone_trainers_sql
from Helpers import format_string, filename_to_location, format_location_name
from GenerateSqlFunctions import generate_milestones_sql

DATA_DIR = "./data"
logger = logging.getLogger(__name__)
Loaders = Loaders.Loaders()
MILESTONE_STAGES = []

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

    # Adds the level up moves that the species should have learnt
    if spec in moves_db:
        for m_lvl, m_name in moves_db[spec]:
            if m_lvl <= level:
                if m_name not in current_moves:
                    current_moves.append(m_name)
            else:
                break

  
    final = current_moves[-4:]
    logger.debug(f"Moves for {spec} at level {level}: {final}")
    return final if final else ['no-data']

def get_mandatory_labels(scripts_folder, constant_file):
    """
   Extracts Trainer Classes (e.g., Rocket) from map scripts.
   Matches dw_const or TrainerHeader usage.
   :param scripts_folder: Folder containing map scripts.
   :param constant_file: file containing trainer ids
   :return: dict of mandatory trainer classes
   """

    # loads all trainer ids based on the file
    id_map = Loaders.load_trainer_constants(constant_file)
    
    #Used to keep track of trainers we already have so we don't dupe the data
    already_categorized = set()
    
    logger.debug(f"All trainer_ids {id_map}")
    # Initialise a dictionary that automatically creates a list for new keys
    mandatory = defaultdict(list)
    
    # for every script in the scripts folder
    for root, _, files in os.walk(scripts_folder):
        for file in files:
            if file.endswith('.asm'):
                # This creates a location name by removing the file extension and adding a space between vars
                location_name = filename_to_location(file)
                logger.debug(f"Location Name: {location_name}")

                with open(os.path.join(root, file), 'r', errors='ignore') as f:
                    content = f.read()

                    # Looks for key words EVENT_BEAT_(\w+)_ROOM, to fetch Elite 4
                    e4 = re.findall(r'EVENT_BEAT_(\w+)_ROOM', content)

                    # For all elite 4 returned from regex
                    for elite in set(e4):
                        logger.debug(f"Elite 4: {elite}")
                        if "Room" in location_name:
                            milestone = format_string(location_name, r"^(\w+?)(?:'s|s)?\s*Room$", r"Elite Four: \1")
                            elite.capitalize()
                            already_categorized.add(f"{location_name}")
                            trainer_clean = elite.capitalize().strip('s')
                            mandatory["Elite4"].append({
                                "stage": milestone,
                                "trainer": trainer_clean,
                                "internal_label": f"{trainer_clean}Data"
                            })

                    # Gets the champion fight
                    # Looks for the event to determine if this trainer is the champion, returns first result
                    champion = re.search(r'HALL_OF_FAME|WalkToHallOfFame', content)                 
                    if champion:
                        #Do a further search for the event beat to try and determine the name:
                        champion_string = re.search(r'EVENT_BEAT_CHAMPION_([A-Z0-9_]+)', content, flags=re.IGNORECASE)
                        champ_name = champion_string.group(1)
                        logger.debug(f"Champion: {champion_string.group(1)}")
                        # If it contains rival, we do a slightly different formatting
                        if "RIVAL" in champ_name:
                            milestone = "Champion: Rival"
                        else:
                            milestone = format_string(champ_name, r"^(\w+?)(?:'s|s)?\s*Room$", r"Champion: \1")
                        already_categorized.add(f"{location_name}")
                        mandatory["Champion"].append({
                            "stage": milestone,
                            "trainer": "Rival" if "RIVAL" in champ_name else champ_name.capitalize(),
                            "internal_label": "Rival3Data" if "RIVAL" in champ_name else f"{champ_name}Data"
                        })
                 
                    # Gets all the rival encounters by looking for certain keywords
                    rivals = re.findall(r'\b(?:RIVAL_CHALLENGES|OPP_[A-Z0-9_]+|RIVAL[0-9]_START_BATTLE)\b', content)

                    for rival in rivals:
                        # Rival1 = Early game, Rival2 = Mid game, Rival3 = Champion
                        if "Oaks Lab" in location_name or "Route22" in location_name or "Cerulean City" in location_name:
                            parties_label = "Rival1Data"
                        elif "SSAnne" in location_name or "Pokemon Tower" in location_name or "Silph Co" in location_name:
                            parties_label = "Rival2Data"
                        else:
                            parties_label = "Rival3Data"
                    
                        mandatory["Rivals"].append({
                            "stage": f"Rival: {location_name}",
                            "trainer": "Rival",
                            "internal_label": parties_label
                        })          

                    # Gets all the gym leaders by looking for certain keywords
                    gym_leader = re.search(r'(?:\w+Gym)?(\w+?)(?:PostBattle)', content)
                
                    if gym_leader:
                        # Gets the first occcurence
                        leader_name = gym_leader.group(1)
                        #Exclude things that shouldn't be gym leaders
                        if "Route" in leader_name or "Snorlax" in leader_name or "Dojo" in leader_name:
                            continue;
                        # Handle Lt Surge as a exception due to the "Lt"
                        if "LTSurge" in leader_name:
                            milestone = "Vermilion Gym Leader: Lt Surge"
                        else:
                            before_formatted=location_name+" "+leader_name
                            milestone = format_string(before_formatted, r'^(.+)\s+(\w+)$', r'\1 Leader: \2')
                        already_categorized.add(f"{location_name}")
                        mandatory["Gyms"].append({
                            "stage": location_name if "Gym" in location_name else f"{location_name} Gym",
                            "trainer": "Lt Surge" if "LTSurge" in leader_name else leader_name,
                            "internal_label": f"{leader_name}Data"
                        })
                        logger.debug(f"Gym leader found: {leader_name}, {milestone}")


                    # Gets all the misc battles
                    ids = re.findall(r'trainer\s+EVENT_[A-Z0-9_]+,\s*(\d+)', content)
                    for fid in ids:
                        if int(fid) in id_map:
                            label = id_map[int(fid)]
                            if location_name in already_categorized or label == "NobodyData":
                                continue

                            milestone = format_location_name(location_name)

                            if label not in [r['internal_label'] for r in mandatory["Routes"]]:
                                mandatory["Routes"].append({
                                    "stage": milestone,
                                    "trainer": label.replace('Data', ''),
                                    "internal_label": label
                                })

    return mandatory


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


    mandatory_lower = set()
    for category, items in mandatory.items():
        for item in items:
            # If item is a dict (Gyms, Rivals, Elite4), extract the internal_label
            if isinstance(item, dict) and 'internal_label' in item:
                mandatory_lower.add(item['internal_label'].lower())
            # If item is a string (Routes), add it directly
            elif isinstance(item, str):
                mandatory_lower.add(item.lower())

    for i in range(1, len(sections), 2):
        label = sections[i].lower()

        # Now 'mistydata', 'brockdata', etc., will match correctly
        if label not in mandatory_lower:
            logger.debug(f"Skipping non-mandatory label: {label}")
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

def build_stage_map(mandatory_labels, mandatory_map):
    # Sort labels by their expected level/order 
    temp_list = []
    for label in mandatory_labels:
        raw = label.lower()
        temp_list.append({
            'label': raw,
            'location': mandatory_map.get(raw, "Kanto"),
            'is_boss': any(x in raw for x in ['gym', 'elite', 'giovanni', 'brock', 'misty'])
        })

    # Backward pass to assign the "Gym" context
    stage_lookup = {}
    current_context = "Indigo Plateau"

    # IMPORTANT: Ensure temp_list is sorted by game progression here
    for i in range(len(temp_list) - 1, -1, -1):
        item = temp_list[i]
        if item['is_boss'] and "Gym" in item['location']:
            current_context = item['location']

        # If it's a Rival, keep it unique, otherwise use the context
        if 'rival' in item['label']:
            stage_lookup[item['label']] = "Rival Battle"
        else:
            stage_lookup[item['label']] = current_context

    return stage_lookup

def generate_milestone_metadata(results, game_slug, mandatory_map):
    """Generates the metadata table for milestones.
    :param results: The results of the process function.
    :param game_slug: The slug of the game.
    :param mandatory_map: The map of mandatory labels to locations.
    :return: A list of SQL tuples representing the metadata table."""
    
    temp_rows = []
    seen_ids = set()

    for entry in results:
        # Regex to pull (ID, Species, Slot, Level, isAce)
        m = re.search(r"\('([^']+)',\s*'[^']+',\s*\d+,\s*(\d+),\s*(\w+)", entry)
        if not m: continue
        m_id, lvl, is_ace = m.groups()

        if is_ace == 'TRUE' and m_id not in seen_ids:
            seen_ids.add(m_id)
            raw_label = m_id.split('_')[0].lower().replace('data', '')
            if raw_label == 'ltsurge':
                raw_label = 'Lt. Surge'
            elif raw_label == 'jrtrainerm':
                raw_label = 'Jr Trainer'
            elif 'rival' in raw_label:
                raw_label = "Rival"
            else:
                raw_label = raw_label.capitalize()
                
            # Identify Trainer Type
            # todo: make future proof
            logger.debug(f"Raw label: {raw_label}")
            is_boss = any(x in raw_label for x in ['gym', 'elite', 'giovanni', 'brock', 'misty', 'surge', 'erika', 'koga', 'sabrina', 'blaine', 'lorelei', 'bruno', 'agatha', 'lance'])
            is_rival = 'rival' in raw_label

            temp_rows.append({
                'm_id': m_id,
                'trainer': raw_label,
                'lvl': int(lvl),
                'is_boss': is_boss,
                'is_rival': is_rival,
                'location': mandatory_map.get(raw_label, "Kanto")
            })

    # Sort everything by Ace Level so the backward pass works chronologically
    temp_rows.sort(key=lambda x: x['lvl'])

    # We look forward to find the next Gym/Boss to name the "Stage"
    current_stage_context = "Indigo Plateau"
    for i in range(len(temp_rows) - 1, -1, -1):
        row = temp_rows[i]

        # If it's a Gym Leader or Giovanni, they set the context for everyone BEFORE them
        if row['is_boss'] and ("Gym" in row['location'] or "Giovanni" in row['trainer']):
            current_stage_context = row['location']

  
        row['display_name'] = current_stage_context

    # Final formatting
    final_meta_rows = []
    for idx, row in enumerate(temp_rows):
        # (game_slug, internal_id, stage_display, trainer_display_name, ace_lvl, order, is_major)
        line = f"('{game_slug}', '{row['display_name']}', '{row['trainer']}', {row['lvl']}, {idx + 1}, {'TRUE' if row['is_boss'] or row['is_rival'] else 'FALSE'})"
        final_meta_rows.append(line)

    return final_meta_rows
    
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
        logger.debug(f"Mandatory Labels: {m_list}")

        # formats game slug
        game_slug = gen_folder.lower().replace('_', '-')
        # Process results
        results = process(m_list, m_dict, b_dict, os.path.join(path, parties_f))
        
        # Generate the List of Milestone Stages
        generate_milestones_sql(m_list,results, game_slug)

        # Generates the list of trainers per milestone
        # generate_milestone_trainers_sql(m_list, results, game_slug)
        
        
        
        # if results:
        #     # Map every UNIQUE milestone (e.g., 'Rival1Data_7') to its minimum level
        #     milestone_min_levels = {}
        #     for entry in results:
        #         # Get 'Rival1Data_7' instead of just 'Rival1Data'
        #         milestone_id = re.search(r"\('([^']+)'", entry).group(1)
        #         lvl = get_level(entry)
        # 
        #         if milestone_id not in milestone_min_levels or lvl < milestone_min_levels[milestone_id]:
        #             milestone_min_levels[milestone_id] = lvl
        # logger.debug(f"Results: {results}")
        # Outputs our results into a sql file
        # if results:
        #     milestone_min_levels = {}
        #     for entry in results:
        #         m_id = re.search(r"\('([^']+)'", entry).group(1)
        #         lvl = get_level(entry)
        #         if m_id not in milestone_min_levels or lvl < milestone_min_levels[m_id]:
        #             milestone_min_levels[m_id] = lvl
        # 
        #     results.sort(key=lambda x: (
        #         milestone_min_levels.get(re.search(r"\('([^']+)'", x).group(1), 0),
        #         re.search(r"\('([^']+)'", x).group(1),
        #         get_slot(x)
        #     ))
        # 
        #     # Generate Metadata Rows
        # game_slug = gen_folder.lower().replace('_', '-')
        # meta_results = generate_milestone_metadata(results, game_slug, m_list)
        # logger.debug(f"Metadata: {meta_results}")
        #     meta_results.sort(key=lambda x: (
        #         milestone_min_levels.get(re.search(r"\('([^']+)'", x).group(1), 0),
        #         re.search(r"\('([^']+)'", x).group(1),
        #         get_slot(x)
        #     ))
        # 
        #     # Milestones
        #     milestone_table_file = f"{OUTPUT_DIR}/xx_populate_{gen_folder}_milestones_table.sql"
        #     with open(milestone_table_file, 'w') as f:
        #         f.write(f"-- Milestone Headers for {gen_folder}\n")
        #         f.write("INSERT INTO milestones (game_slug, stage_name, trainer_name, level_cap, order_index, is_major_boss)\nVALUES\n")
        #         f.write(",\n".join(meta_results) + ";")

            # Milestone Teams
            # milestone_team_file = f"{OUTPUT_DIR}/xx_pokemon_{gen_folder}_milestone_teams_table.sql"
            # game_names = gen_folder.split('_')
            # names_formatted = ", ".join([f"'{name}'" for name in game_names])
            # 
            # with open(milestone_team_file, 'w') as f:
            #     f.write(f"-- Teams for {gen_folder}\n")
            #     f.write("INSERT INTO milestone_teams (milestone_id, pokemon_id, slot, level, is_ace, moves, condition)\n")
            #     f.write("SELECT m.id, p.id, t.slot, t.lvl, t.ace, t.moves_arr, t.condition\nFROM (VALUES\n")
            #     f.write(",\n".join(results))
            #     f.write("\n) AS t(stage_search, p_name, slot, lvl, ace, moves_arr, condition)\n")
            #     f.write("JOIN pokemon p ON p.name = t.p_name\n")
            #     f.write("JOIN milestones m ON m.stage_name = t.stage_search\n") # Joins on 'Rival1Data_1'
            #     f.write("JOIN games g ON m.game_id = g.id\n")
            #     f.write(f"WHERE g.name IN ({names_formatted});\n")
            # 
            # print(f"Success: {gen_folder} processed.")
    
            