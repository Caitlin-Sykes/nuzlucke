-- THIS TABLE ACTUALLY CONTAINS POKÉMON
CREATE TABLE pokemon (
                        id SERIAL PRIMARY KEY,
                        national_dex_number INTEGER NOT NULL,
                        name VARCHAR(50) NOT NULL,
                        slug VARCHAR(50),
                        form_name VARCHAR(50) NOT NULL DEFAULT 'Base',
                        is_official_form BOOLEAN DEFAULT TRUE,
                        evolves_from_id INTEGER REFERENCES pokemon(id)
);

-- Nat Dex is unique, and there is only one type of each form
ALTER TABLE pokemon
    ADD CONSTRAINT unique_dex_and_form
        UNIQUE (national_dex_number, form_name);
