-- -- THIS TABLE ACTUALLY CONTAINS POKÉMON
CREATE TABLE IF NOT EXISTS pokemon (
    id SERIAL PRIMARY KEY,
    national_dex_number INTEGER NOT NULL,
    name VARCHAR(50) NOT NULL,
    slug VARCHAR(50),
    form_name VARCHAR(50) DEFAULT NULL,
    is_official_form BOOLEAN DEFAULT TRUE,
    evolves_from_id INTEGER REFERENCES pokemon(id),

    CONSTRAINT unique_dex_and_form UNIQUE (national_dex_number, form_name)
);

