from .BaseRepository import BaseRepository
import hashlib
import json


def _hash_config(payload: dict | None) -> str | None:
    """Hashes a configuration dictionary for use as a run_config_hash column value."""
    if not payload:
        return None
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


class SyncStateRepository(BaseRepository):
    """Repository for tracking synchronisation state."""
    
    def mark_start(self, component: str, generation: int = 0, run_config: dict | None = None):
        """Marks the start of a synchronisation process for a given component and generation.
        
        :param component: The component identifier for the synchronisation.
        :param generation: The generation number (defaults to 0 for tasks like games generation).
        :param run_config: Optional configuration parameters for the synchronisation run.
        """
        h = _hash_config(run_config)
        self.db.cursor.execute(
            """
            INSERT INTO sync_state (component, generation, status, started_at, run_config_hash)
            VALUES (%s, %s, 'in_progress', now(), %s)
            ON CONFLICT (component, generation)
                DO UPDATE SET status='in_progress', started_at=now(), finished_at=NULL, error_message=NULL, run_config_hash=EXCLUDED.run_config_hash;
            """,
            (component, generation, h)
        )
        self.db.conn.commit()

    def mark_success(self, component: str, generation: int = 0):
        """Marks the completion of a synchronisation process for a given component and generation.
        :param component: The component identifier for the synchronisation.
        :param generation: The generation number (defaults to 0 for non-generational tasks)."""
        self.db.cursor.execute(
            "UPDATE sync_state SET status='completed', finished_at=now(), error_message=NULL WHERE component=%s AND generation=%s",
            (component, generation)
        )
        self.db.conn.commit()


    def mark_failure(self, component: str, generation: int = 0, err: str = None, last_cursor: dict | None = None):
        """Marks the failure of a synchronisation process for a given component and generation.
        :param component: The component identifier for the synchronisation.
        :param generation: The generation number (defaults to 0 for non-generational tasks)."""
        self.db.cursor.execute(
            "UPDATE sync_state SET status='failed', finished_at=now(), error_message=%s, last_cursor=%s WHERE component=%s AND generation=%s",
            (err, json.dumps(last_cursor) if last_cursor else None, component, generation)
        )
        self.db.conn.commit()

    def is_completed(self, component: str, generation: int = 0) -> bool:
        """Checks if a synchronisation process for a given component and generation has completed.
        :param component: The component identifier for the synchronisation.
        :param generation: The generation number (defaults to 0 for non-generational tasks)."""
        self.db.cursor.execute(
            "SELECT 1 FROM sync_state WHERE component=%s AND generation=%s AND status='completed' LIMIT 1",
            (component, generation)
        )
        return self.db.cursor.fetchone() is not None