import logging
import re
from BattleParser import BattleParser
from BulbapediaParser import BulbapediaParser
from WebScrapingUtils import WebScrapingUtils
from MoveService import MoveService
from SqlIntegration import SqlIntegration

logger = logging.getLogger(__name__)


def get_data_from_page(url, save_to_db=True):
    logger.debug(f">> get_data_from_page: {url}")

    # Initialize necessary services
    scraper = WebScrapingUtils()
    move_service = MoveService()
    bulb_parser = BulbapediaParser(move_service)
    battle_parser = BattleParser()
    sql_writer = SqlIntegration()
    soup_data = scraper.scrape_page(url)
    game_slug = bulb_parser.get_game_slug(url)

    if not game_slug:
        return [], [], 5

    # Extract Standard Trainers & Areas
    raw_milestones = bulb_parser.extract_milestones_and_trainers(soup_data, game_slug)

    # Clean and Group Milestones (Merge "Route 1 - North" and "Route 1 - South")
    all_milestones = []
    for m in raw_milestones:
        clean_name = re.split(r' - | \(|: | \d+[FfBb]', m['milestone_name'])[0].strip()
        existing = next((gm for gm in all_milestones if gm['milestone_name'] == clean_name), None)
        if existing:
            existing['trainers'].extend(m['trainers'])
        else:
            m['milestone_name'] = clean_name
            all_milestones.append(m)

    # Extract Major Battles (Rivals/Bosses)
    rivals = battle_parser.extract_rival_battles(soup_data)
    for rival in rivals:
        if 'pokemon_team' in rival:
            rival['pokemon'] = rival.pop('pokemon_team')
        rival['is_major_boss'] = True

        # Identify if this is a Gym Leader, Rival, etc.
        node = rival.get('element_node')
        prefix = bulb_parser.get_trainer_prefix(node) if node else "Major Battle"
        t_name = rival['trainer_name']
        target_milestone_name = f"{prefix}: {t_name}"

        # Try to attach the boss to an existing milestone (e.g., Brock to Pewter City)
        found_home = False
        for milestone in all_milestones:
            m_name = milestone['milestone_name'].lower()
            if t_name.lower() in m_name or "gym" in m_name:
                milestone['trainers'].append(rival)
                milestone['milestone_name'] = target_milestone_name
                found_home = True
                break

        if not found_home:
            all_milestones.append({"milestone_name": target_milestone_name, "trainers": [rival]})

    # Handle Starters
    starters = bulb_parser.extract_starters_dynamically(soup_data)

    # Calculate max level for this specific page
    local_levels = [p['level'] for m in all_milestones for t in m['trainers'] for p in t.get('pokemon', [])]
    page_max_lv = max(local_levels) if local_levels else 5

    if save_to_db:
        logger.debug("Saving to db")
        sql_writer.save_scraped_data_to_db(all_milestones, starters, page_max_lv, game_slug)
    logger.debug(f"<< get_data_from_page")
    return all_milestones, starters, page_max_lv