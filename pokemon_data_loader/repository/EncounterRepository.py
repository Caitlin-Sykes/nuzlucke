from .BaseRepository import BaseRepository
from pokemon_data_loader.utils.Constants import SURF_MILESTONE


class EncounterRepository(BaseRepository):
    """ This class handles the encounters and order of 
    progression in the db. It also adds encounter methods
    """

    def insert_encounter_methods(self):
        """
        Inserts encounter methods based off the data in the encounters table
    
        """
        self.logger.debug(">> insert_encounter_methods")

        sql = """
              INSERT INTO encounter_methods (name, is_primary)
              SELECT DISTINCT
                  method,
                  CASE
                      WHEN method IN ('walk', 'seaweed', 'dark-grass', 'tall-grass') THEN TRUE
                      ELSE FALSE
                      END
              FROM encounters
              ON CONFLICT (name) DO UPDATE SET is_primary = EXCLUDED.is_primary; \
              """

        try:
            self.db.cursor.execute(sql)
            self.db.conn.commit()
            self.logger.debug("<< insert_encounter_methods")
        except Exception as e:
            self.logger.error(f"Failed to insert encounter methods: {e}")
            self.db.conn.rollback()
            raise

    def map_encounters_to_milestones(self, game_id: int):
        """
        Automates the encounter chain by matching the max wild level 
        of an area to the appropriate milestone level cap.
        :param game_id: The ID of the game to map encounters for
        """
        self.logger.debug(f">> map_encounters_to_milestones for game {game_id}")
    
        sql = """
              INSERT INTO milestone_encounters (milestone_id, location_area_id)
              WITH AreaMaxLevels AS (
                  -- for each area get the highest level
                  SELECT
                      e.location_area_id,
                      MAX(e.max_level) as area_max_lvl
                  FROM encounters e
                           JOIN encounter_methods em ON e.method = em.name
                  WHERE e.game_id = %s
                    AND em.is_primary = TRUE
                  GROUP BY e.location_area_id
              )
              SELECT DISTINCT ON (aml.location_area_id)
                  m.id as milestone_id,
                  aml.location_area_id
              FROM AreaMaxLevels aml
                       JOIN milestones m ON m.game_id = %s
              -- compare with our milestone levels to see where it falls
              WHERE aml.area_max_lvl <= m.level_cap
              -- pick the first one so they don't overmatch
              ORDER BY aml.location_area_id, m.order_index
              ON CONFLICT DO NOTHING; \
              """
    
        try:
            self.db.cursor.execute(sql, (game_id, game_id))
            self.db.conn.commit()
            self.logger.debug("<< map_encounters_to_milestones")
        except Exception as e:
            self.logger.error(f"Mapping failed: {e}")
            self.db.conn.rollback()
            raise

    def kanto_overrides(self):
        """
        Adds manual encounter overrides for areas
        that are incorrectly allocated by the level-finding
        algorithm.
        For example, kanto-route-3 is accessed after Misty's badge,
        despite having the level cap for Brock.
        """
        self.logger.debug(">> kanto_overrides")
    
        sql = """
              INSERT INTO milestone_encounters (milestone_id, location_area_id, is_manual_override)
              SELECT m.id, la.id, TRUE
              FROM (VALUES
                        -- Blocked by Pewter Guard (Move from Gym 1 guess to Gym 2)
                        ('kanto-route-3-area', 'Cerulean City - Gym 2'),
                        ('mt-moon-1f', 'Cerulean City - Gym 2'),
                        ('mt-moon-b1f', 'Cerulean City - Gym 2'),
                        ('mt-moon-b2f', 'Cerulean City - Gym 2'),
                        ('kanto-route-4-area', 'Cerulean City - Gym 2'),
    
                        -- Accessible only after Mt. Moon / Misty
                        ('kanto-route-24-area', 'Cerulean City - Gym 2'),
                        ('kanto-route-25-area', 'Cerulean City - Gym 2'),
                        ('kanto-route-5-area', 'Cerulean City - Gym 2'),
    
                        -- Blocked by HM Cut (Requires Gym 2 Badge to use outside)
                        ('kanto-route-9-area', 'Vermillion City - Gym 3'),
                        ('kanto-route-10-area', 'Vermillion City - Gym 3'),
                        ('rock-tunnel-1f', 'Vermillion City - Gym 3'),
                        ('rock-tunnel-b1f', 'Vermillion City - Gym 3'),
    
                        -- Blocked by Snorlax (Requires Poke Flute after Gym 4)
                        ('kanto-route-12-area', 'Fuchsia City - Gym 5'),
                        ('kanto-route-16-area', 'Fuchsia City - Gym 5'),
                        ('kanto-route-13-area', 'Fuchsia City - Gym 5'),
                        ('kanto-route-14-area', 'Fuchsia City - Gym 5'),
                        ('kanto-route-15-area', 'Fuchsia City - Gym 5')
                   ) AS t(area_name, milestone_name)
                       JOIN location_areas la ON la.name = t.area_name
                       JOIN milestones m ON m.stage_name = t.milestone_name
              WHERE m.game_id = 1
              ON CONFLICT (milestone_id, location_area_id)
                  DO UPDATE SET
                  is_manual_override = TRUE;
              """
        try:
            self.db.cursor.execute(sql)
            self.db.conn.commit()
            self.logger.debug("<< kanto_overrides")
        except Exception as e:
            self.logger.error(f"Kanto Overrides failed: {e}")
            self.db.conn.rollback()
            raise

    def sync_surf_milestones(self):
        """
        Updates the DB milestones with the Surf flag based on the config
        in Constants.py.
        """
        self.logger.debug(">> sync_surf_milestones")

    
        sql = """
              UPDATE milestones
              SET unlocks_surf = TRUE
              WHERE stage_name = %s
                AND game_id = (SELECT id FROM games WHERE name = %s); \
              """
    
        try:
            for milestone_name, slugs in SURF_MILESTONE.items():
                for slug in slugs:
                    self.db.cursor.execute(sql, (milestone_name, slug))
    
            self.db.conn.commit()
            self.logger.debug("<< sync_surf_milestones")
        except Exception as e:
            self.db.conn.rollback()
            self.logger.error(f"Failed to sync surf milestones: {e}")
