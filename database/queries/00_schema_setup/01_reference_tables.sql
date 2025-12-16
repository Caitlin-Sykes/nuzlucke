-- THIS TABLE IS FOR POKÉMON TYPES
CREATE TABLE types (
                       id SERIAL PRIMARY KEY,
                       name VARCHAR(50) UNIQUE NOT NULL,
                       is_official BOOLEAN DEFAULT TRUE
);

-- THIS TABLE IS FOR POKÉMON ABILITIES
CREATE TABLE abilities (
                           id SERIAL PRIMARY KEY,
                           name VARCHAR(50) UNIQUE NOT NULL,
                           description TEXT
);

-- THIS TABLE IS FOR POKÉMON REGIONS
CREATE TABLE regions (
                         id SERIAL PRIMARY KEY,
                         name VARCHAR(50) UNIQUE NOT NULL
);

-- THIS TABLE IS FOR POKÉMON RULESETS
CREATE TABLE rulesets (
                          id SERIAL PRIMARY KEY,
                          name VARCHAR(100) UNIQUE NOT NULL,       -- e.g., 'Gen 1', 'Storm Silver',
                          description TEXT,
                          is_official BOOLEAN DEFAULT TRUE        -- Whether it is a official ruleset
);
