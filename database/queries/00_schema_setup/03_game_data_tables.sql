-- THIS IS A TABLE FOR POKÉMON GAMES
CREATE TABLE games (
                       id SERIAL PRIMARY KEY,
                       name VARCHAR(100) NOT NULL,
                       ruleset_id INTEGER NOT NULL REFERENCES rulesets(id),
                       region_id INTEGER REFERENCES regions(id),
                       api_version_id INTEGER UNIQUE,
                       is_rom_hack BOOLEAN DEFAULT FALSE
);

-- Represents broad geographical areas (e.g., 'Route 1', 'Viridian Forest').
CREATE TABLE locations (
                           id SERIAL PRIMARY KEY,
                           region_id INTEGER REFERENCES regions(id),
                           name VARCHAR(100) NOT NULL,
                           api_id INTEGER UNIQUE,
                           CONSTRAINT unique_loc_per_region UNIQUE (region_id, name)
);

-- Represents specific sub-sections within a Location (e.g., 'Route 1 - Grass').
CREATE TABLE location_areas (
                                id SERIAL PRIMARY KEY,
                                location_id INTEGER NOT NULL REFERENCES locations(id),
                                name VARCHAR(100) NOT NULL,
                                api_id INTEGER UNIQUE
);
