-- -- Tracks the current state of the table, so that we can restore from where it crashed/leftoff
-- -- later. Also if the user wants to update their generations

-- Creates a new type for game engine types
CREATE TYPE sync_status AS ENUM ('completed', 'failed', 'in_progress');

CREATE TABLE IF NOT EXISTS sync_state (
                                          component       text        NOT NULL,           -- e.g. 'games' | 'pokemon_info' | 'encounters'
                                          generation      int         NOT NULL,           -- e.g. 1..9
                                          status          sync_status        NOT NULL,           -- 'completed' | 'failed'
                                          started_at      timestamptz NOT NULL DEFAULT now(),
                                          finished_at     timestamptz NULL,
                                          last_cursor     jsonb       NULL,
                                          run_config_hash text        NULL,
                                          error_message   text        NULL,

                                          CONSTRAINT sync_state_pk PRIMARY KEY (component, generation)
);