import logging
import os
from Config import Config
from WebScrapingUtils import get_data_from_page, get_pages_to_scrape


def setup_logging():
    logging_conf = Config.get("logging", {})
    file_name = logging_conf.get("logging_file_name", "default.log")

    level = getattr(logging, logging_conf.get("logging_level", "INFO"))

    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(base_dir, file_name)

    logging.basicConfig(filename=str(log_path), level=level,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')




if __name__ == "__main__":
    if not Config:
        print("ERROR: Configuration file not found or is empty!")
    else:
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Application started.")

        target_url = Config.get("api", {}).get("page_to_scrape")

        if target_url:
            logger.info(f"Target URL identified: {target_url}")
            pages = get_pages_to_scrape()
            is_single_page = len(pages) == 1
            logger.info(f"Found links: {pages}")

            if pages:
                all_game_battles = []
                for page_title in (pages.keys()):
                    logger.info(f"--- Scraping Battles from: {page_title} ---")
                    page_url = pages[page_title]
                    # Skip the first page, because it's the main page
                    if not is_single_page and "/" not in page_title:
                        logger.warning(f"Skipping {page_title} because it is the index page. ")
                        continue
                    get_data_from_page(page_url)
                    break;
        else:
            logger.error("No 'page_to_scrape' found in config.toml")