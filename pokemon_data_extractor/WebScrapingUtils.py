import logging
import os
from urllib.parse import urljoin, urlparse, unquote

import requests
from bs4 import BeautifulSoup

from Config import Config
from ParseDataUtils import extract_starters_dynamically

logger = logging.getLogger(__name__)


def fetch_next_level_cap(page):
    """ Finds the max level of the very first trainer table on the page """
    # Look for the first 'roundy' table that contains 'Reward:' (standard for trainers)
    first_trainer = page.find("table", class_="roundy", string=lambda t: t and "Reward:" in t)

    if first_trainer:
        # Extract all 'Lv.X' patterns and find the highest number
        import re
        levels = re.findall(r"Lv\.(\d+)", first_trainer.get_text())
        if levels:
            return max(map(int, levels))

    return 5

def scrape_page(url):
    """ Scrapes page and returns as beautiful soup object
    :param url: URL of the page to scrape
    :return: Beautiful Soup object with results from the page"""

    logger.info(f"--- Fetching from Web: {url} ---")
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = 'utf-8'
    return BeautifulSoup(response.content, "html.parser")

def get_game_slug(url):
    """ Extracts the game slug from the given URL.
    :param url: The URL to extract the game slug from."""
    logger.debug(f">> get_game_slug: {url=}")

    parts = url.split('/')
    for part in parts:
        if "Walkthrough:" in part:
            slug = part.replace("Walkthrough:Pokémon_", "").replace("_", "-").lower()
            return unquote(slug)
    return "unknown-game"


def get_data_from_page(url):
    """ Gets and fetches the data from a given url,
    and formats into queries
    :param url: URL of the page to fetch data from"""
    logger.debug(">> get_data_from_page")
    # Get the data to be parsed
    data = scrape_page(url)
    game_slug = get_game_slug(url)
    all_stages = []
    if "part_1" in url.lower() or "part-1" in url.lower():
        logger.debug("Found part 1. Looking for starters")
        starters = extract_starters_dynamically(data)
        if starters:
            logger.info(f"Successfully identified starters: {starters}")
            first_boss_lv = fetch_next_level_cap(data)

            starter_stage = {
                "stage_name": f"Starter Selection: {', '.join(starters)}",
                "trainer_name": "N/A",
                "level_cap": first_boss_lv,
                "order_index": 1,
                "is_major_boss": False,
                "game_slug": game_slug
            }
            all_stages.append(starter_stage)
    logger.debug("<< get_data_from_page")




def get_pages_to_scrape():
    """ If the link provided in the toml contains several links
    to different parts of a playthrough, put these in a dictionary,
    otherwise return just the link

    See https://bulbapedia.bulbagarden.net/wiki/Category:Red_and_Blue_walkthrough as
    an example of a playthrough with several pages to scrape.

    :param target_url: URL to scrape
    :return dict of links to scrape or str if only one link provided"""
    logger.info(">> get_pages_to_scrape")

    debug_conf = Config.get("debug", {})
    api_conf = Config.get("api", {})
    is_debug = debug_conf.get("debug", False)
    target_url = api_conf.get("page_to_scrape")
    cache_file_name = debug_conf.get("file_to_store_local_copy", "page_cache.html")
    parsed_uri = urlparse(target_url)
    base_url = f"{parsed_uri.scheme}://{parsed_uri.netloc}"
    # Define the folder and full path
    cache_dir = os.path.join(os.getcwd(), "cache")
    cache_path = os.path.join(cache_dir, cache_file_name)

    # If in debug mode and the local cache file exists, read it
    if is_debug and os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            raw_html = f.read()
            content = BeautifulSoup(raw_html, "html.parser")
        logger.warning(f"--- Using Local Cache: {cache_path} ---")
    else:
        content = scrape_page(target_url)

        # if debug, write to cache
        if is_debug:
            # Create the 'cache' directory if it doesn't exist
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)
                logger.info(f"Created missing directory: {cache_dir}")

            with open(cache_path, "w", encoding="utf-8") as f:
                f.write(content.prettify())
            logger.info(f"--- Cached local copy to {cache_path} ---")
    try:

        # Tries to get a container containing all walkthrough links
        category_container = content.find("div", id="mw-pages")
        if category_container:
            logger.info(f"Detected Category page: {target_url}")
            walkthrough_links = {}

            # Find all links in the category
            for link in category_container.find_all("a"):
                # Remove things like /n
                raw_title = link.get_text().strip()

                # Fix the 'é' issue: Replace the accented 'é' with 'e'
                clean_title = raw_title.replace('é', 'e')

                # Filter out the main walkthrough page if needed
                if "Part" in clean_title or "Walkthrough" in clean_title:
                    relative_path = link.get("href")
                    full_url = urljoin(base_url, relative_path)
                    walkthrough_links[clean_title] = full_url

            logger.info(f"Found {len(walkthrough_links)} links")
            return walkthrough_links

        # If no category container is found, it's probably a single page
        logger.info(f"Detected Single page: {target_url}")
        return {"Main Page": target_url}

    except Exception as e:
        logger.error(f"Failed to fetch {target_url}: {e}")
        return None
