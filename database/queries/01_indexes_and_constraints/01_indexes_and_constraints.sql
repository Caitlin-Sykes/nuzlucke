CREATE INDEX idx_encounters_game_loc ON encounters(game_id, location_id);
CREATE INDEX idx_pokemon_evolves_from ON pokemon(evolves_from_id);
ALTER TABLE milestone_encounters
    ADD CONSTRAINT unique_milestone_location_area UNIQUE (milestone_id, location_area_id);