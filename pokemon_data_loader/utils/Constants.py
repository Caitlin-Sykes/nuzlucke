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
group_to_ruleset = {
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
    21: 8,  # Gen 8 (the-isle-of-armor)
    22: 8,  # Gen 8 (the-crown-tundra)
    23: 8,  # Gen 8 (BDSP/Arceus)
    24: 8,
    25: 9,  # Gen 9 (Scarlet/Violet)
    26: 9,  # Gen 9 (Teal-Mask)
    27: 9,  # Gen 9 (Indigo-Disk)
    30: 9,  # Legends (LegendsZA)
    31: 9  # Mega Dimension
}