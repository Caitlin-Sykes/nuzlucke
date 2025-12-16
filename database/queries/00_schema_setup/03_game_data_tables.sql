-- THIS IS A TABLE FOR POKÉMON GAMES
CREATE TABLE games (
                       id SERIAL PRIMARY KEY,
                       name VARCHAR(100) NOT NULL,
                       ruleset_id INTEGER NOT NULL REFERENCES rulesets(id),
                       region_id INTEGER REFERENCES regions(id),
                       api_version_id INTEGER,
                       is_rom_hack BOOLEAN DEFAULT FALSE
);

-- THIS CREATES A RECORD FOR EACH LOCATION IN A GAME
CREATE TABLE locations (
                           id SERIAL PRIMARY KEY,
                           region_id INTEGER REFERENCES regions(id),
                           name VARCHAR(100) NOT NULL,
                           CONSTRAINT unique_loc_per_region UNIQUE (region_id, name)
);
