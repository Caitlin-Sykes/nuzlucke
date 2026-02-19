-- Tracks the current state of the table, so that we can restore from where it crashed/leftoff
-- later. Also if the user wants to update their generations

CREATE TABLE IF NOT EXISTS sync_state (
                                          component       text        NOT NULL,           -- e.g. 'games' | 'pokemon_info' | 'encounters'
                                          generation      int         NOT NULL,           -- e.g. 1..9
                                          status          text        NOT NULL,           -- 'pending' | 'in_progress' | 'completed' | 'failed'
                                          started_at      timestamptz NOT NULL DEFAULT now(),
                                          finished_at     timestamptz NULL,
                                          last_cursor     jsonb       NULL,               -- optional: resume point (e.g., last_processed_pokemon_id)
                                          run_config_hash text        NULL,               -- optional: hash of input params (version ids, valid methods)
                                          error_message   text        NULL,

                                          CONSTRAINT sync_state_pk PRIMARY KEY (component, generation)
);