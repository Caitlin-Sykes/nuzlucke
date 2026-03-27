import logging


def extract_starters_dynamically(page):
    """Extracts starters from a given page
    by looking for a three-column three-row
    table
    :param page to be scraped"""
    logging.info(">> extract_starters_dynamically")
    starters = []

    for table in page.find_all("table", class_="roundy"):
        cells = table.find_all("td")
        cell_contents = [cell.get_text().strip() for cell in cells]

        # We only care about tables that contain the word 'Gift'
        if "Gift" in cell_contents:
            logging.debug(f"Found a Gift/Starter table. Filtering...")

            # Loop through the list and look for the 'Gift' marker
            for i, content in enumerate(cell_contents):
                if content == "Gift":
                    # Based on the log pattern, the name is 1 or 2 slots before 'Gift'
                    # e.g., ['Treecko', 'Treecko', 'Gift']
                    potential_name = cell_contents[i - 1]

                    # Clean the name (remove symbols like male/female)
                    clean_name = potential_name.replace('♂', '').replace('♀', '').strip()

                    # Validation:
                    # 1. Must be capitalized
                    # 2. Must not be 'Gift' or empty
                    # 3. Not already in our list
                    if clean_name and clean_name[0].isupper() and clean_name != "Gift":
                        if clean_name not in starters:
                            starters.append(clean_name)

        # Most games have 3 starters. If we found 3, we can stop.
        if len(starters) == 3:
            break

    logging.info(f"<< extract_starters_dynamically (Found: {starters})")
    return starters