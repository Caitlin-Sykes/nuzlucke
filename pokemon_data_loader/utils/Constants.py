# Mapping the games and their ids to their generation
GEN_VERSION_MAP = {
    1: [1, 2, 3],  # Red, Blue, Yellow
    2: [4, 5, 6],  # Gold, Silver, Crystal
    3: [7, 8, 9, 10, 11, 19, 20],  # Ruby, Sapphire, Emerald, FireRed, LeafGreen + Colosseum/XD
    4: [12, 13, 14, 15, 16],  # Diamond, Pearl, Platinum, HeartGold, SoulSilver
    5: [17, 18, 21, 22],  # Black, White, Black 2, White 2
    6: [23, 24, 25, 26],  # X, Y, Omega Ruby, Alpha Sapphire
    7: [27, 28, 29, 30, 31, 32],  # Sun, Moon, Ultra Sun, Ultra Moon, Let's Go P/E
    8: [33, 34, 35, 36, 37, 38, 39],  # Sword, Shield + DLCs (Armor/Tundra), BD/SP, Arceus
    9: [40, 41, 42, 43, 47, 48]  # Scarlet, Violet + DLCs (Teal/Indigo), ZA, Mega Dimension
}
# Mapping PokeAPI's version_group_id to rulesets
# Numbers on the left are the games, so 1: Red
# Number on the right is the ruleset. You can look at it as the generation of the game.
GROUP_TO_RULESET = {
    1: 1,  # Gen 1 (Red/Blue/Yellow)
    2: 1,
    3: 2,  # Gen 2 (Gold/Silver/Crystal)
    4: 2,
    5: 3,  # Gen 3 (Ruby/Sapphire/Emerald/FRLG)
    6: 3,
    7: 3,
    8: 4,  # Gen 4 (DPP/HGSS)
    9: 4,
    10: 4,
    11: 5,  # Gen 5 (Black/White)
    12: 3,  # Colosseum
    13: 3,  # XD
    14: 5,  # Gen 5 (B2W2)
    15: 6,  # Gen 6 (XY/ORAS)
    16: 6,
    17: 7,  # Gen 7 (Sun/Moon/USUM/LetsGo) 
    18: 7,
    19: 7,
    20: 8,  # Gen 8 (Sword/Shield)
    21: 8,  # Gen 8 (the-isle-of-armour)
    22: 8,  # Gen 8 (the-crown-tundra)
    23: 8,  # Gen 8 (BDSP/Arceus)
    24: 8,
    25: 9,  # Gen 9 (Scarlet/Violet)
    26: 9,  # Gen 9 (Teal-Mask)
    27: 9,  # Gen 9 (Indigo-Disk)
    30: 9,  # Legends (LegendsZA)
    31: 9  # Mega Dimension
}

# For each game, map what gym you get surf
# so we can add these to the encounters
# available to the player
# this is also used to map the surfing
#ABILITY not just the move
SURF_MILESTONE = {
    "Fuchsia City - Gym 5": ["red", "blue", "yellow", "firered", "leafgreen", "lets-go-pikachu", "lets-go-eevee"],
    "Ecruteak City - Gym 4": ["gold", "silver", "crystal", "heartgold", "soulsilver"],
    "Petalburg City - Gym 5": ["ruby", "sapphire", "emerald", "omega-ruby", "alpha-sapphire"],
    "Hearthome City - Gym 5": ["diamond", "pearl", "platinum", "brilliant-diamond", "shining-pearl"],
    "Mistralton City - Gym 6": ["black", "white"],
    "Driftveil City - Gym 5": ["black-2", "white-2"],
    "Shalour City - Gym 3": ["x", "y"],
    "Brooklet Hill - Lana Trial": ["sun", "moon", "ultra-sun", "ultra-moon"],
    "Circhester Stadium - Gym 6": ["sword", "shield"],
    "West Province (Area One) - Open Sky Titan": ["scarlet", "violet"]
}

# This is metadata for the games
# that could not be retrieved from an api
# so it is hardcoded here
GB = "Game Boy"
GBC = "Game Boy Color"
GBA = "Game Boy Advance"
NDS = "Nintendo DS"
N3DS = "Nintendo 3DS"
SWITCH = "Nintendo Switch"
GAMECUBE = "Nintendo Gamecube"

GAME_METADATA = [
    # GEN 1
    {"slug": "red", "jp": "1996-02-27", "us": "1998-09-28", "eu": "1999-10-05", "au": "1998-10-23", "platform": GB, "gens": (1,),"is_dlc":False},
    {"slug": "blue", "jp": "1996-10-15", "us": "1998-09-28", "eu": "1999-10-05", "au": "1998-10-23", "platform": GB, "gens": (1,),"is_dlc":False},
    {"slug": "yellow", "jp": "1998-09-12", "us": "1999-10-18", "eu": "2000-06-16", "au": "1999-09-03", "platform": GB, "gens": (1,),"is_dlc":False},

    # GEN 2
    {"slug": "gold", "jp": "1999-11-21", "us": "2000-10-15", "eu": "2001-04-06", "au": "2000-10-13", "platform": GBC, "gens": (1, 2),"is_dlc":False},
    {"slug": "silver", "jp": "1999-11-21", "us": "2000-10-15", "eu": "2001-04-06", "au": "2000-10-13", "platform": GBC, "gens": (1, 2),"is_dlc":False},
    {"slug": "crystal", "jp": "2000-12-14", "us": "2001-07-29", "eu": "2001-11-02", "au": "2001-09-30", "platform": GBC, "gens": (1, 2),"is_dlc":False},

    # GEN 3
    {"slug": "ruby", "jp": "2002-11-21", "us": "2003-03-19", "eu": "2003-07-25", "au": "2003-04-03", "platform": GBA, "gens": (1, 2, 3),"is_dlc":False},
    {"slug": "sapphire", "jp": "2002-11-21", "us": "2003-03-19", "eu": "2003-07-25", "au": "2003-04-03", "platform": GBA, "gens": (1, 2, 3),"is_dlc":False},
    {"slug": "emerald", "jp": "2004-09-16", "us": "2005-05-01", "eu": "2005-10-21", "au": "2005-06-09", "platform": GBA, "gens": (1, 2, 3),"is_dlc":False},
    {"slug": "firered", "jp": "2004-01-29", "us": "2004-09-07", "eu": "2004-10-01", "au": "2004-09-23", "platform": GBA, "gens": (1, 2, 3),"is_dlc":False},
    {"slug": "leafgreen", "jp": "2004-01-29", "us": "2004-09-07", "eu": "2004-10-01", "au": "2004-09-23", "platform": GBA, "gens": (1, 2, 3),"is_dlc":False},
    {"slug": "colosseum", "jp": "2003-11-21", "us": "2004-03-22", "eu": "2004-05-14", "au": "2004-06-24", "platform": GAMECUBE, "gens": (3,),"is_dlc":False},
    {"slug": "xd", "jp": "2005-08-04", "us": "2005-10-03", "eu": "2005-11-10", "au": "2005-11-18", "platform": GAMECUBE, "gens": (3,),"is_dlc":False},

    # GEN 4
    {"slug": "diamond", "jp": "2006-09-28", "us": "2007-04-22", "eu": "2007-07-27", "au": "2007-06-21", "platform": NDS, "gens": (1, 2, 3, 4),"is_dlc":False},
    {"slug": "pearl", "jp": "2006-09-28", "us": "2007-04-22", "eu": "2007-07-27", "au": "2007-06-21", "platform": NDS, "gens": (1, 2, 3, 4),"is_dlc":False},
    {"slug": "platinum", "jp": "2008-09-13", "us": "2009-03-22", "eu": "2009-05-22", "au": "2009-05-14", "platform": NDS, "gens": (1, 2, 3, 4),"is_dlc":False},
    {"slug": "heartgold", "jp": "2009-09-12", "us": "2010-03-14", "eu": "2010-03-26", "au": "2010-03-25", "platform": NDS, "gens": (1, 2, 3, 4),"is_dlc":False},
    {"slug": "soulsilver", "jp": "2009-09-12", "us": "2010-03-14", "eu": "2010-03-26", "au": "2010-03-25", "platform": NDS, "gens": (1, 2, 3, 4),"is_dlc":False},

    # GEN 5
    {"slug": "black", "jp": "2010-09-18", "us": "2011-03-06", "eu": "2011-03-04", "au": "2011-03-10", "platform": NDS, "gens": (1, 2, 3, 4, 5),"is_dlc":False},
    {"slug": "white", "jp": "2010-09-18", "us": "2011-03-06", "eu": "2011-03-04", "au": "2011-03-10", "platform": NDS, "gens": (1, 2, 3, 4, 5),"is_dlc":False},
    {"slug": "black-2", "jp": "2012-06-23", "us": "2012-10-07", "eu": "2012-10-12", "au": "2012-10-11", "platform": NDS, "gens": (1, 2, 3, 4, 5),"is_dlc":False},
    {"slug": "white-2", "jp": "2012-06-23", "us": "2012-10-07", "eu": "2012-10-12", "au": "2012-10-11", "platform": NDS, "gens": (1, 2, 3, 4, 5),"is_dlc":False},

    # GEN 6
    {"slug": "x", "jp": "2013-10-12", "us": "2013-10-12", "eu": "2013-10-12", "au": "2013-10-12", "platform": N3DS, "gens": (1, 2, 3, 4, 5, 6),"is_dlc":False},
    {"slug": "y", "jp": "2013-10-12", "us": "2013-10-12", "eu": "2013-10-12", "au": "2013-10-12", "platform": N3DS, "gens": (1, 2, 3, 4, 5, 6),"is_dlc":False},
    {"slug": "omega-ruby", "jp": "2014-11-21", "us": "2014-11-21", "eu": "2014-11-28", "au": "2014-11-21", "platform": N3DS, "gens": (1, 2, 3, 4, 5, 6),"is_dlc":False},
    {"slug": "alpha-sapphire", "jp": "2014-11-21", "us": "2014-11-21", "eu": "2014-11-28", "au": "2014-11-21", "platform": N3DS, "gens": (1, 2, 3, 4, 5, 6),"is_dlc":False},

    # GEN 7
    {"slug": "sun", "jp": "2016-11-18", "us": "2016-11-18", "eu": "2016-11-23", "au": "2016-11-18", "platform": N3DS, "gens": (1, 2, 3, 4, 5, 6, 7),"is_dlc":False},
    {"slug": "moon", "jp": "2016-11-18", "us": "2016-11-18", "eu": "2016-11-23", "au": "2016-11-18", "platform": N3DS, "gens": (1, 2, 3, 4, 5, 6, 7),"is_dlc":False},
    {"slug": "ultra-sun", "jp": "2017-11-17", "us": "2017-11-17", "eu": "2017-11-17", "au": "2017-11-17", "platform": N3DS, "gens": (1, 2, 3, 4, 5, 6, 7),"is_dlc":False},
    {"slug": "ultra-moon", "jp": "2017-11-17", "us": "2017-11-17", "eu": "2017-11-17", "au": "2017-11-17", "platform": N3DS, "gens": (1, 2, 3, 4, 5, 6, 7),"is_dlc":False},
    {"slug": "lets-go-pikachu", "jp": "2018-11-16", "us": "2018-11-16", "eu": "2018-11-16", "au": "2018-11-16", "platform": SWITCH, "gens": (1, 7),"is_dlc":False},
    {"slug": "lets-go-eevee", "jp": "2018-11-16", "us": "2018-11-16", "eu": "2018-11-16", "au": "2018-11-16", "platform": SWITCH, "gens": (1, 7),"is_dlc":False},

    # GEN 8
    {"slug": "sword", "jp": "2019-11-15", "us": "2019-11-15", "eu": "2019-11-15", "au": "2019-11-15", "platform": SWITCH, "gens": (1, 2, 3, 4, 5, 6, 7, 8),"is_dlc":False},
    {"slug": "shield", "jp": "2019-11-15", "us": "2019-11-15", "eu": "2019-11-15", "au": "2019-11-15", "platform": SWITCH, "gens": (1, 2, 3, 4, 5, 6, 7, 8),"is_dlc":False},
    {"slug": "the-isle-of-armor", "jp": "2020-06-17", "us": "2020-06-17", "eu": "2020-06-17", "au": "2020-06-17", "platform": SWITCH, "gens": (1, 2, 3, 4, 5, 6, 7, 8),"is_dlc":True},
    {"slug": "the-crown-tundra", "jp": "2020-10-23", "us": "2020-10-23", "eu": "2020-10-23", "au": "2020-10-23", "platform": SWITCH, "gens": (1, 2, 3, 4, 5, 6, 7, 8),"is_dlc":True},
    {"slug": "brilliant-diamond", "jp": "2021-11-19", "us": "2021-11-19", "eu": "2021-11-19", "au": "2021-11-19", "platform": SWITCH, "gens": (1, 2, 3, 4),"is_dlc":False},
    {"slug": "shining-pearl", "jp": "2021-11-19", "us": "2021-11-19", "eu": "2021-11-19", "au": "2021-11-19", "platform": SWITCH, "gens": (1, 2, 3, 4),"is_dlc":False},
    {"slug": "legends-arceus", "jp": "2022-01-28", "us": "2022-01-28", "eu": "2022-01-28", "au": "2022-01-28", "platform": SWITCH, "gens": (1, 2, 4, 8),"is_dlc":False},

    # GEN 9
    {"slug": "scarlet", "jp": "2022-11-18", "us": "2022-11-18", "eu": "2022-11-18", "au": "2022-11-18", "platform": SWITCH, "gens": (1, 2, 3, 4, 5, 6, 7, 8, 9),"is_dlc":False},
    {"slug": "violet", "jp": "2022-11-18", "us": "2022-11-18", "eu": "2022-11-18", "au": "2022-11-18", "platform": SWITCH, "gens": (1, 2, 3, 4, 5, 6, 7, 8, 9),"is_dlc":False},
    {"slug": "the-teal-mask", "jp": "2023-09-13", "us": "2023-09-13", "eu": "2023-09-13", "au": "2023-09-13", "platform": SWITCH, "gens": (1, 2, 3, 4, 5, 6, 7, 8, 9),"is_dlc":True},
    {"slug": "the-indigo-disk", "jp": "2023-12-14", "us": "2023-12-14", "eu": "2023-12-14", "au": "2023-12-14", "platform": SWITCH, "gens": (1, 2, 3, 4, 5, 6, 7, 8, 9),"is_dlc":True},
    {"slug": "legends-za", "jp": "2025-10-16", "us": "2025-10-16", "eu": "2025-10-16", "au": "2025-10-16", "platform": SWITCH, "gens": (1, 2, 3, 4, 5, 6, 7, 8, 9),"is_dlc":False},
    {"slug": "mega-dimension", "jp": "2025-12-10", "us": "2025-12-10", "eu": "2025-12-10", "au": "2025-12-10", "platform": SWITCH, "gens": (1, 2, 3, 4, 5, 6, 7, 8, 9),"is_dlc":True}
]





