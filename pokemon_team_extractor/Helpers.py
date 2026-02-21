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
