-- THIS IS A TABLE FOR POKÉMON GAMES
CREATE TABLE IF NOT EXISTS games (
                       id SERIAL PRIMARY KEY,
                       name VARCHAR(100) NOT NULL,
                       ruleset_id INTEGER NOT NULL REFERENCES rulesets(id),
                       region_id INTEGER REFERENCES regions(id),
                       is_rom_hack BOOLEAN DEFAULT FALSE,
                       is_dlc BOOLEAN DEFAULT FALSE,
                       illustration JSONB,
                       game_credits JSONB,
                       release_dates JSONB,
                       platform VARCHAR(50),
                       generations_included INTEGER[],
                       description VARCHAR(500),
                       has_alternate_forms BOOLEAN DEFAULT FALSE,
                       has_mega_evolution BOOLEAN DEFAULT FALSE,
                       CONSTRAINT unique_game_per_ruleset UNIQUE (ruleset_id, name)
);

-- Creates a new type for game engine types
CREATE TYPE game_engine AS ENUM ('Rom Hack', 'Essentials', 'Unity');

-- Contains specific data about a game
CREATE TABLE IF NOT EXISTS game_metadata (
                                             game_id INT PRIMARY KEY REFERENCES games(id) ON DELETE CASCADE,

                                             has_fakemon BOOLEAN DEFAULT false,

                                             stats_modified BOOLEAN DEFAULT true,
    
                                             is_complete BOOLEAN DEFAULT false,
                                           
                                             -- "ROM Hack of?" - link to games table
                                             -- E.G: Radical Red (ID 50) points to FireRed (ID 5)
                                             rom_hack_of_game_id INT REFERENCES games(id),

                                             engine_type game_engine,

                                            -- Nuzlocke Quality of Life 
                                            -- This stores your "Challenge Modes", "HM Items", etc.
                                             qol_features JSONB,

                                             -- Difficulty Level (string or enum)
                                             difficulty_level VARCHAR(50),
                                         
                                             unique_story BOOLEAN DEFAULT true
);

-- Represents broad geographical areas (e.g., 'Route 1', 'Viridian Forest').
CREATE TABLE IF NOT EXISTS locations (
                           id SERIAL PRIMARY KEY,
                           region_id INTEGER REFERENCES regions(id),
                           name VARCHAR(100) NOT NULL,
                           CONSTRAINT unique_loc_per_region UNIQUE (region_id, name)
);
-- 
-- -- Represents specific sub-sections within a Location (e.g., 'Route 1 - Grass').
CREATE TABLE IF NOT EXISTS location_areas (
                                id SERIAL PRIMARY KEY,
                                location_id INTEGER NOT NULL REFERENCES locations(id),
                                name VARCHAR(100) NOT NULL,
                                CONSTRAINT unique_area_per_location UNIQUE (name, location_id)
);
-- 
-- -- These are for specific stages within a game
-- -- like gyms, etc, used for level_caps
-- CREATE TABLE IF NOT EXISTS milestone_stages (
--                                   id SERIAL PRIMARY KEY,
--                                   game_slug  VARCHAR(50) NOT NULL,
--                                   stage_name VARCHAR(100) NOT NULL, -- 'Pewter Gym', 'Route 3'
--                                   level_cap INTEGER NOT NULL,       -- 14
--                                   order_index INTEGER NOT NULL     -- For sorting chronologically
--                              
-- );
-- -- 3. Trainers (Specific encounters within a stage)
-- -- CREATE TABLE milestone_trainers (
-- --                                     id SERIAL PRIMARY KEY,
-- --                                     stage_id INTEGER REFERENCES milestone_stages(id),
-- --                                     trainer_name VARCHAR(100) NOT NULL, -- 'Brock', 'Camper Liam'
-- --                                     is_major_boss BOOLEAN DEFAULT FALSE,
-- --                                     internal_label VARCHAR(100),       -- 'BrockData', 'Camper1Data'
-- --                                     condition VARCHAR(100)             -- 'bulbasaur' (if encounter changes based on starter)
-- -- );
-- 
-- -- These are the milestones that a game has.
-- -- like gyms, etc, used for level_caps
CREATE TABLE IF NOT EXISTS milestones (
                            id SERIAL PRIMARY KEY,
                            game_id INT REFERENCES games(id),
                            stage_name VARCHAR(100) NOT NULL,
                            level_cap INT NOT NULL,
                            order_index INT NOT NULL,
                            game_slug VARCHAR(50),
                            unlocks_surf BOOLEAN DEFAULT FALSE,
                            has_fishing_rod BOOLEAN DEFAULT FALSE,
                            CONSTRAINT uq_game_order_index UNIQUE (game_id, order_index)
);

-- -- Trainers you can fight in a stage
CREATE TABLE IF NOT EXISTS milestone_trainers (
                                    id SERIAL PRIMARY KEY,
                                    stage_id INTEGER REFERENCES milestones(id),
                                    trainer_name VARCHAR(100) NOT NULL, -- 'Brock', 'Camper Liam'
                                    is_major_boss BOOLEAN DEFAULT FALSE,
                                    condition VARCHAR(100)             -- 'bulbasaur' (if encounter changes based on starter)

);
-- -- Teams (The actual Pokemon in the party)
CREATE TABLE IF NOT EXISTS milestone_teams (
                                 id SERIAL PRIMARY KEY,
                                 trainer_id INTEGER REFERENCES milestone_trainers(id),
                                 pokemon_slug VARCHAR(50) NOT NULL,  -- 'geodude', 'onix'
                                 slot_number INTEGER NOT NULL,      -- 1, 2, 3
                                 level INTEGER NOT NULL,
                                 is_ace BOOLEAN DEFAULT FALSE,
                                 moves TEXT[],                      -- ARRAY['tackle', 'screech']
                                 ability VARCHAR(50)                -- For later gens
);

CREATE TABLE IF NOT EXISTS pokemon_learnsets (
    id SERIAL PRIMARY KEY,
    game_slug VARCHAR(50) NOT NULL, -- Matches PokéAPI version-group
    pokemon_slug VARCHAR(50) NOT NULL,
    move_name VARCHAR(50),
    level_learned INT,
    UNIQUE (pokemon_slug, game_slug, move_name, level_learned)
);

CREATE INDEX IF NOT EXISTS idx_pokemon_move_lookup
ON pokemon_learnsets (pokemon_slug, game_slug);
    -- -- -- Used to store encounters for milestones.
-- -- -- -- ie, what routes you can get to before a badge
-- CREATE TABLE milestone_encounters (
--                                       id SERIAL PRIMARY KEY,
--                                       milestone_id INTEGER NOT NULL REFERENCES milestones(id) ON DELETE CASCADE,
--                                       location_area_id INTEGER NOT NULL REFERENCES location_areas(id),
--
--     -- This flag is for the 10% the algorithm gets wrong.
--     -- If TRUE, the algorithm won't overwrite it.
--                                       is_manual_override BOOLEAN DEFAULT FALSE,
--
--                                       CONSTRAINT unique_encounter_per_game UNIQUE (milestone_id, location_area_id)
-- );


-- -- methods of encountering pokemon
CREATE TABLE IF NOT EXISTS encounter_methods (
                                   id SERIAL PRIMARY KEY,
                                   name VARCHAR(50) UNIQUE,
                                   is_primary BOOLEAN DEFAULT FALSE
);


-- 

-- 

-- 


