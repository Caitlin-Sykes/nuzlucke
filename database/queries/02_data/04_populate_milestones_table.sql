INSERT INTO milestones (game_id, game_slug, stage_name, trainer_name, level_cap, order_index, is_major_boss)
SELECT
    g.id,
    m.game_slug,
    m.stage_name,
    m.trainer_name,
    m.level_cap,
    m.order_index,
    m.is_major_boss
FROM (
         VALUES
             -- Red/Blue Caps
             ('red-blue', 'Rival Battle', 'Blue', 5, 1, TRUE),
             ('red-blue', 'Pewter City - Gym 1', 'Brock', 14, 2, TRUE),
             ('red-blue', 'Cerulean City - Gym 2', 'Misty', 21, 3, TRUE),
             ('red-blue', 'Vermillion City - Gym 3', 'Lt. Surge', 24, 4, TRUE),
             ('red-blue', 'Celadon City - Gym 4', 'Erika', 29, 5, TRUE),
             ('red-blue', 'Fuchsia City - Gym 5', 'Koga', 43, 6, TRUE),
             ('red-blue', 'Saffron City - Gym 6', 'Sabrina', 43, 7, TRUE),
             ('red-blue', 'Cinnabar Island - Gym 7', 'Blaine', 47, 8, TRUE),
             ('red-blue', 'Viridian City - Gym 8', 'Giovanni', 50, 9, TRUE),
             ('red-blue', 'Elite Four 1', 'Lorelei', 56, 10, TRUE),
             ('red-blue', 'Elite Four 2', 'Bruno', 58, 11, TRUE),
             ('red-blue', 'Elite Four 3', 'Agatha', 60, 12, TRUE),
             ('red-blue', 'Elite Four 4', 'Lance', 62, 13, TRUE),
             ('red-blue', 'Champion', 'Blue', 65, 14, TRUE),

             -- Yellow
             ('yellow', 'Pewter City - Gym 1', 'Brock', 12, 1, TRUE),
             ('yellow', 'Cerulean City - Gym 2', 'Misty', 21, 2, TRUE),
             ('yellow', 'Vermillion City - Gym 3', 'Lt. Surge', 28, 3, TRUE),
             ('yellow', 'Celadon City - Gym 4', 'Erika', 32, 4, TRUE),
             ('yellow', 'Fuchsia City - Gym 5', 'Koga', 50, 5, TRUE),
             ('yellow', 'Saffron City - Gym 6', 'Sabrina', 50, 6, TRUE),
             ('yellow', 'Cinnabar Island - Gym 7', 'Blaine', 54, 7, TRUE),
             ('yellow', 'Viridian City - Gym 8', 'Giovanni', 55, 8, TRUE),
             ('yellow', 'Elite Four 1', 'Lorelei', 56, 9, TRUE),
             ('yellow', 'Elite Four 2', 'Bruno', 58, 10, TRUE),
             ('yellow', 'Elite Four 3', 'Agatha', 60, 11, TRUE),
             ('yellow', 'Elite Four 4', 'Lance', 62, 12, TRUE),
             ('yellow', 'Champion', 'Blue', 65, 13, TRUE),

             -- Gen 2 (Gold/Silver)
             -- Johto League
             ('gold-silver', 'Violet City - Gym 1', 'Falkner', 9, 1, TRUE),
             ('gold-silver', 'Azalea Town - Gym 2', 'Bugsy', 16, 2, TRUE),
             ('gold-silver', 'Goldenrod City - Gym 3', 'Whitney', 20, 3, TRUE),
             ('gold-silver', 'Ecruteak City - Gym 4', 'Morty', 25, 4, TRUE),
             ('gold-silver', 'Cianwood City - Gym 5', 'Chuck', 30, 5, TRUE),
             ('gold-silver', 'Olivine City - Gym 6', 'Jasmine', 35, 6, TRUE),
             ('gold-silver', 'Mahogany Town - Gym 7', 'Pryce', 31, 7, TRUE),
             ('gold-silver', 'Blackthorn City - Gym 8', 'Clair', 40, 8, TRUE),
             ('gold-silver', 'Elite Four 1', 'Will', 42, 9, TRUE),
             ('gold-silver', 'Elite Four 2', 'Koga', 44, 10, TRUE),
             ('gold-silver', 'Elite Four 3', 'Bruno', 46, 11, TRUE),
             ('gold-silver', 'Elite Four 4', 'Karen', 47, 12, TRUE),
             ('gold-silver', 'Champion', 'Lance', 50, 13, TRUE),

              -- Kanto Post-Game
             ('gold-silver', 'Vermilion City - Gym 9', 'Lt. Surge', 45, 14, TRUE),
             ('gold-silver', 'Saffron City - Gym 10', 'Sabrina', 48, 15, TRUE),
             ('gold-silver', 'Celadon City - Gym 11', 'Erika', 46, 16, TRUE),
             ('gold-silver', 'Fuchsia City - Gym 12', 'Janine', 39, 17, TRUE),
             ('gold-silver', 'Cerulean City - Gym 13', 'Misty', 47, 18, TRUE),
             ('gold-silver', 'Pewter City - Gym 14', 'Brock', 44, 19, TRUE),
             ('gold-silver', 'Seafoam Islands - Gym 15', 'Blaine', 50, 20, TRUE),
             ('gold-silver', 'Viridian City - Gym 16', 'Blue', 58, 21, TRUE),

             -- Final Boss
             ('gold-silver', 'Mt. Silver - Final Boss', 'Red', 81, 22, TRUE),

             -- Gen 2 (Crystal)
             -- Johto League
             ('crystal', 'Violet City - Gym 1', 'Falkner', 9, 1, TRUE),
             ('crystal', 'Azalea Town - Gym 2', 'Bugsy', 16, 2, TRUE),
             ('crystal', 'Goldenrod City - Gym 3', 'Whitney', 20, 3, TRUE),
             ('crystal', 'Ecruteak City - Gym 4', 'Morty', 25, 4, TRUE),
             ('crystal', 'Cianwood City - Gym 5', 'Chuck', 30, 5, TRUE),
             ('crystal', 'Olivine City - Gym 6', 'Jasmine', 35, 6, TRUE),
             ('crystal', 'Mahogany Town - Gym 7', 'Pryce', 31, 7, TRUE),
             ('crystal', 'Blackthorn City - Gym 8', 'Clair', 40, 8, TRUE),
             ('crystal', 'Elite Four 1', 'Will', 42, 9, TRUE),
             ('crystal', 'Elite Four 2', 'Koga', 44, 10, TRUE),
             ('crystal', 'Elite Four 3', 'Bruno', 46, 11, TRUE),
             ('crystal', 'Elite Four 4', 'Karen', 47, 12, TRUE),
             ('crystal', 'Champion', 'Lance', 50, 13, TRUE),

             -- Kanto Post-Game
             ('crystal', 'Vermilion City - Gym 9', 'Lt. Surge', 45, 14, TRUE),
             ('crystal', 'Saffron City - Gym 10', 'Sabrina', 48, 15, TRUE),
             ('crystal', 'Celadon City - Gym 11', 'Erika', 46, 16, TRUE),
             ('crystal', 'Fuchsia City - Gym 12', 'Janine', 39, 17, TRUE),
             ('crystal', 'Cerulean City - Gym 13', 'Misty', 47, 18, TRUE),
             ('crystal', 'Pewter City - Gym 14', 'Brock', 44, 19, TRUE),
             ('crystal', 'Seafoam Islands - Gym 15', 'Blaine', 50, 20, TRUE),
             ('crystal', 'Viridian City - Gym 16', 'Blue', 58, 21, TRUE),

             -- Final Boss
             ('crystal', 'Mt. Silver - Final Boss', 'Red', 81, 22, TRUE),

             -- Gen 3 - Ruby/Sapphire
             ('ruby-sapphire', 'Rustboro City - Gym 1', 'Roxanne', 15, 1, TRUE),
             ('ruby-sapphire', 'Dewford Town - Gym 2', 'Brawly', 18, 2, TRUE),
             ('ruby-sapphire', 'Mauville City - Gym 3', 'Wattson', 23, 3, TRUE),
             ('ruby-sapphire', 'Lavaridge Town - Gym 4', 'Flannery', 28, 4, TRUE),
             ('ruby-sapphire', 'Petalburg City - Gym 5', 'Norman', 31, 5, TRUE),
             ('ruby-sapphire', 'Fortree City - Gym 6', 'Winona', 33, 6, TRUE),
             ('ruby-sapphire', 'Mossdeep City - Gym 7', 'Tate and Liza', 42, 7, TRUE),
             ('ruby-sapphire', 'Sootopolis City - Gym 8', 'Wallace', 43, 8, TRUE),
             ('ruby-sapphire', 'Elite Four 1', 'Sidney', 49, 9, TRUE),
             ('ruby-sapphire', 'Elite Four 2', 'Phoebe', 51, 10, TRUE),
             ('ruby-sapphire', 'Elite Four 3', 'Glacia', 53, 11, TRUE),
             ('ruby-sapphire', 'Elite Four 4', 'Drake', 55, 12, TRUE),
             ('ruby-sapphire', 'Champion', 'Steven', 58, 13, TRUE),

             -- Emerald
             ('emerald', 'Rustboro City - Gym 1', 'Roxanne', 15, 1, TRUE),
             ('emerald', 'Dewford Town - Gym 2', 'Brawly', 19, 2, TRUE),
             ('emerald', 'Mauville City - Gym 3', 'Wattson', 24, 3, TRUE),
             ('emerald', 'Lavaridge Town - Gym 4', 'Flannery', 29, 4, TRUE),
             ('emerald', 'Petalburg City - Gym 5', 'Norman', 31, 5, TRUE),
             ('emerald', 'Fortree City - Gym 6', 'Winona', 33, 6, TRUE),
             ('emerald', 'Mossdeep City - Gym 7', 'Tate and Liza', 42, 7, TRUE),
             ('emerald', 'Sootopolis City - Gym 8', 'Juan', 46, 8, TRUE),
             ('emerald', 'Elite Four 1', 'Sidney', 49, 9, TRUE),
             ('emerald', 'Elite Four 2', 'Phoebe', 51, 10, TRUE),
             ('emerald', 'Elite Four 3', 'Glacia', 53, 11, TRUE),
             ('emerald', 'Elite Four 4', 'Drake', 55, 12, TRUE),
             ('emerald', 'Champion', 'Wallace', 58, 13, TRUE),

             -- Fire-Red, Leafgreen
             ('firered-leafgreen', 'Pewter City - Gym 1', 'Brock', 14, 1, TRUE),
             ('firered-leafgreen', 'Cerulean City - Gym 2', 'Misty', 21, 2, TRUE),
             ('firered-leafgreen', 'Vermilion City - Gym 3', 'Lt. Surge', 24, 3, TRUE),
             ('firered-leafgreen', 'Celadon City - Gym 4', 'Erika', 29, 4, TRUE),
             ('firered-leafgreen', 'Fuchsia City - Gym 5', 'Koga', 43, 5, TRUE),
             ('firered-leafgreen', 'Saffron City - Gym 6', 'Sabrina', 43, 6, TRUE),
             ('firered-leafgreen', 'Cinnabar Island - Gym 7', 'Blaine', 47, 7, TRUE),
             ('firered-leafgreen', 'Viridian City - Gym 8', 'Giovanni', 50, 8, TRUE),
             ('firered-leafgreen', 'Elite Four 1', 'Lorelei', 54, 9, TRUE),
             ('firered-leafgreen', 'Elite Four 2', 'Bruno', 56, 10, TRUE),
             ('firered-leafgreen', 'Elite Four 3', 'Agatha', 58, 11, TRUE),
             ('firered-leafgreen', 'Elite Four 4', 'Lance', 60, 12, TRUE),
             ('firered-leafgreen', 'Champion', 'Blue', 63, 13, TRUE),
             -- Rematches
             ('firered-leafgreen', 'Elite Four 1 Rematch', 'Lorelei', 66, 14, TRUE),
             ('firered-leafgreen', 'Elite Four 2 Rematch', 'Bruno', 68, 15, TRUE),
             ('firered-leafgreen', 'Elite Four 3 Rematch', 'Agatha', 70, 16, TRUE),
             ('firered-leafgreen', 'Elite Four 4 Rematch', 'Lance', 72, 17, TRUE),
             ('firered-leafgreen', 'Champion Rematch', 'Blue', 75, 18, TRUE),
             
             -- Gen 4 - Diamond/Pearl  
             ('diamond-pearl', 'Oreburgh City - Gym 1', 'Roark', 14, 1, TRUE),
             ('diamond-pearl', 'Eterna City - Gym 2', 'Gardenia', 22, 2, TRUE),
             ('diamond-pearl', 'Veilstone City - Gym 3', 'Maylene', 30, 3, TRUE),
             ('diamond-pearl', 'Pastoria City - Gym 4', 'Crasher Wake', 30, 4, TRUE),
             ('diamond-pearl', 'Hearthome City - Gym 5', 'Fantina', 36, 5, TRUE),
             ('diamond-pearl', 'Canalave City - Gym 6', 'Byron', 39, 6, TRUE),
             ('diamond-pearl', 'Snowpoint City - Gym 7', 'Candice', 42, 7, TRUE),
             ('diamond-pearl', 'Sunyshore City - Gym 8', 'Volkner', 49, 8, TRUE),
             ('diamond-pearl', 'Elite Four 1', 'Aaron', 57, 9, TRUE),
             ('diamond-pearl', 'Elite Four 2', 'Bertha', 59, 10, TRUE),
             ('diamond-pearl', 'Elite Four 3', 'Flint', 61, 11, TRUE),
             ('diamond-pearl', 'Elite Four 4', 'Lucian', 63, 12, TRUE),
             ('diamond-pearl', 'Champion', 'Cynthia', 66, 13, TRUE),
            
            -- Platinum
             ('platinum', 'Oreburgh City - Gym 1', 'Roark', 14, 1, TRUE),
             ('platinum', 'Eterna City - Gym 2', 'Gardenia', 22, 2, TRUE),
             ('platinum', 'Hearthome City - Gym 3', 'Fantina', 26, 3, TRUE),
             ('platinum', 'Veilstone City - Gym 4', 'Maylene', 32, 4, TRUE),
             ('platinum', 'Pastoria City - Gym 5', 'Crasher Wake', 37, 5, TRUE),
             ('platinum', 'Canalave City - Gym 6', 'Byron', 41, 6, TRUE),
             ('platinum', 'Snowpoint City - Gym 7', 'Candice', 44, 7, TRUE),
             ('platinum', 'Sunyshore City - Gym 8', 'Volkner', 50, 8, TRUE),
             ('platinum', 'Elite Four 1', 'Aaron', 53, 9, TRUE),
             ('platinum', 'Elite Four 2', 'Bertha', 55, 10, TRUE),
             ('platinum', 'Elite Four 3', 'Flint', 57, 11, TRUE),
             ('platinum', 'Elite Four 4', 'Lucian', 59, 12, TRUE),
             ('platinum', 'Champion', 'Cynthia', 62, 13, TRUE),
             ('platinum', 'Battle Frontier Tag', 'Volkner and Flint', 58, 14, TRUE),
             ('platinum', 'Elite Four 1 Rematch', 'Aaron', 69, 15, TRUE),
             ('platinum', 'Elite Four 2 Rematch', 'Bertha', 71, 16, TRUE),
             ('platinum', 'Elite Four 3 Rematch', 'Flint', 73, 17, TRUE),
             ('platinum', 'Elite Four 4 Rematch', 'Lucian', 75, 18, TRUE),
             ('platinum', 'Champion Rematch', 'Cynthia', 78, 19, TRUE),
         
            -- Heartgold/Soulsilver
             -- Johto
             ('heartgold-soulsilver', 'Violet City - Gym 1', 'Falkner', 13, 1, TRUE),
             ('heartgold-soulsilver', 'Azalea Town - Gym 2', 'Bugsy', 17, 2, TRUE),
             ('heartgold-soulsilver', 'Goldenrod City - Gym 3', 'Whitney', 19, 3, TRUE),
             ('heartgold-soulsilver', 'Ecruteak City - Gym 4', 'Morty', 25, 4, TRUE),
             ('heartgold-soulsilver', 'Cianwood City - Gym 5', 'Chuck', 31, 5, TRUE),
             ('heartgold-soulsilver', 'Olivine City - Gym 6', 'Jasmine', 35, 6, TRUE),
             ('heartgold-soulsilver', 'Mahogany Town - Gym 7', 'Pryce', 34, 7, TRUE),
             ('heartgold-soulsilver', 'Blackthorn City - Gym 8', 'Clair', 41, 8, TRUE),
             -- Kanto
             ('heartgold-soulsilver', 'Vermilion City - Kanto 1', 'Lt. Surge', 53, 14, TRUE),
             ('heartgold-soulsilver', 'Saffron City - Kanto 2', 'Sabrina', 55, 15, TRUE),
             ('heartgold-soulsilver', 'Celadon City - Kanto 3', 'Erika', 56, 16, TRUE),
             ('heartgold-soulsilver', 'Cerulean City - Kanto 4', 'Misty', 54, 17, TRUE),
             ('heartgold-soulsilver', 'Fuchsia City - Kanto 5', 'Janine', 50, 18, TRUE),
             ('heartgold-soulsilver', 'Pewter City - Kanto 6', 'Brock', 54, 19, TRUE),
             ('heartgold-soulsilver', 'Seafoam Island - Kanto 7', 'Blaine', 59, 20, TRUE),
             ('heartgold-soulsilver', 'Viridian City - Kanto 8', 'Blue', 60, 21, TRUE),
             ('heartgold-soulsilver', 'Elite Four 1', 'Will', 42, 9, TRUE),
             ('heartgold-soulsilver', 'Elite Four 2', 'Koga', 44, 10, TRUE),
             ('heartgold-soulsilver', 'Elite Four 3', 'Bruno', 46, 11, TRUE),
             ('heartgold-soulsilver', 'Elite Four 4', 'Karen', 47, 12, TRUE),
             ('heartgold-soulsilver', 'Champion', 'Lance', 50, 13, TRUE),
             -- Rematches
             ('heartgold-soulsilver', 'Elite Four 1 Rematch', 'Will', 62, 22, TRUE),
             ('heartgold-soulsilver', 'Elite Four 2 Rematch', 'Koga', 64, 23, TRUE),
             ('heartgold-soulsilver', 'Elite Four 3 Rematch', 'Bruno', 64, 24, TRUE),
             ('heartgold-soulsilver', 'Elite Four 4 Rematch', 'Karen', 64, 25, TRUE),
             ('heartgold-soulsilver', 'Champion Rematch', 'Lance', 75, 26, TRUE)
     ) AS m(game_slug, stage_name, trainer_name, level_cap, order_index, is_major_boss)
         JOIN games g ON (
    (m.game_slug = 'red-blue' AND g.name IN ('red', 'blue')) OR
    (m.game_slug = 'yellow' AND g.name = 'yellow') OR
    (m.game_slug = 'gold-silver' AND g.name IN ('gold', 'silver')) OR
    (m.game_slug = 'ruby-sapphire' AND g.name IN ('ruby', 'sapphire')) OR
    (m.game_slug = 'crystal' AND g.name = 'crystal') OR
    (m.game_slug = 'emerald' AND g.name = 'emerald') OR 
    (m.game_slug = 'firered-leafgreen' AND g.name IN ('firered', 'leafgreen')) OR
    (m.game_slug = 'diamond-pearl' AND g.name IN ('diamond', 'pearl')) OR
    (m.game_slug = 'platinum' AND g.name IN ('platinum')) OR
    (m.game_slug = 'heartgold-soulsilver' AND g.name IN ('heartgold', 'soulsilver'))
    )
ON CONFLICT (game_id, order_index) DO UPDATE SET
                                                 level_cap = EXCLUDED.level_cap,
                                                 game_slug = EXCLUDED.game_slug,
                                                 stage_name = EXCLUDED.stage_name,
                                                 trainer_name = EXCLUDED.trainer_name,
                                                 is_major_boss = EXCLUDED.is_major_boss;