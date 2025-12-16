CREATE INDEX idx_encounters_game_loc ON encounters(game_id, location_id);
CREATE INDEX idx_progression_game ON game_progression(game_id, visit_order);
CREATE INDEX idx_pokemon_evolves_from ON pokemon(evolves_from_id);