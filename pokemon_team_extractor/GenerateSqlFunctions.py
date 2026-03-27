import logging
import re

OUTPUT_DIR = "output"
logger = logging.getLogger(__name__)

def generate_milestones_sql(mandatory_labels, trainer_results, game_slug):
    """Generates the SQL for populating the milestone_stages table.
    :param mandatory_labels: The mandatory labels.
    :param trainer_results: The results of the trainer processing.
    :param game_slug: The slug of the game. (i.e., red-blue for pokemon red and blue)"""
    # Map internal labels to their highest level
    caps_lookup = {}
    for entry in trainer_results:
        # entry looks like: ('brockdata_1', 'onix', 1, 14, TRUE, ...)
        # We need to extract 'brockdata' and 14
        m = re.search(r"\('([^']+)_(\d+)',\s*'[^']+',\s*\d+,\s*(\d+)", entry)
        if m:
            full_label, team_idx, lvl = m.groups()
            label_base = full_label.lower().split('_')[0]
            lvl = int(lvl)

            if label_base not in caps_lookup or lvl > caps_lookup[label_base]:
                caps_lookup[label_base] = lvl
                logger.debug(f"Cap found: {label_base} -> {lvl}")

    # Process categories - we don't want general routes in here
    categories = ['Gyms', 'Rivals', 'Elite4', 'Champion']
    all_milestones = []

    for cat in categories:
        for m in mandatory_labels[cat]:
            clean_label = m['internal_label'].lower()

            m['cap'] = caps_lookup.get(clean_label, 0)

            all_milestones.append(m)

    # Sort by Level Cap
    all_milestones.sort(key=lambda x: x['cap'])

    stage_values = []

    for idx, m in enumerate(all_milestones):
        order_idx = idx + 1
        # Escape single quotes for SQL (e.g. Lt. Surge's Room)
        s_name = m['stage'].replace("'", "''")
        t_name = m['trainer'].replace("'", "''")

        stage_values.append(f"('{game_slug}', '{s_name}', {m['cap']}, {order_idx})")

    # create the query
    with open(f"{OUTPUT_DIR}/populate_{game_slug}_milestones.sql", "w") as f:
        f.write("-- Nuzlocke Milestones\n")
        if stage_values:
            f.write("INSERT INTO milestone_stages (game_slug, stage_name, level_cap, order_index) VALUES\n")
            f.write(",\n".join(stage_values) + ";\n\n")

    print(f"SQL generated. {len(all_milestones)-1} boss stages processed.")


def generate_milestone_trainers_sql(mandatory_labels, trainer_results, game_slug):
    """
    Generates SQL for ALL individual trainers.
    Links them to their specific location stages using the Routes data.
    """
    # 1. Build a Comprehensive Lookup: internal_label -> Stage Name
    # This combines Bosses and the Route trainers you extracted in Main.py
    stage_lookup = {}
    for cat, entries in mandatory_labels.items():
        for entry in entries:
            if isinstance(entry, dict) and 'internal_label' in entry:
                label_key = entry['internal_label'].lower()
                # We store the stage name (e.g., 'Route 1' or 'Pewter Gym')
                stage_lookup[label_key] = entry['stage']

    sql_output = ["-- Nuzlocke Trainer Milestone Links", "BEGIN;"]
    sql_output.append(f"\n-- DATA FOR: {game_slug.upper()}")

    trainer_lines = []
    processed_teams = set() # Track unique 'youngsterdata_1', etc.

    for entry in trainer_results:
        # 2. Extract specific team identity: ('youngsterdata_1', 'rattata', ...)
        m = re.search(r"\('([^']+)_(\d+)'", entry)
        if not m:
            continue

        label_base = m.group(1) # e.g., youngsterdata
        team_idx = m.group(2)   # e.g., 1
        full_internal_id = f"{label_base}_{team_idx}" # youngsterdata_1

        # Only create ONE entry per team (not one per Pokemon)
        if full_internal_id in processed_teams:
            continue
        processed_teams.add(full_internal_id)

        # 3. Find the Stage Name
        label_lower = label_base.lower()

        # Check if we found this trainer in a specific location during script parsing
        if label_lower in stage_lookup:
            stage_name = stage_lookup[label_lower]
        else:
            # Fallback for trainers that weren't found in a specific script
            stage_name = f"Misc: {label_base.replace('Data', '')}"

        # 4. Determine Display Name
        # Result: 'Youngster 1', 'Brock', 'Hiker 5'
        clean_name = label_base.replace('Data', '').replace('data', '').capitalize()
        is_boss = label_lower in [l.lower() for l in ['Gyms', 'Rivals', 'Elite4', 'Champion']]

        display_name = clean_name if is_boss else f"{clean_name} {team_idx}"

        s_name_sql = stage_name.replace("'", "''")
        t_name_sql = display_name.replace("'", "''")

        # 5. Link to the stage table via subquery
        stage_id_sub = (
            f"(SELECT id FROM milestone_stages "
            f"WHERE stage_name = '{s_name_sql}' AND game_slug = '{game_slug}')"
        )

        trainer_lines.append(f"({stage_id_sub}, '{t_name_sql}', {'TRUE' if is_boss else 'FALSE'}, '{full_internal_id}')")

    if trainer_lines:
        sql_output.append("INSERT INTO milestone_trainers (stage_id, trainer_name, is_major_boss, internal_label) VALUES")
        sql_output.append(",\n".join(trainer_lines) + ";")

    sql_output.append("\nCOMMIT;")

    filename = f"{OUTPUT_DIR}/xx_populate_{game_slug}_milestone_trainers.sql"
    with open(filename, "w") as f:
        f.write("\n".join(sql_output))

    print(f"Generated {len(trainer_lines)} trainers linked to locations.")