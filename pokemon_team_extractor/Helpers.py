import re


def get_level(tuple_str):
    """Extracts the 4th value in the tuple: Level)
    :param tuple_str: String representation of a tuple.
    """ 
    match = re.search(r"\([^,]+,[^,]+,[^,]+,\s*(\d+)", tuple_str)
    return int(match.group(1)) if match else 0


def get_slot(tuple_str):
    """Extracts the 3rd value in the tuple: Slot
    :param tuple_str: String representation of a tuple.
    """
    match = re.search(r"\([^,]+,[^,]+,\s*(\d+)", tuple_str)
    return int(match.group(1)) if match else 0


def get_label(tuple_str):
    """Extracts the 1st value in the tuple: Label)
    :param tuple_str: String representation of a tuple.
    """
    match = re.search(r"\('([^']+)_", tuple_str)
    return match.group(1) if match else ""

def filename_to_location(filename):
    """Formats a location name from its filename by adding spaces before capital letters and removing the file extension.
    :param filename: Location filename."""
    name = filename.replace('.asm', '')
    return re.sub(r'([a-z])([A-Z])', r'\1 \2', name)

def format_rival_name(raw_name):
    """Formats the rival name by stripping numbers off it
    also capitalises it
    :param raw_name: Name of the Rival without the number in front of it."""
    return re.sub(r'\d+', '', raw_name).capitalize()

def format_display_name(m_id, location, is_boss):
    """Formats 'rival1data_1' -> 'Oak's Lab: Rival Battle'"""
    # Clean the trainer name
    trainer = m_id.split('_')[0].replace('Data', '').replace('data', '').capitalize()

    if "Rival" in trainer:
        return "Rival Battle"

    if is_boss:
        # e.g., "Pewter Gym: Brock"
        return f"{location}: {trainer}"

    # For minor trainers: "Route 3: Youngster"
    return f"{trainer}"


def format_string(location, regex, format_template):
    """Formats a location name based on a passed in string and regex
    :param location: Location string.
    :param regex: Regex pattern to match against.
    :param format_template: Formatting template to apply to matched string. (Example: 'Elite Four: \1')"""
    return re.sub(regex, format_template, location)


def format_location_name(name):
    """Formats a location name by adding spaces between words and numbers.
    :param name: Name of the location
    :return formatted_name: Formatted location name"""
    # Add spaces between CamelCase words (ViridianForest -> Viridian Forest)
    name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)

    # Add spaces between Words and Numbers (Route10 -> Route 10)
    name = re.sub(r'([a-zA-Z])(\d+)', r'\1 \2', name)

    # Handle S.S. Anne and its floor transitions (1FRooms -> 1F Rooms)
    name = name.replace("SSAnne", "S.S. Anne")
    name = re.sub(r'(\dF)([A-Z])', r'\1 \2', name)

    # Fix Basement spacing (B 1F -> B1F)
    name = name.replace("B ", "B")

    return name.strip()