# These are used to determine the conditions for the rivals unique teams
RIVAL_STARTER_CONDITIONS = {
    # Rival has Charizard/Charmeleon/Charmander -> Player must have picked Bulbasaur
    'CHARMANDER': "bulbasaur",
    'CHARMELEON': "bulbasaur",
    'CHARIZARD':   "bulbasaur",

    # Rival has Blastoise/Wartortle/Squirtle -> Player must have picked Charmander
    'SQUIRTLE':   "charmander",
    'WARTORTLE':  "charmander",
    'BLASTOISE':  "charmander",

    # Rival has Venusaur/Ivysaur/Bulbasaur -> Player must have picked Squirtle
    'BULBASAUR':  "squirtle",
    'IVYSAUR':    "squirtle",
    'VENUSAUR':   "squirtle",

    # Rival has CYNDAQUIL/QUILAVA/TYPHLOSION -> Player must have picked chikorita
    'CYNDAQUIL': "chikorita",
    'QUILAVA': "chikorita",
    'TYPHLOSION':   "chikorita",

    # Rival has TOTODILE/CROCONAW/FERALIGATR -> Player must have picked cyndaquil
    'TOTODILE':   "cyndaquil",
    'CROCONAW':  "cyndaquil",
    'FERALIGATR':  "cyndaquil",

    # Rival has CHIKORITA/BAYLEAF/MEGANIUM -> Player must have picked totodile
    'CHIKORITA':  "totodile",
    'BAYLEAF':    "totodile",
    'MEGANIUM':   "totodile",

    # Rival has TORCHIC/COMBUSKEN/BLAZIKEN -> Player must have picked treecko
    'TORCHIC': "treecko",
    'COMBUSKEN': "treecko",
    'BLAZIKEN':   "treecko",

    # Rival has MUDKIP/MARSHTOMP/SWAMPERT -> Player must have picked torchic
    'MUDKIP':   "torchic",
    'MARSHTOMP':  "torchic",
    'SWAMPERT':  "torchic",

    # Rival has TREECKO/GROVYLE/SCEPTILE -> Player must have picked mudkip
    'TREECKO':  "mudkip",
    'GROVYLE':    "mudkip",
    'SCEPTILE':   "mudkip",

    # Rival has CHIMCHAR/MONFERNO/INFERNAPE -> Player must have picked turtwig
    'CHIMCHAR': "turtwig",
    'MONFERNO': "turtwig",
    'INFERNAPE':   "turtwig",

    # Rival has PIPLUP/PRINPLUP/EMPOLEON -> Player must have picked chimchar
    'PIPLUP':   "chimchar",
    'PRINPLUP':  "chimchar",
    'EMPOLEON':  "chimchar",

    # Rival has TURTWIG/GROTLE/TORTERRA -> Player must have picked piplup
    'TURTWIG':  "piplup",
    'GROTLE':    "piplup",
    'TORTERRA':   "piplup"
}
