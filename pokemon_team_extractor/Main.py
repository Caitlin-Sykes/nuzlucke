import re
import logging
import os

DATA_DIR = "./data"
logger = logging.getLogger(__name__)

def get_mandatory_labels(folder):
    """
    Extracts Trainer Classes (e.g., Rocket) from map scripts.
    Matches dw_const or TrainerHeader usage.
    :param folder: Folder containing map scripts.
    :return: Set of mandatory trainer classes
    """
    mandatory_classes = set()

    # For every file in the folder
    for root, _, files in os.walk(folder):
        # for every asm file
        for file in files:
            if file.endswith('.asm'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as mf:
                    content = mf.read()
                    
                    # Look for any TrainerHeader files
                    # example: MtMoon3TrainerHeader0
                    headers = re.findall(r'(\w+?)TrainerHeader\d+', content)
                    logger.debug(f"Found headers: {headers}")
                    
                    
                    #Look for Class Names in text pointers 
                    #example MtMoonB2FRocket1BattleText)
                    text_classes = re.findall(r'dw_const\s+\w+?([A-Z][A-Za-z0-9]+?)\d+Text', content)
                    logger.debug(f"Found text classes: {text_classes}")
                    
                    
                    for h in headers: mandatory_classes.add(h)
                    for c in text_classes: mandatory_classes.add(c)

    final_labels = {c + "Data" for c in mandatory_classes}
    logger.debug(f"Found mandatory classes: {final_labels}")
    return final_labels

def load_moves(filepath):
    """
    Loads moves data from a file.
    :param filepath: Path to the moves file.
    :return: Dictionary of moves data.
    """
    db = {}
  
    with open(filepath, 'r') as f:
        content = f.read()
    curr = None
    for line in content.split('\n'):
        s_match = re.match(r'^(\w+)EvosMoves:', line)
        if s_match: curr = s_match.group(1).upper(); db[curr] = []
        m_match = re.match(r'^db\s+(\d+),\s+(\w+)', line.strip())
        if m_match and curr: db[curr].append((int(m_match.group(1)), m_match.group(2).lower().replace('_', '-')))
    return db

def calculate_moves(species, level, db):
    spec = species.upper()
    if spec not in db: return ['NO DATA']
    available = [m[1] for m in db[spec] if m[0] <= level]
    return available[-4:] if available else ['NO DATA']

def process(mandatory, moves_db, parties_path):
    """
    Processes parties data and generates SQL tuples.
    :param mandatory: probable mandatory trainer battles
    :param moves_db: the dict of moves 
    :param parties_path: the path to the parties file
    :return: tuple of SQL tuples
    """
    tuples = []

    with open(parties_path, 'r') as f:
        # splits where it finds a word followed by "Data" and a colon
        sections = re.split(r'(\w+Data):', f.read())

    for i in range(1, len(sections), 2):
        label = sections[i]
        
        logger.debug(f"Processing label: {label}")
        logger.debug(f"Mandatory classes: {mandatory}")
    
        # if the label is not in mandatory, skip to the next iteration
        # is likely an optional file
        if label not in mandatory:
            logger.warning(f"Skipping label found in parties file: {label} (not in mandatory list)")
            continue
        
        data_block = sections[i+1].strip()
        teams = data_block.split('\n')

        team_index = 1
        for line in teams:
            line = line.split(';')[0].strip() # Remove comments
            if not line.startswith('db'): continue

            raw_parts = line.replace('db', '').strip().split(',')
            parts = [p.strip() for p in raw_parts if p.strip()]

            if not parts: continue

            mon_list = []
           
            # if it contains $FF it basically means each pokemon has its own level
            #example: db $FF, 18, PIDGEOTTO, 15, ABRA, 15, RATTATA, 17, SQUIRTLE, 0
            if parts[0] == '$FF':
                for j in range(1, len(parts)-1, 2):
                    if parts[j] == '0': break
                    mon_list.append({'lvl': int(parts[j]), 'spec': parts[j+1]})
                    
            # If it doesn't, and its only db, it means all pokemon have the same level
            else:
                lvl = int(parts[0])
                for j in range(1, len(parts)):
                    if parts[j] == '0': break
                    mon_list.append({'lvl': lvl, 'spec': parts[j]})

            # Converts it into useful sql, 
            # Result format: (TrainerLabel, Species, Slot, Level, isAce, Moves, Condition)
            # Example: ('Cerulean City - Gym 2', 'staryu', 1, 18, FALSE, ARRAY['tackle', 'water-gun'], NULL),
            for idx, mon in enumerate(mon_list):
                m = calculate_moves(mon['spec'], mon['lvl'], moves_db)
                ace = 'TRUE' if (idx + 1) == len(mon_list) else 'FALSE'
                moves_sql = "ARRAY[" + ", ".join([f"'{move}'" for move in m]) + "]"
               
                tuples.append(f"('{label}_{team_index}', '{mon['spec'].lower()}', {idx+1}, {mon['lvl']}, {ace}, {moves_sql}, NULL)")

            team_index += 1

    return tuples

def setup_logging(cwd):
    log_path = os.path.join(cwd, "pokemon_team_extractor.log")
    logging.basicConfig(filename=str(log_path), level="WARNING",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    setup_logging(base_dir)
    
    if not os.path.exists(DATA_DIR):
        print(f"Directory {DATA_DIR} not found.")
        exit()
        
    # for each game folder in data
    for gen_folder in os.listdir(DATA_DIR):
        logger.info(f"Processing {gen_folder}...")
        
        # gets the path of each game_folder in /data
        game_folder_path = os.path.join(DATA_DIR, gen_folder)
        
        #gets all files in the gen_folder
        all_files = os.listdir(f"{game_folder_path}")
        
        # tries to find moves_file_name by looking for files containing "moves" in the name
        moves_file_name = next((f for f in all_files if re.search(r'moves', f, re.I) and f.endswith('.asm')), None)

        # tries to find parties_file_name by looking for files containing "parties" in the name
        parties_file_name = next((f for f in all_files if re.search(r'parties', f, re.I) and f.endswith('.asm')), None)
        
        logger.info(f"Moves file: {moves_file_name} and Parties file: {parties_file_name}.")
        
        # Basically gets any trainer that has some kind of map data attached to them
        # usually a good indicator of it being an unavoidable battle
        m_list = get_mandatory_labels(f"{game_folder_path}/scripts")

        # loads the moves data into a dict
        m_dict = load_moves(f"{game_folder_path}/{moves_file_name}") if moves_file_name else {exit("Cannot find file containing moves data. Please check the file name contains 'moves'")}

        # it gets the name of the games its applying to from the name of the folder
        # and splits it by underscore
        #ie, red_blue becomes ["red", "blue"]
        game_names = gen_folder.split('_')
        
        # Format them for the SQL IN clause: ('red', 'blue')
        names_formatted = ", ".join([f"'{name}'" for name in game_names])
        
        results = process(m_list, m_dict, f"{game_folder_path}/{parties_file_name}")

        OUTPUT_DIR = "output"
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            logger.info(f"Created missing directory: {OUTPUT_DIR}")
    
        OUTPUT_FILE = f"{OUTPUT_DIR}/xx_pokemon_{gen_folder}_milestone_teams_table.sql"      
        
        if results:
            with open(OUTPUT_FILE, 'w') as f:
                # Start the Insert
                f.write("INSERT INTO milestone_teams (milestone_id, pokemon_id, slot, level, is_ace, moves, condition)\n")
        
                # Start the Select from the Virtual Table (the 't' values)
                f.write("SELECT m.id, p.id, t.slot, t.lvl, t.ace, t.moves_arr, t.condition\n")
                f.write("FROM (VALUES\n")
        
                # Write the actual data rows
                f.write(",\n".join(results))
        
                # Close the Values block and perform the Joins
                f.write(f"\n) AS t(stage_search, p_name, slot, lvl, ace, moves_arr, condition)\n")
                f.write("JOIN pokemon p ON p.name = t.p_name\n")
                f.write("JOIN milestones m ON m.stage_name = t.stage_search\n")
                f.write("JOIN games g ON m.game_id = g.id\n")
        
                # The Filter: matches your folder names and handles the NULL requirement
                f.write(f"WHERE (g.name IN ({names_formatted}) OR g.name IS NULL);\n")
        else:
            logger.info("Still 0 matches. Double check your folder names.")