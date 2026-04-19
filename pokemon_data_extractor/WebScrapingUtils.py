import logging
import os
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup

from Config import Config


class WebScrapingUtils:
    """ Has all scraping utilities"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def scrape_page(self,url):
        """ Scrapes page and returns as beautiful soup object
        :param url: URL of the page to scrape
        :return: Beautiful Soup object with results from the page"""

        self.logger.info(f">> scrape_page: {url}")
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        self.logger.info("<< scrape_page")
        return BeautifulSoup(response.content, "html.parser")

    def get_pages_to_scrape(self):
        """ If the link provided in the toml contains several links
        to different parts of a playthrough, put these in a dictionary,
        otherwise return just the link

        See https://bulbapedia.bulbagarden.net/wiki/Category:Red_and_Blue_walkthrough as
        an example of a playthrough with several pages to scrape.

        :param target_url: URL to scrape
        :return dict of links to scrape or str if only one link provided"""
        self.logger.debug(">> get_pages_to_scrape")

        api_conf = Config.get("api", {})
        target_url = api_conf.get("page_to_scrape")
        parsed_uri = urlparse(target_url)
        base_url = f"{parsed_uri.scheme}://{parsed_uri.netloc}"
        content = self.scrape_page(target_url)
        try:

            # Tries to get a container containing all walkthrough links
            # Sometimes its a div, sometimes it is a table
            category_container = content.find("div", id="mw-pages")
            category_table = content.find("table", class_="roundy")

            if category_container:
                self.logger.info(f"Detected Category Container: {target_url}")
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

                self.logger.info(f"Found {len(walkthrough_links)} links")
                return walkthrough_links

            elif category_table and "Part" not in target_url:
                self.logger.info(f"Detected Category Table: {target_url}")
                walkthrough_links = {}

                # Find all links in the category
                for link in category_table.find_all("a"):
                    # Remove things like /n
                    raw_title = link.get_text().strip()

                    # Fix the 'é' issue: Replace the accented 'é' with 'e'
                    clean_title = raw_title.replace('é', 'e')

                    # Filter out the main walkthrough page if needed
                    if "Part" in clean_title or "Walkthrough" in clean_title:
                        relative_path = link.get("href")
                        full_url = urljoin(base_url, relative_path)
                        walkthrough_links[clean_title] = full_url

                self.logger.info(f"Found {len(walkthrough_links)} links")
                return walkthrough_links

            # If no category container is found, it's probably a single page
            self.logger.info(f"Detected Single page: {target_url}")
            self.logger.debug("<< get_pages_to_scrape")
            return {"Main Page": target_url}

        except Exception as e:
            self.logger.error(f"Failed to fetch {target_url}: {e}")
            return None




