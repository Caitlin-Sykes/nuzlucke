-- THIS IS A TABLE FOR POKÉMON GAMES
CREATE TABLE games (
                       id SERIAL PRIMARY KEY,
                       name VARCHAR(100) NOT NULL,
                       ruleset_id INTEGER NOT NULL REFERENCES rulesets(id),
                       region_id INTEGER REFERENCES regions(id),
                       api_version_id INTEGER UNIQUE,
                       is_rom_hack BOOLEAN DEFAULT FALSE,
                       is_dlc BOOLEAN DEFAULT FALSE,
                       -- Assets & Metadata
                       image_url TEXT,                    
                       image_rights VARCHAR(255),         
                       image_credits VARCHAR(255),        
                       release_date_us DATE,
                       release_date_jp DATE,
                       release_date_eu DATE,
                       release_date_au DATE,
                       platform VARCHAR(50),
                       creator VARCHAR(50),
                       generations_included INTEGER[]
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

-- These are the milestones that a game has.
-- like gyms, etc, used for level_caps
CREATE TABLE milestones (
                            id SERIAL PRIMARY KEY,
                            game_id INT REFERENCES games(id),
                            stage_name VARCHAR(100) NOT NULL,
                            trainer_name VARCHAR(100),
                            level_cap INT NOT NULL,
                            order_index INT NOT NULL,
                            is_major_boss BOOLEAN DEFAULT TRUE,
                            game_slug VARCHAR(50),
                            unlocks_surf VARCHAR(50) DEFAULT NULL,
                            UNIQUE(game_id, order_index)
);

-- this table is only relevant for milestones that have pokemon teams
-- like gym leaders, etc
CREATE TABLE milestone_teams (
                                 id SERIAL PRIMARY KEY,
                                 milestone_id INT REFERENCES milestones(id) ON DELETE CASCADE,
                                 pokemon_id INT REFERENCES pokemon(id),
                                 slot_number INT,
                                 level INT NOT NULL,
                                 is_ace BOOLEAN DEFAULT FALSE,
                                 moves TEXT[], -- This stores ['tackle', 'bind', 'bide']
                                 ability varchar(50) DEFAULT NULL,
                                 condition TEXT DEFAULT NULL -- This is used for varying teams, like rival having fire type if you picked grass, etc. This stores the PLAYER choice
);

-- Used to store encounters for milestones.
-- ie, what routes you can get to before a badge
CREATE TABLE milestone_encounters (
                                      id SERIAL PRIMARY KEY,
                                      milestone_id INTEGER NOT NULL REFERENCES milestones(id) ON DELETE CASCADE,
                                      location_area_id INTEGER NOT NULL REFERENCES location_areas(id),

    -- This flag is for the 10% the algorithm gets wrong.
    -- If TRUE, the algorithm won't overwrite it.
                                      is_manual_override BOOLEAN DEFAULT FALSE,

                                      CONSTRAINT unique_encounter_per_game UNIQUE (milestone_id, location_area_id)
);

-- methods of encountering pokemon
CREATE TABLE encounter_methods (
                                   id SERIAL PRIMARY KEY,
                                   name VARCHAR(50) UNIQUE,
                                   is_primary BOOLEAN DEFAULT FALSE
);