import logging
import re

class BattleParser:
    """ Parses battle data from a given page and extracts relevant information. """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def extract_rival_battles(self, page):
        """ Extracts all the rival battles from the page
        :param page: BeautifulSoup page object to extract from"""
        self.logger.debug(">> extract_rival_battles")
        all_battles = []

        # For all the party containers in the page
        for party_container in page.find_all("div", class_="partycontainer"):

            trainer_name, is_major_boss = self._get_trainer_name(party_container)

            condition = self._get_team_condition(party_container)

            trainer_data = {
                "trainer_name": trainer_name,
                "is_major_boss": is_major_boss,
                "element_node": party_container,
                "condition": condition,
                "pokemon_team": []
            }

            # things with the class PKMN box is usually a team
            poke_boxes = party_container.find_all("div", class_="PKMNbox")
            for index, pb in enumerate(poke_boxes, start=1):
                clean_name, level = self._get_pokemon_name_and_level(pb)

                # Get the ability
                ability = self._get_ability_text(pb)

                pk = {
                    "pokemon_slug": clean_name.lower(),
                    "slot_number": index,
                    "level": level,
                    "is_ace": False,
                    "moves": [m.get_text(strip=True) for m in pb.find_all("div", class_="PKMNmovename")],
                    "ability": ability
                }

                trainer_data["pokemon_team"].append(pk)

            #if its the highest level we assume its the "ace"
            if trainer_data["pokemon_team"]:
                max_lv = max(p['level'] for p in trainer_data["pokemon_team"])
                for p in trainer_data["pokemon_team"]:
                    if p['level'] == max_lv: p['is_ace'] = True

            all_battles.append(trainer_data)
        self.logger.debug("<< extract_rival_battles")
        return all_battles

    def  _get_trainer_name(self, container):
        """ Gets the name of the trainer from the page, and whether its a major boss or not
        :param container: BeautifulSoup container object to extract from
        :return: the name of the trainer
        :return: whether its a major boss"""
        self.logger.debug(f">> _get_trainer_name")
        # Tries to use the headings to see if its a boss
        is_major_boss = False
        prev_h = container.find_previous(["h2", "h3", "h4"])
        # If rival is in the previous heading, it's a boss.'
        if prev_h and "rival" in prev_h.get_text().lower():
            is_major_boss = True

        # Gets the name of the trainer
        name_div = container.find("div", class_="partyname")
        trainer_name = name_div.get_text(strip=True) if name_div else "Unknown"
        self.logger.debug(f"The name of the trainer is {trainer_name}")
        self.logger.debug(f"<< _get_trainer_name")
        return trainer_name, is_major_boss

    def _get_team_condition(self, container):
        """This tries to determine whether there is a condition to this team
        like if the player must've picked "charmander"
        :param container: BeautifulSoup container object to extract from
        :return: the condition if there is one, otherwise None"""
        self.logger.debug(f">> _get_team_condition")
        condition = None

        # This tries to determine whether there is a condition to this team
        # like if the player must've picked "charmander"
        caption_div = container.find("div", class_="partycaption")
        if caption_div:
            match = re.search(r"chose\s+(\w+)", caption_div.get_text(separator=" ", strip=True))
            if match: condition = match.group(1)
        self.logger.debug(f"<< _get_team_condition")
        return condition

    def _get_pokemon_name_and_level(self, pb):
        """Gets the name of the pokemon and the level of the pokemon.
        :param pb: BeautifulSoup object to extract from
        :return: the name of the pokemon
        :return: the level of the Pokemon"""
        self.logger.debug(f">> _get_pokemon_name_and_level")

        raw_name = pb.find("div", class_="PKMNnamebox").get_text(strip=True)

        clean_name = re.sub(r'Lv\..*', '', raw_name).strip()
        logging.debug(f"Tidied name is: {clean_name}")
        lvl_tag = pb.find("span", class_="PKMNlevel")
        if lvl_tag:
            lvl_text = lvl_tag.get_text(strip=True)  # Result: "Lv.5"
            # Find only the numbers
            match = re.search(r'\d+', lvl_text)
            if match:
                level = int(match.group())
                logging.debug(f"Level is {level}")
        self.logger.debug(f"<< _get_pokemon_name_and_level")
        return clean_name, level

    def _get_ability_text(self, pb):
        """Gets the ability of the pokemon.
        :param pb: BeautifulSoup object to extract from
        :return: the ability of the pokemon"""
        self.logger.debug(f">> _get_ability_text")

        ability_div = pb.find("div", class_="PKMNability")
        # gets the text of the ability
        ability = ability_div.get_text(strip=True) if ability_div else "None"

        # older gens dont have abilities so they are none
        if ability == "No Ability" or not ability:
            ability = None
        self.logger.debug(f"<< _get_ability_text")
        return ability