-- VARIABLE STATS (Handles "In this hack, Charizard is Dragon Type")
CREATE TABLE pokemon_game_stats (
                                    id SERIAL PRIMARY KEY,
                                    pokemon_id INTEGER NOT NULL REFERENCES pokemon(id),
                                    ruleset_id INTEGER NOT NULL REFERENCES rulesets(id),
                                    type_1_id INTEGER REFERENCES types(id),
                                    type_2_id INTEGER REFERENCES types(id),
                                    ability_1_id INTEGER REFERENCES abilities(id),
                                    ability_2_id INTEGER REFERENCES abilities(id),
                                    hidden_ability_id INTEGER REFERENCES abilities(id),

    -- Composite UNIQUE constraint for the base stats table:
    -- A Pokémon can only have one set of stats per ruleset.
                                    UNIQUE (pokemon_id, ruleset_id)
);

-- GAME PROGRESSION
-- This controls the frontend "Order of Events" screen.
CREATE TABLE game_progression (
                                  id SERIAL PRIMARY KEY,
                                  game_id INTEGER NOT NULL REFERENCES games(id),
                                  location_id INTEGER NOT NULL REFERENCES locations(id),
                                  visit_order INTEGER NOT NULL,
                                  display_label VARCHAR(100),
                                  level_cap INTEGER,
                                  UNIQUE (game_id, visit_order)
);

-- ENCOUNTERS
CREATE TABLE encounters (
                            id SERIAL PRIMARY KEY,
                            game_id INTEGER NOT NULL REFERENCES games(id),
                            location_id INTEGER NOT NULL REFERENCES locations(id),
                            location_area_id INTEGER REFERENCES location_areas(id), 
                            pokemon_id INTEGER NOT NULL REFERENCES pokemon(id),
                            method VARCHAR(50),
                            rate_percentage INTEGER,
                            min_level INTEGER,
                            max_level INTEGER,

                            UNIQUE (game_id, location_id, location_area_id, pokemon_id, method)
);