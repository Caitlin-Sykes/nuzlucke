import logging
import re
from urllib.parse import unquote

import requests
import DatabaseConfig

class BulbapediaParser:
    """Has data parsing utilities for bulbapedia
    these will not scrape pages themselves"""

    def __init__(self, move_service):
        self.move_service = move_service
        self.logger = logging.getLogger(__name__)

    def extract_starters_dynamically(self, page):
        """Extracts starters from a given page
        by looking for a three-column three-row
        table
        :param page to be scraped"""
        self.logger.info(">> extract_starters_dynamically")
        starters = []

        for table in page.find_all("table", class_="roundy"):
            cells = table.find_all("td")
            cell_contents = [cell.get_text().strip() for cell in cells]

            if "Gift" in cell_contents:
                self.logger.debug(f"Found a Gift/Starter table. Filtering...")
                for i, content in enumerate(cell_contents):
                    if content == "Gift":
                        potential_name = cell_contents[i - 1]
                        clean_name = potential_name.replace('♂', '').replace('♀', '').strip()
                        if clean_name and clean_name[0].isupper() and clean_name != "Gift":
                            if clean_name not in starters:
                                starters.append(clean_name)

            if len(starters) == 3:
                break

        self.logger.debug(f"<< extract_starters_dynamically (Found: {starters})")
        return starters

    def extract_milestones_and_trainers(self, page, game_slug):
        """ Main loop to find headers and associate them with trainer tables
        :param page: BeautifulSoup object representing the page to extract from
        :param game_slug: slug of the game to extract for
        :return: list of milestones and trainers extracted from the page
        """
        self.logger.debug(f">> extract_milestones_and_trainers")

        milestones = []
        seen_trainers = set()

        elements = page.find_all(['h2', 'h3', 'table'])
        current_milestone = "Unknown Area"

        for element in elements:
            if element.name in ['h2', 'h3']:
                header_text = element.get_text(strip=True).replace("[edit]", "")
                if header_text not in ["Contents", "Items", "External links"]:
                    current_milestone = header_text

            elif element.name == 'table' and 'roundy' in element.get('class', []):
                header = element.find("th")
                if header and "Trainer" in header.get_text():
                    # get the trainers from the table
                    trainers_in_table = self.extract_trainers_from_table(element, game_slug)

                    unique_trainers = []
                    for t in trainers_in_table:
                        level_sum = sum(p['level'] for p in t['pokemon'])
                        fingerprint = f"{current_milestone}|{t['trainer_name']}|{level_sum}"

                        if fingerprint not in seen_trainers:
                            seen_trainers.add(fingerprint)
                            unique_trainers.append(t)
                        else:
                            self.logger.debug(f"Skipping duplicate trainer: {fingerprint}")

                    if unique_trainers:
                        milestones.append({
                            "milestone_name": current_milestone,
                            "trainers": unique_trainers
                        })
        self.logger.debug(f"<< extract_milestones_and_trainers")
        return milestones

    def extract_trainers_from_table(self, table, game_slug):
        """ Parses a specific Bulbapedia trainer table into a list of trainer dicts
        :param table: table to parse
        :param game_slug: game slug to use for the game
        :return: list of trainers in the table"""
        self.logger.debug(f">> extract_trainers_from_table")

        trainers = []
        rows = table.select("tr")
        current_trainer = None

        for row in rows:
            style_str = str(row.get('style', '')).replace(" ", "")
            if row.find("th") or "background:#34612D" in style_str:
                continue

            cells = row.find_all("td", recursive=False)
            if not cells:
                cells = row.find_all("td")
            if not cells:
                continue

            if len(cells) >= 2:
                trainer_cell = cells[0]
                pokemon_cell = cells[1]
                t_name_tag = trainer_cell.find("b")
                if t_name_tag:
                    current_trainer = {
                        "trainer_name": t_name_tag.get_text(strip=True),
                        "pokemon": []
                    }
                    trainers.append(current_trainer)
            elif len(cells) == 1 and current_trainer:
                pokemon_cell = cells[0]
            else:
                continue

            pk_link = pokemon_cell.find("a", title=re.compile(r"\(Pokémon\)")) or pokemon_cell.find("a")

            if pk_link:
                pk_name = pk_link.get_text(strip=True)
                pk_slug = pk_name.lower().replace(" ", "-").replace(".", "").replace("♂", "-m").replace("♀", "-f")
                lvl_text = pokemon_cell.get_text()
                lvl_match = re.search(r'Lv\.?\s*(\d+)', lvl_text)
                level = int(lvl_match.group(1)) if lvl_match else 0

                if level > 0 and pk_slug:
                    moves = self.move_service.get_moves(pk_slug, game_slug, level)
                    current_trainer["pokemon"].append({
                        "pokemon_slug": pk_slug,
                        "level": level,
                        "moves": moves
                    })
        self.logger.debug(f"<< extract_trainers_from_table")
        return trainers

    def get_trainer_prefix(self, element):
        """ Determines trainer significance based on preceding headers
        :param element: element to find the header
        :return battle prefix"""
        self.logger.debug(f">> get_trainer_prefix")

        prev_headers = element.find_all_previous(['h2', 'h3', 'h4'], limit=5)
        context_text = " ".join([h.get_text().lower() for h in prev_headers])

        if "champion" in context_text: return "Champion"
        if "rival" in context_text: return "Rival Battle"
        if "gym" in context_text or "leader" in context_text: return "Gym Leader"
        if any(k in context_text for k in ["boss", "rocket", "dojo", "giovanni"]):
            return "Boss Battle"
        return "Major Battle"

    def fetch_next_level_cap(self, page):
        """ Finds the max level of the very first trainer table on the page """
        self.logger.debug(">> fetch_next_level_cap")
        first_trainer = page.find("table", class_="roundy", string=lambda t: t and "Reward:" in t)
        if first_trainer:
            levels = re.findall(r"Lv\.(\d+)", first_trainer.get_text())
            if levels:
                self.logger.debug(f"<< get_trainer_prefix")
                return max(map(int, levels))
            self.logger.debug(f"<< get_trainer_prefix")
        return 5

    def get_game_slug(self, url):
        """ Dynamically extracts the game name from a Bulbapedia URL.
        :param url: URL of the page
        :return the game slug"""
        self.logger.debug(f">> get_game_slug")

        decoded_url = unquote(url)

        # Pattern 1: Look for Walkthrough:Pokémon_Name
        match = re.search(r'Walkthrough:Pokémon_([^/]+)', decoded_url)

        # Pattern 2: Look for Category:Name_walkthrough
        if not match:
            match = re.search(r'Category:([^/]+)_walkthrough', decoded_url)

        if match:
            game_part = match.group(1)
            # red_and_blue -> red-blue
            slug = game_part.lower().replace("_and_", "-").replace("_", "-").replace(" ", "-")
            slug = slug.replace("pokemon-", "")
            return slug.strip("-")

        fallback = decoded_url.split(':')[-1].split('/')[-1].lower().replace("_", "-")
        self.logger.debug(f"<< get_game_slug")
        return fallback if fallback else "unknown-game"

    def get_trainer_prefix(self, element):
        """
        Look backwards from the trainer table to find the nearest
        header and determine the trainer's significance.
        :param element: the element to find the header
        """
        self.logger.debug(f">> get_trainer_prefix")

        if not element:
            return "Major Battle"

        prev_headers = element.find_all_previous(['h2', 'h3', 'h4'], limit=5)
        context_text = " ".join([h.get_text().lower() for h in prev_headers])

        self.logger.debug(f"<< get_trainer_prefix")

        if "champion" in context_text:
            return "Champion"
            # Explicitly check for Elite Four names/keywords to fix the cap logic
        if any(k in context_text for k in ["elite four", "lorelei", "bruno", "agatha", "lance"]):
            return "Elite Four"
        if "gym" in context_text or "leader" in context_text:
            return "Gym Leader"
        if "rival" in context_text:
            return "Rival Battle"
        if any(k in context_text for k in ["boss", "rocket", "dojo", "giovanni"]):
            return "Boss Battle"
        return "Major Battle"