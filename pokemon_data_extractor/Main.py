import logging
import os

from BulbapediaParser import BulbapediaParser
from Config import Config
from DataOrchestrator import get_data_from_page
from MoveService import MoveService
from WebScrapingUtils import WebScrapingUtils
from SqlIntegration import SqlIntegration


def setup_logging():
    """ Setup a logger based on Config.toml """
    logging_conf = Config.get("logging", {})
    file_name = logging_conf.get("logging_file_name", "pokemon_data_extractor.log")
    level_str = logging_conf.get("logging_level", "INFO")
    level = getattr(logging, level_str.upper(), logging.INFO)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(base_dir, file_name)

    logging.basicConfig(
        filename=str(log_path),
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)

    if not Config:
        logger.error("Configuration file not found!")
    else:
        utils = WebScrapingUtils()
        sql_writer = SqlIntegration()
        move_service = MoveService()
        bulb_parser = BulbapediaParser(move_service)

        target_url = Config.get("api", {}).get("page_to_scrape")

        if target_url:
            #Get the list of pages (Walkthrough Part 1, Part 2, etc.)
            pages = utils.get_pages_to_scrape()
            master_milestones = []
            master_starters = []

            final_slug = bulb_parser.get_game_slug(target_url)

            if pages:
                for page_title, page_url in pages.items():
                    logger.info(f"Processing: {page_title}")

                    #Extract data using Orchestrator (save_to_db=False so we can consolidate)
                    p_milestones, p_starters, p_cap = get_data_from_page(page_url, save_to_db=False)

                    master_milestones.extend(p_milestones)

                    #Only capture starters from the beginning of the game
                    if any(key in page_title.lower() for key in ["part 1", "pallet", "starter"]):
                        if p_starters and not master_starters:
                            master_starters = p_starters

                # This ensures the level cap for a route is the level of the NEXT boss
                current_cap = 5
                for m in reversed(master_milestones):
                    boss_levels = [p['level'] for t in m.get('trainers', [])
                                   if t.get('is_major_boss')
                                   for p in t.get('pokemon', [])]

                    if boss_levels:
                        current_cap = max(boss_levels)

                    m['level_cap'] = current_cap

                if master_milestones:
                    sql_writer.save_scraped_data_to_db(master_milestones, master_starters, 5, final_slug)
                    logger.info(f"Consolidated SQL generated for {final_slug}")