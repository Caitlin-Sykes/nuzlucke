INSERT INTO milestone_teams (milestone_id, pokemon_id, slot_number, level, is_ace, moves, condition)
SELECT m.id, p.id, t.slot, t.lvl, t.ace, t.moves_arr, t.condition
FROM (
         VALUES
             -- First Rival Battle - If Player Chose Bulbasaur
             ('Rival Battle', 'charmander', 1, 5, TRUE, ARRAY['tackle', 'defense-curl'],'bulbasaur'),
             -- First Rival Battle - If Player Chose Squirtle
             ('Rival Battle', 'bulbasaur', 1, 5, TRUE, ARRAY['tackle', 'defense-curl'],'squirtle'),
             -- First Rival Battle - If Player Chose Charmander
             ('Rival Battle', 'squirtle', 1, 5, TRUE, ARRAY['tackle', 'defense-curl'],'charmander'),
             
             -- Gym 1: Brock
             ('Pewter City - Gym 1', 'geodude', 1, 12, FALSE, ARRAY['tackle', 'defense-curl'], NULL),
             ('Pewter City - Gym 1', 'onix', 2, 14, TRUE, ARRAY['tackle', 'screech', 'bide'], NULL),

             -- Gym 2: Misty
             ('Cerulean City - Gym 2', 'staryu', 1, 18, FALSE, ARRAY['tackle', 'water-gun'], NULL),
             ('Cerulean City - Gym 2', 'starmie', 2, 21, TRUE, ARRAY['tackle', 'water-gun', 'harden', 'bubble-beam'], NULL),

             -- Gym 3: Lt. Surge
             ('Vermillion City - Gym 3', 'voltorb', 1, 21, FALSE, ARRAY['tackle', 'screech', 'sonic-boom'], NULL),
             ('Vermillion City - Gym 3', 'pikachu', 2, 18, FALSE, ARRAY['thunder-shock', 'thunder-wave', 'growl', 'quick-attack'], NULL),
             ('Vermillion City - Gym 3', 'raichu', 3, 24, TRUE, ARRAY['thunderbolt', 'thunder-shock', 'thunder-wave', 'growl'], NULL),

             -- Gym 4: Erika
             ('Celadon City - Gym 4', 'victreebel', 1, 29, FALSE, ARRAY['wrap', 'poison-powder', 'sleep-powder', 'razor-leaf'], NULL),
             ('Celadon City - Gym 4', 'tangela', 2, 24, FALSE, ARRAY['bind', 'constrict'], NULL),
             ('Celadon City - Gym 4', 'vileplume', 3, 29, TRUE, ARRAY['poison-powder', 'mega-drain', 'sleep-powder', 'petal-dance'], NULL),

             -- Gym 5: Koga
             ('Fuchsia City - Gym 5', 'koffing', 1, 37, FALSE, ARRAY['tackle', 'smog', 'sludge', 'smokescreen'], NULL),
             ('Fuchsia City - Gym 5', 'muk', 2, 39, FALSE, ARRAY['disable', 'poison-gas', 'minimize', 'sludge'], NULL),
             ('Fuchsia City - Gym 5', 'koffing', 3, 37, FALSE, ARRAY['tackle', 'smog', 'sludge', 'smokescreen'], NULL),
             ('Fuchsia City - Gym 5', 'weezing', 4, 43, TRUE, ARRAY['smog', 'sludge', 'toxic', 'self-destruct'], NULL),

             -- Gym 6: Sabrina
             ('Saffron City - Gym 6', 'kadabra', 1, 38, FALSE, ARRAY['disable', 'psybeam', 'recover', 'psychic'], NULL),
             ('Saffron City - Gym 6', 'mr-mime', 2, 37, FALSE, ARRAY['confusion', 'barrier', 'light-screen', 'double-slap'], NULL),
             ('Saffron City - Gym 6', 'venomoth', 3, 38, FALSE, ARRAY['poison-powder', 'leech-life', 'stun-spore', 'psybeam'], NULL),
             ('Saffron City - Gym 6', 'alakazam', 4, 43, TRUE, ARRAY['psybeam', 'recover', 'psywave', 'reflect'], NULL),

             -- Gym 7: Blaine
             ('Cinnabar City - Gym 7', 'growlithe', 1, 42, FALSE, ARRAY['ember', 'leer', 'take-down', 'agility'], NULL),
             ('Cinnabar City - Gym 7', 'ponyta', 2, 40, FALSE, ARRAY['tail-whip', 'stomp', 'growl', 'fire-spin'], NULL),
             ('Cinnabar City - Gym 7', 'rapidash', 3, 42, FALSE, ARRAY['tail-whip', 'stomp', 'growl', 'fire-spin'], NULL),
             ('Cinnabar City - Gym 7', 'arcanine', 4, 47, TRUE, ARRAY['roar', 'ember', 'take-down', 'fire-blast'], NULL),

             -- Gym 8: Giovanni
             ('Viridian City - Gym 8', 'rhyhorn', 1, 45, FALSE, ARRAY['stomp', 'tail-whip', 'fury-attack', 'horn-attack'], NULL),
             ('Viridian City - Gym 8', 'dugtrio', 2, 42, FALSE, ARRAY['growl', 'dig', 'sand-attack', 'slash'], NULL),
             ('Viridian City - Gym 8', 'nidoqueen', 3, 44, FALSE, ARRAY['scratch', 'tail-whip', 'poison-sting', 'body-slam'], NULL),
             ('Viridian City - Gym 8', 'nidoking', 4, 45, FALSE, ARRAY['tackle', 'horn-attack', 'poison-sting', 'thrash'], NULL),
             ('Viridian City - Gym 8', 'rhydon', 5, 50, TRUE, ARRAY['stomp', 'tail-whip', 'fissure', 'horn-drill'], NULL),

             -- LORELEI
             ('Elite Four 1', 'dewgong', 1, 54, FALSE, ARRAY['growl', 'aurora-beam', 'rest', 'take-down'], NULL),
            ('Elite Four 1', 'cloyster', 2, 53, FALSE, ARRAY['supersonic', 'clamp', 'aurora-beam', 'spike-cannon'], NULL),
            ('Elite Four 1', 'slowbro', 3, 54, FALSE, ARRAY['water-gun', 'growl', 'withdraw', 'amnesia'], NULL),
            ('Elite Four 1', 'jynx', 4, 56, FALSE, ARRAY['double-slap', 'ice-punch', 'body-slam', 'thrash'], NULL),
            ('Elite Four 1', 'lapras', 5, 56, TRUE, ARRAY['body-slam', 'confuse-ray', 'hydro-pump', 'blizzard'], NULL),
    
            -- BRUNO
            ('Elite Four 2', 'onix', 1, 53, FALSE, ARRAY['rock-throw', 'rage', 'slam', 'harden'], NULL),
            ('Elite Four 2', 'hitmonchan', 2, 55, FALSE, ARRAY['ice-punch', 'mega-punch', 'thunder-punch', 'counter'], NULL),
            ('Elite Four 2', 'hitmonlee', 3, 55, FALSE, ARRAY['jump-kick', 'focus-energy', 'high-jump-kick', 'mega-kick'], NULL),
            ('Elite Four 2', 'onix', 4, 56, FALSE, ARRAY['rock-throw', 'rage', 'slam', 'harden'], NULL),
            ('Elite Four 2', 'machamp', 5, 58, TRUE, ARRAY['leer', 'focus-energy', 'fissure', 'submission'], NULL),
    
            -- AGATHA
            ('Elite Four 3', 'gengar', 1, 56, FALSE, ARRAY['confuse-ray', 'night-shade', 'hypnosis', 'dream-eater'], NULL),
            ('Elite Four 3', 'golbat', 2, 56, FALSE, ARRAY['supersonic', 'confuse-ray', 'wing-attack', 'haze'], NULL),
            ('Elite Four 3', 'haunter', 3, 55, FALSE, ARRAY['confuse-ray', 'night-shade', 'hypnosis', 'dream-eater'], NULL),
            ('Elite Four 3', 'arbok', 4, 58, FALSE, ARRAY['bite', 'glare', 'screech', 'acid'], NULL),
            ('Elite Four 3', 'gengar', 5, 60, TRUE, ARRAY['confuse-ray', 'night-shade', 'toxic', 'dream-eater'], NULL),
    
            -- LANCE
            ('Elite Four 4', 'gyarados', 1, 58, FALSE, ARRAY['hydro-pump', 'dragon-rage', 'leer', 'hyper-beam'], NULL),
            ('Elite Four 4', 'dragonair', 2, 56, FALSE, ARRAY['agility', 'slam', 'dragon-rage', 'hyper-beam'], NULL),
            ('Elite Four 4', 'dragonair', 3, 56, FALSE, ARRAY['agility', 'slam', 'dragon-rage', 'hyper-beam'], NULL),
            ('Elite Four 4', 'aerodactyl', 4, 60, FALSE, ARRAY['supersonic', 'take-down', 'bite', 'hyper-beam'], NULL),
            ('Elite Four 4', 'dragonite', 5, 62, TRUE, ARRAY['agility', 'slam', 'barrier', 'hyper-beam'], NULL),
    
            -- CHAMPION (Fixed Members)
            ('Champion', 'pidgeot', 1, 61, FALSE, ARRAY['wing-attack', 'mirror-move', 'sky-attack', 'whirlwind'], NULL),
            ('Champion', 'alakazam', 2, 59, FALSE, ARRAY['psybeam', 'psychic', 'reflect', 'recover'], NULL),
            ('Champion', 'rhydon', 3, 61, FALSE, ARRAY['leer', 'tail-whip', 'fury-attack', 'horn-drill'], NULL),
    
            -- CHAMPION (Variable - Player chose Squirtle)
            ('Champion', 'arcanine', 4, 61, FALSE, ARRAY['roar', 'leer', 'ember', 'take-down'], 'squirtle'),
            ('Champion', 'gyarados', 5, 63, FALSE, ARRAY['dragon-rage', 'hydro-pump', 'hyper-beam', 'leer'], 'squirtle'),
            ('Champion', 'venusaur', 6, 65, TRUE, ARRAY['growth', 'mega-drain', 'razor-leaf', 'solar-beam'], 'squirtle'),
    
            -- CHAMPION (Variable - Player chose Bulbasaur)
            ('Champion', 'gyarados', 4, 61, FALSE, ARRAY['dragon-rage', 'hydro-pump', 'hyper-beam', 'leer'], 'bulbasaur'),
            ('Champion', 'exeggutor', 5, 63, FALSE, ARRAY['hypnosis', 'barrage', 'stomp'], 'bulbasaur'),
            ('Champion', 'charizard', 6, 65, TRUE, ARRAY['fire-blast', 'rage', 'slash', 'fire-spin'], 'bulbasaur'),
    
            -- CHAMPION (Variable - Player chose Charmander)
            ('Champion', 'exeggutor', 4, 61, FALSE, ARRAY['hypnosis', 'barrage', 'stomp'], 'charmander'),
            ('Champion', 'arcanine', 5, 63, FALSE, ARRAY['roar', 'leer', 'ember', 'take-down'], 'charmander'),
            ('Champion', 'blastoise', 6, 65, TRUE, ARRAY['hydro-pump', 'blizzard', 'bite', 'withdraw'], 'charmander')
             
     ) AS t(stage_search, p_name, slot, lvl, ace, moves_arr, condition)
         JOIN pokemon p ON p.name = t.p_name
         JOIN milestones m ON m.stage_name = t.stage_search
         JOIN games g ON m.game_id = g.id
WHERE g.name IN ('red', 'blue', NULL);

INSERT INTO milestone_teams (milestone_id, pokemon_id, slot_number, level, is_ace, moves, condition)
SELECT m.id, p.id, t.slot, t.lvl, t.ace, t.moves_arr, t.condition
FROM (
         VALUES
             -- Gym 1: Brock
             ('Pewter City - Gym 1', 'geodude', 1, 10, FALSE, ARRAY['tackle'], NULL),
             ('Pewter City - Gym 1', 'onix', 2, 12, TRUE, ARRAY['tackle', 'screech', 'bide', 'bind'], NULL),

             -- Gym 2: Misty
             ('Cerulean City - Gym 2', 'staryu', 1, 18, FALSE, ARRAY['tackle', 'water-gun'], NULL),
             ('Cerulean City - Gym 2', 'starmie', 2, 21, TRUE, ARRAY['tackle', 'water-gun', 'harden', 'bubble-beam'], NULL),

             -- Gym 3: Lt. Surge (Yellow only has Raichu)
             ('Vermillion City - Gym 3', 'raichu', 1, 28, TRUE, ARRAY['thunderbolt', 'growl', 'mega-punch', 'mega-kick'], NULL),

             -- Gym 4: Erika
             ('Celadon City - Gym 4', 'weepinbell', 1, 32, FALSE, ARRAY['wrap', 'stun-spore', 'sleep-powder', 'razor-leaf'], NULL),
             ('Celadon City - Gym 4', 'tangela', 2, 30, FALSE, ARRAY['bind', 'mega-drain', 'vine-whip', 'constrict'], NULL),
             ('Celadon City - Gym 4', 'gloom', 3, 32, TRUE, ARRAY['acid', 'petal-dance', 'stun-spore', 'sleep-powder'], NULL),

             -- Gym 5: Koga (The Venonat Army)
             ('Fuchsia City - Gym 5', 'venonat', 1, 44, FALSE, ARRAY['tackle', 'toxic', 'sleep-powder', 'psychic'], NULL),
             ('Fuchsia City - Gym 5', 'venonat', 2, 46, FALSE, ARRAY['toxic', 'psybeam', 'supersonic', 'psychic'], NULL),
             ('Fuchsia City - Gym 5', 'venonat', 3, 48, FALSE, ARRAY['toxic', 'psychic', 'sleep-powder', 'double-edge'], NULL),
             ('Fuchsia City - Gym 5', 'venomoth', 4, 50, TRUE, ARRAY['toxic', 'psychic', 'leech-life', 'double-team'], NULL),

             -- Gym 6: Sabrina
             ('Saffron City - Gym 6', 'abra', 1, 50, FALSE, ARRAY['teleport', 'flash'], NULL),
             ('Saffron City - Gym 6', 'kadabra', 2, 50, FALSE, ARRAY['psychic', 'recover', 'kinesis', 'psywave'], NULL),
             ('Saffron City - Gym 6', 'alakazam', 3, 50, TRUE, ARRAY['psychic', 'psywave', 'reflect', 'recover'], NULL),

             -- Gym 7: Blaine
             ('Cinnabar City - Gym 7', 'ninetales', 1, 48, FALSE, ARRAY['confuse-ray', 'quick-attack', 'tail-whip', 'flamethrower'], NULL),
             ('Cinnabar City - Gym 7', 'rapidash', 2, 50, FALSE, ARRAY['take-down', 'stomp', 'growl', 'fire-spin'], NULL),
             ('Cinnabar City - Gym 7', 'arcanine', 3, 54, TRUE, ARRAY['reflect', 'flamethrower', 'take-down', 'fire-blast'], NULL),

             -- Gym 8: Giovanni
             ('Viridian City - Gym 8', 'dugtrio', 1, 50, FALSE, ARRAY['sand-attack', 'dig', 'fissure', 'earthquake'], NULL),
             ('Viridian City - Gym 8', 'persian', 2, 53, FALSE, ARRAY['screech', 'slash', 'fury-swipes', 'double-team'], NULL),
             ('Viridian City - Gym 8', 'nidoqueen', 3, 53, FALSE, ARRAY['tail-whip', 'double-kick', 'poison-sting', 'thunder'], NULL),
             ('Viridian City - Gym 8', 'nidoking', 4, 55, FALSE, ARRAY['thunder', 'leer', 'earthquake', 'thrash'], NULL),
             ('Viridian City - Gym 8', 'rhydon', 5, 55, TRUE, ARRAY['rock-slide', 'fury-attack', 'earthquake', 'horn-drill'], NULL),

             -- LORELEI
             ('Elite Four 1', 'dewgong', 1, 54, FALSE, ARRAY['bubble-beam', 'aurora-beam', 'rest', 'take-down'], NULL),
             ('Elite Four 1', 'cloyster', 2, 53, FALSE, ARRAY['supersonic', 'clamp', 'ice-beam', 'spike-cannon'], NULL),
             ('Elite Four 1', 'slowbro', 3, 54, FALSE, ARRAY['surf', 'psychic', 'withdraw', 'amnesia'], NULL),
             ('Elite Four 1', 'jynx', 4, 56, FALSE, ARRAY['double-slap', 'ice-punch', 'lovely-kiss', 'thrash'], NULL),
             ('Elite Four 1', 'lapras', 5, 56, TRUE, ARRAY['body-slam', 'confuse-ray', 'hydro-pump', 'blizzard'], NULL),

             -- BRUNO
             ('Elite Four 2', 'onix', 1, 53, FALSE, ARRAY['rock-throw', 'dig', 'slam', 'screech'], NULL),
             ('Elite Four 2', 'hitmonchan', 2, 55, FALSE, ARRAY['ice-punch', 'fire-punch', 'thunder-punch', 'double-team'], NULL),
             ('Elite Four 2', 'hitmonlee', 3, 55, FALSE, ARRAY['double-kick', 'double-team', 'high-jump-kick', 'mega-kick'], NULL),
             ('Elite Four 2', 'onix', 4, 56, FALSE, ARRAY['rock-slide', 'screech', 'earthquake', 'slam'], NULL),
             ('Elite Four 2', 'machamp', 5, 58, TRUE, ARRAY['leer', 'strength', 'karate-chop', 'submission'], NULL),

             -- AGATHA
             ('Elite Four 3', 'gengar', 1, 56, FALSE, ARRAY['confuse-ray', 'lick', 'substitute', 'mega-drain'], NULL),
             ('Elite Four 3', 'golbat', 2, 56, FALSE, ARRAY['supersonic', 'leech-life', 'wing-attack', 'toxic'], NULL),
             ('Elite Four 3', 'haunter', 3, 55, FALSE, ARRAY['confuse-ray', 'lick', 'hypnosis', 'dream-eater'], NULL),
             ('Elite Four 3', 'arbok', 4, 58, FALSE, ARRAY['wrap', 'glare', 'screech', 'acid'], NULL),
             ('Elite Four 3', 'gengar', 5, 60, TRUE, ARRAY['confuse-ray', 'psychic', 'hypnosis', 'dream-eater'], NULL),

             -- LANCE
             ('Elite Four 4', 'gyarados', 1, 58, FALSE, ARRAY['hydro-pump', 'dragon-rage', 'leer', 'hyper-beam'], NULL),
             ('Elite Four 4', 'dragonair', 2, 56, FALSE, ARRAY['thunderbolt', 'slam', 'thunder-wave', 'hyper-beam'], NULL),
             ('Elite Four 4', 'dragonair', 3, 56, FALSE, ARRAY['wrap', 'bubble-beam', 'ice-beam', 'hyper-beam'], NULL),
             ('Elite Four 4', 'aerodactyl', 4, 60, FALSE, ARRAY['wing-attack', 'fly', 'swift', 'hyper-beam'], NULL),
             ('Elite Four 4', 'dragonite', 5, 62, TRUE, ARRAY['blizzard', 'fire-blast', 'thunder', 'hyper-beam'], NULL),

             -- CHAMPION (Fixed Base Members)
             ('Champion', 'sandslash', 1, 61, FALSE, ARRAY['earthquake', 'slash', 'poison-sting', 'fury-swipes'], NULL),
             ('Champion', 'alakazam', 2, 59, FALSE, ARRAY['psybeam', 'psychic', 'kinesis', 'recover'], NULL),
             ('Champion', 'exeggutor', 3, 61, FALSE, ARRAY['barrage', 'hypnosis', 'stomp', 'leech-seed'], NULL),

             -- CHAMPION (Variation 1: Vaporeon Path)
             ('Champion', 'magneton', 4, 63, FALSE, ARRAY['thunderbolt', 'thunder-wave', 'screech', 'swift'], '0'),
             ('Champion', 'ninetales', 5, 61, FALSE, ARRAY['fire-spin', 'tail-whip', 'quick-attack', 'confuse-ray'], '0'),
             ('Champion', 'vaporeon', 6, 65, TRUE, ARRAY['hydro-pump', 'aurora-beam', 'quick-attack', 'mist'], '0'),

             -- CHAMPION (Variation 2: Jolteon Path)
             ('Champion', 'ninetales', 4, 63, FALSE, ARRAY['fire-spin', 'tail-whip', 'quick-attack', 'confuse-ray'], '2'),
             ('Champion', 'cloyster', 5, 61, FALSE, ARRAY['ice-beam', 'spike-cannon', 'aurora-beam', 'clamp'], '2'),
             ('Champion', 'jolteon', 6, 65, TRUE, ARRAY['thunder', 'thunderbolt', 'quick-attack', 'pin-missile'], '2'),

             -- CHAMPION (Variation 3: Flareon Path)
             ('Champion', 'cloyster', 4, 63, FALSE, ARRAY['ice-beam', 'spike-cannon', 'aurora-beam', 'clamp'], '1'),
             ('Champion', 'magneton', 5, 61, FALSE, ARRAY['thunderbolt', 'thunder-wave', 'screech', 'swift'], '1'),
             ('Champion', 'flareon', 6, 65, TRUE, ARRAY['flamethrower', 'quick-attack', 'smog', 'fire-spin'], '1')
     ) AS t(stage_search, p_name, slot, lvl, ace, moves_arr, condition)
         JOIN pokemon p ON p.name = t.p_name
         JOIN milestones m ON m.stage_name = t.stage_search
         JOIN games g ON m.game_id = g.id
WHERE g.name IN ('yellow', NULL);

INSERT INTO milestone_teams (milestone_id, pokemon_id, slot_number, level, is_ace, moves, condition)
SELECT m.id, p.id, t.slot, t.lvl, t.ace, t.moves_arr, t.condition
FROM (
         VALUES
             -- Falkner
             ('Violet City - Gym 1', 'pidgey', 1, 7, FALSE, ARRAY['tackle', 'mud-slap'], NULL),
             ('Violet City - Gym 1', 'pidgeotto', 2, 9, TRUE, ARRAY['tackle', 'mud-slap', 'gust'], NULL),

             -- Bugsy
             ('Azalea Town - Gym 2', 'metapod', 1, 14, FALSE, ARRAY['tackle', 'string-shot', 'harden'], NULL),
             ('Azalea Town - Gym 2', 'kakuna', 2, 14, FALSE, ARRAY['poison-sting', 'string-shot', 'harden'], NULL),
             ('Azalea Town - Gym 2', 'scyther', 3, 16, TRUE, ARRAY['quick-attack', 'leer', 'fury-cutter'], NULL),

             -- Whitney
             ('Goldenrod City - Gym 3', 'clefairy', 1, 18, FALSE, ARRAY['double-slap', 'mimic', 'encore', 'metronome'],NULL),
             ('Goldenrod City - Gym 3', 'miltank', 2, 20, TRUE, ARRAY['rollout', 'attract', 'stomp', 'milk-drink'],NULL),

             -- Morty
             ('Ecruteak City - Gym 4', 'gastly', 1, 21, FALSE, ARRAY['lick', 'spite', 'mean-look', 'curse'],NULL),
             ('Ecruteak City - Gym 4', 'haunter', 2, 21, FALSE, ARRAY['hypnosis', 'mimic', 'curse', 'night-shade'],NULL),
             ('Ecruteak City - Gym 4', 'haunter', 3, 23, FALSE, ARRAY['spite', 'mean-look', 'mimic', 'night-shade'],NULL),
             ('Ecruteak City - Gym 4', 'gengar', 4, 25, TRUE, ARRAY['hypnosis', 'shadow-ball', 'mean-look', 'dream-eater'],NULL),

             -- Chuck
             ('Cianwood City - Gym 5', 'primeape', 1, 27, FALSE, ARRAY['leer', 'rage', 'karate-chop', 'fury-swipes'],NULL),
             ('Cianwood City - Gym 5', 'poliwrath', 2, 30, TRUE, ARRAY['hypnosis', 'mind-reader', 'surf', 'dynamic-punch'],NULL),

             -- Jasmine
             ('Olivine City - Gym 6', 'magnemite', 1, 30, FALSE, ARRAY['thunderbolt', 'supersonic', 'sonic-boom', 'thunder-wave'],NULL),
             ('Olivine City - Gym 6', 'magnemite', 2, 30, FALSE, ARRAY['thunderbolt', 'supersonic', 'sonic-boom', 'thunder-wave'],NULL),
             ('Olivine City - Gym 6', 'steelix', 3, 35, TRUE, ARRAY['screech', 'sunny-day', 'rock-throw', 'iron-tail'],NULL),

             -- Pryce
             ('Mahogany Town - Gym 7', 'seel', 1, 27, FALSE, ARRAY['headbutt', 'icy-wind', 'aurora-beam', 'rest'],NULL),
             ('Mahogany Town - Gym 7', 'dewgong', 2, 29, FALSE, ARRAY['headbutt', 'icy-wind', 'aurora-beam', 'rest'],NULL),
             ('Mahogany Town - Gym 7', 'piloswine', 3, 31, TRUE, ARRAY['icy-wind', 'fury-attack', 'mist', 'blizzard'],NULL),

             -- Clair
             ('Blackthorn City - Gym 8', 'dragonair', 1, 37, FALSE, ARRAY['thunder-wave', 'surf', 'slam', 'dragon-breath'],NULL),
             ('Blackthorn City - Gym 8', 'dragonair', 2, 37, FALSE, ARRAY['thunder-wave', 'thunderbolt', 'slam', 'dragon-breath'],NULL),
             ('Blackthorn City - Gym 8', 'dragonair', 3, 37, FALSE, ARRAY['thunder-wave', 'ice-beam', 'slam', 'dragon-breath'],NULL),
             ('Blackthorn City - Gym 8', 'kingdra', 4, 40, TRUE, ARRAY['smokescreen', 'surf', 'hyper-beam', 'dragon-breath'],NULL),
             ('Elite Four 1', 'xatu', 1, 40, FALSE, ARRAY['quick-attack', 'future-sight', 'confuse-ray', 'psychic'],NULL),
             ('Elite Four 1', 'jynx', 2, 41, FALSE, ARRAY['double-slap', 'lovely-kiss', 'ice-punch', 'psychic'],NULL),
             ('Elite Four 1', 'exeggutor', 3, 41, FALSE, ARRAY['reflect', 'leech-seed', 'egg-bomb', 'psychic'],NULL),
             ('Elite Four 1', 'slowbro', 4, 41, FALSE, ARRAY['curse', 'amnesia', 'body-slam', 'psychic'],NULL),
             ('Elite Four 1', 'xatu', 5, 42, TRUE, ARRAY['quick-attack', 'future-sight', 'confuse-ray', 'psychic'],NULL),

             -- Koga
             ('Elite Four 2', 'ariados', 1, 40, FALSE, ARRAY['double-team', 'spider-web', 'baton-pass', 'giga-drain',NULL], NULL),
             ('Elite Four 2', 'venomoth', 2, 41, FALSE, ARRAY['supersonic', 'gust', 'psychic', 'toxic'],NULL),
             ('Elite Four 2', 'forretress', 3, 43, FALSE, ARRAY['protect', 'swift', 'explosion', 'spikes'],NULL),
             ('Elite Four 2', 'muk', 4, 42, FALSE, ARRAY['minimize', 'acid-armor', 'sludge-bomb', 'toxic'],NULL),
             ('Elite Four 2', 'crobat', 5, 44, TRUE, ARRAY['double-team', 'quick-attack', 'wing-attack', 'toxic'],NULL),

             -- Bruno 
             ('Elite Four 3', 'hitmontop', 1, 42, FALSE, ARRAY['pursuit', 'quick-attack', 'dig', 'detect'],NULL),
             ('Elite Four 3', 'hitmonlee', 2, 42, FALSE, ARRAY['swagger', 'double-kick', 'hi-jump-kick', 'foresight'],NULL),
             ('Elite Four 3', 'hitmonchan', 3, 42, FALSE, ARRAY['thunder-punch', 'fire-punch', 'ice-punch', 'mach-punch'],NULL),
             ('Elite Four 3', 'onix', 4, 43, FALSE, ARRAY['bind', 'earthquake', 'sandstorm', 'rock-slide'],NULL),
             ('Elite Four 3', 'machamp', 5, 46, TRUE, ARRAY['rock-slide', 'foresight', 'vital-throw', 'cross-chop'],NULL),

             -- Karen 
             ('Elite Four 4', 'umbreon', 1, 42, FALSE, ARRAY['sand-attack', 'confuse-ray', 'faint-attack', 'mean-look'],NULL),
             ('Elite Four 4', 'vileplume', 2, 42, FALSE, ARRAY['stun-spore', 'acid', 'moonlight', 'petal-dance'],NULL),
             ('Elite Four 4', 'gengar', 3, 45, FALSE, ARRAY['lick', 'spite', 'curse', 'destiny-bond'],NULL),
             ('Elite Four 4', 'murkrow', 4, 44, FALSE, ARRAY['quick-attack', 'whirlwind', 'pursuit', 'faint-attack'],NULL),
             ('Elite Four 4', 'houndoom', 5, 47, TRUE, ARRAY['roar', 'pursuit', 'flamethrower', 'crunch'],NULL),

             -- Lance 
             ('Champion', 'gyarados', 1, 44, FALSE, ARRAY['flail', 'rain-dance', 'surf', 'hyper-beam'],NULL),
             ('Champion', 'dragonite', 2, 47, FALSE, ARRAY['thunder-wave', 'twister', 'thunder', 'hyper-beam'],NULL),
             ('Champion', 'dragonite', 3, 47, FALSE, ARRAY['thunder-wave', 'twister', 'blizzard', 'hyper-beam'],NULL),
             ('Champion', 'aerodactyl', 4, 46, FALSE, ARRAY['wing-attack', 'ancient-power', 'rock-slide', 'hyper-beam'],NULL),
             ('Champion', 'charizard', 5, 46, FALSE, ARRAY['flamethrower', 'wing-attack', 'slash', 'hyper-beam'],NULL),
             ('Champion', 'dragonite', 6, 50, TRUE, ARRAY['fire-blast', 'safeguard', 'outrage', 'hyper-beam'],NULL),
            
             -- Lt. Surge
            ('Vermilion City - Gym 9', 'raichu', 1, 44, FALSE, ARRAY['thunder-wave', 'quick-attack', 'thunderbolt', 'thunder'],NULL),
            ('Vermilion City - Gym 9', 'electrode', 2, 40, FALSE, ARRAY['screech', 'double-team', 'swift', 'explosion'],NULL),
            ('Vermilion City - Gym 9', 'electrode', 3, 40, FALSE, ARRAY['screech', 'double-team', 'swift', 'explosion'],NULL),
            ('Vermilion City - Gym 9', 'magneton', 4, 40, FALSE, ARRAY['lock-on', 'double-team', 'swift', 'zap-cannon'],NULL),
            ('Vermilion City - Gym 9', 'electabuzz', 5, 45, TRUE, ARRAY['quick-attack', 'thunder-punch', 'light-screen', 'thunder'],NULL),
    
            -- Sabrina
            ('Saffron City - Gym 10', 'espeon', 1, 46, FALSE, ARRAY['sand-attack', 'quick-attack', 'swift', 'psychic'],NULL),
            ('Saffron City - Gym 10', 'mr-mime', 2, 46, FALSE, ARRAY['barrier', 'reflect', 'baton-pass', 'psychic'],NULL),
            ('Saffron City - Gym 10', 'alakazam', 3, 48, TRUE, ARRAY['recover', 'future-sight', 'psychic', 'reflect'],NULL),
    
            -- Erika
            ('Celadon City - Gym 11', 'tangela', 1, 42, FALSE, ARRAY['vine-whip', 'bind', 'giga-drain', 'sleep-powder'],NULL),
            ('Celadon City - Gym 11', 'jumpluff', 2, 41, FALSE, ARRAY['mega-drain', 'leech-seed', 'cotton-spore', 'giga-drain'],NULL),
            ('Celadon City - Gym 11', 'victreebel', 3, 46, FALSE, ARRAY['sunny-day', 'synthesis', 'acid', 'razor-leaf'],NULL),
            ('Celadon City - Gym 11', 'bellossom', 4, 46, TRUE, ARRAY['sunny-day', 'synthesis', 'petal-dance', 'solar-beam'],NULL),
    
            -- Janine
            ('Fuchsia City - Gym 12', 'crobat', 1, 36, FALSE, ARRAY['screech', 'supersonic', 'confuse-ray', 'wing-attack'],NULL),
            ('Fuchsia City - Gym 12', 'weezing', 2, 36, FALSE, ARRAY['smog', 'sludge-bomb', 'toxic', 'explosion'],NULL),
            ('Fuchsia City - Gym 12', 'weezing', 3, 36, FALSE, ARRAY['smog', 'sludge-bomb', 'toxic', 'explosion'],NULL),
            ('Fuchsia City - Gym 12', 'ariados', 4, 33, FALSE, ARRAY['scary-face', 'giga-drain', 'string-shot', 'night-shade'],NULL),
            ('Fuchsia City - Gym 12', 'venomoth', 5, 39, TRUE, ARRAY['foresight', 'double-team', 'gust', 'psychic'],NULL),
    
            -- Misty
            ('Cerulean City - Gym 13', 'golduck', 1, 42, FALSE, ARRAY['surf', 'disable', 'psych-up', 'psychic'],NULL),
            ('Cerulean City - Gym 13', 'quagsire', 2, 42, FALSE, ARRAY['surf', 'amnesia', 'earthquake', 'rain-dance'],NULL),
            ('Cerulean City - Gym 13', 'lapras', 3, 44, FALSE, ARRAY['surf', 'perish-song', 'blizzard', 'rain-dance'],NULL),
            ('Cerulean City - Gym 13', 'starmie', 4, 47, TRUE, ARRAY['surf', 'confuse-ray', 'recover', 'ice-beam'],NULL),
    
            -- Brock
            ('Pewter City - Gym 14', 'graveler', 1, 41, FALSE, ARRAY['defense-curl', 'rock-slide', 'rollout', 'earthquake'], NULL),
            ('Pewter City - Gym 14', 'rhyhorn', 2, 41, FALSE, ARRAY['fury-attack', 'scary-face', 'earthquake', 'horn-drill'], NULL),
            ('Pewter City - Gym 14', 'omastar', 3, 42, FALSE, ARRAY['bite', 'surf', 'protect', 'spike-cannon'], NULL),
            ('Pewter City - Gym 14', 'onix', 4, 44, TRUE, ARRAY['bind', 'rock-slide', 'bide', 'sandstorm'], NULL),
            ('Pewter City - Gym 14', 'kabutops', 5, 42, FALSE, ARRAY['slash', 'surf', 'endure', 'giga-drain'], NULL),
    
            -- Blaine
            ('Seafoam Islands - Gym 15', 'magcargo', 1, 45, FALSE, ARRAY['curse', 'smog', 'flamethrower', 'rock-slide'], NULL),
            ('Seafoam Islands - Gym 15', 'magmar', 2, 45, FALSE, ARRAY['thunder-punch', 'fire-punch', 'sunny-day', 'confuse-ray'], NULL),
            ('Seafoam Islands - Gym 15', 'rapidash', 3, 50, TRUE, ARRAY['quick-attack', 'fire-spin', 'fury-attack', 'fire-blast'], NULL),
    
            -- Blue
            ('Viridian City - Gym 16', 'pidgeot', 1, 56, FALSE, ARRAY['quick-attack', 'whirlwind', 'wing-attack', 'mirror-move'], NULL),
            ('Viridian City - Gym 16', 'alakazam', 2, 54, FALSE, ARRAY['disable', 'recover', 'psychic', 'reflect'], NULL),
            ('Viridian City - Gym 16', 'rhydon', 3, 56, FALSE, ARRAY['fury-attack', 'sandstorm', 'rock-slide', 'earthquake'], NULL),
            ('Viridian City - Gym 16', 'gyarados', 4, 58, FALSE, ARRAY['twister', 'hydro-pump', 'rain-dance', 'hyper-beam'], NULL),
            ('Viridian City - Gym 16', 'exeggutor', 5, 58, FALSE, ARRAY['sunny-day', 'leech-seed', 'egg-bomb', 'solar-beam'], NULL),
            ('Viridian City - Gym 16', 'arcanine', 6, 58, TRUE, ARRAY['roar', 'swift', 'flamethrower', 'extreme-speed'], NULL),
         
            -- Red
            ('Mt. Silver - Final Boss', 'pikachu', 1, 81, TRUE, ARRAY['charm', 'quick-attack', 'thunderbolt', 'thunder'], NULL),
            ('Mt. Silver - Final Boss', 'espeon', 2, 73, FALSE, ARRAY['mud-slap', 'reflect', 'swift', 'psychic'], NULL),
            ('Mt. Silver - Final Boss', 'snorlax', 3, 75, FALSE, ARRAY['amnesia', 'snore', 'rest', 'body-slam'], NULL),
            ('Mt. Silver - Final Boss', 'venusaur', 4, 77, FALSE, ARRAY['sunny-day', 'giga-drain', 'synthesis', 'solar-beam'], NULL),
            ('Mt. Silver - Final Boss', 'charizard', 5, 77, FALSE, ARRAY['flamethrower', 'wing-attack', 'slash', 'fire-spin'], NULL),
            ('Mt. Silver - Final Boss', 'blastoise', 6, 77, FALSE, ARRAY['rain-dance', 'surf', 'blizzard', 'whirlpool'], NULL)
     
         ) AS t(stage_search, p_name, slot, lvl, ace, moves_arr,condition)
         JOIN pokemon p ON p.name = t.p_name
         JOIN milestones m ON m.stage_name = t.stage_search
         JOIN games g ON m.game_id = g.id
WHERE g.name IN ('gold', 'silver', NULL);

INSERT INTO milestone_teams (milestone_id, pokemon_id, slot_number, level, is_ace, moves, condition)
SELECT m.id, p.id, t.slot, t.lvl, t.ace, t.moves_arr, t.condition
FROM (
         VALUES
             -- Falkner
             ('Violet City - Gym 1', 'pidgey', 1, 7, FALSE, ARRAY['tackle', 'mud-slap'], NULL),
             ('Violet City - Gym 1', 'pidgeotto', 2, 9, TRUE, ARRAY['tackle', 'mud-slap', 'gust'], NULL),

             -- Bugsy
             ('Azalea Town - Gym 2', 'metapod', 1, 14, FALSE, ARRAY['tackle', 'string-shot', 'harden'], NULL),
             ('Azalea Town - Gym 2', 'kakuna', 2, 14, FALSE, ARRAY['poison-sting', 'string-shot', 'harden'], NULL),
             ('Azalea Town - Gym 2', 'scyther', 3, 16, TRUE, ARRAY['quick-attack', 'leer', 'fury-cutter'], NULL),

             -- Whitney
             ('Goldenrod City - Gym 3', 'clefairy', 1, 18, FALSE, ARRAY['double-slap', 'mimic', 'encore', 'metronome'], NULL),
             ('Goldenrod City - Gym 3', 'miltank', 2, 20, TRUE, ARRAY['rollout', 'attract', 'stomp', 'milk-drink'], NULL),

             -- Morty
             ('Ecruteak City - Gym 4', 'gastly', 1, 21, FALSE, ARRAY['lick', 'spite', 'mean-look', 'curse'], NULL),
             ('Ecruteak City - Gym 4', 'haunter', 2, 21, FALSE, ARRAY['hypnosis', 'mimic', 'curse', 'night-shade'], NULL),
             ('Ecruteak City - Gym 4', 'haunter', 3, 23, FALSE, ARRAY['spite', 'mean-look', 'mimic', 'night-shade'], NULL),
             ('Ecruteak City - Gym 4', 'gengar', 4, 25, TRUE, ARRAY['hypnosis', 'shadow-ball', 'mean-look', 'dream-eater'], NULL),

             -- Chuck
             ('Cianwood City - Gym 5', 'primeape', 1, 27, FALSE, ARRAY['leer', 'rage', 'karate-chop', 'fury-swipes'], NULL),
             ('Cianwood City - Gym 5', 'poliwrath', 2, 30, TRUE, ARRAY['hypnosis', 'mind-reader', 'surf', 'dynamic-punch'], NULL),

             -- Jasmine
             ('Olivine City - Gym 6', 'magnemite', 1, 30, FALSE, ARRAY['thunderbolt', 'supersonic', 'sonic-boom', 'thunder-wave'], NULL),
             ('Olivine City - Gym 6', 'magnemite', 2, 30, FALSE, ARRAY['thunderbolt', 'supersonic', 'sonic-boom', 'thunder-wave'], NULL),
             ('Olivine City - Gym 6', 'steelix', 3, 35, TRUE, ARRAY['screech', 'sunny-day', 'rock-throw', 'iron-tail'], NULL),

             -- Pryce
             ('Mahogany Town - Gym 7', 'seel', 1, 27, FALSE, ARRAY['headbutt', 'icy-wind', 'aurora-beam', 'rest'], NULL),
             ('Mahogany Town - Gym 7', 'dewgong', 2, 29, FALSE, ARRAY['headbutt', 'icy-wind', 'aurora-beam', 'rest'], NULL),
             ('Mahogany Town - Gym 7', 'piloswine', 3, 31, TRUE, ARRAY['icy-wind', 'fury-attack', 'mist', 'blizzard'], NULL),

             -- Clair
             ('Blackthorn City - Gym 8', 'dragonair', 1, 37, FALSE, ARRAY['thunder-wave', 'surf', 'slam', 'dragon-breath'], NULL),
             ('Blackthorn City - Gym 8', 'dragonair', 2, 37, FALSE, ARRAY['thunder-wave', 'thunderbolt', 'slam', 'dragon-breath'], NULL),
             ('Blackthorn City - Gym 8', 'dragonair', 3, 37, FALSE, ARRAY['thunder-wave', 'ice-beam', 'slam', 'dragon-breath'], NULL),
             ('Blackthorn City - Gym 8', 'kingdra', 4, 40, TRUE, ARRAY['smokescreen', 'surf', 'hyper-beam', 'dragon-breath'], NULL),
             ('Elite Four 1', 'xatu', 1, 40, FALSE, ARRAY['quick-attack', 'future-sight', 'confuse-ray', 'psychic'], NULL),
             ('Elite Four 1', 'jynx', 2, 41, FALSE, ARRAY['double-slap', 'lovely-kiss', 'ice-punch', 'psychic'], NULL),
             ('Elite Four 1', 'exeggutor', 3, 41, FALSE, ARRAY['reflect', 'leech-seed', 'egg-bomb', 'psychic'], NULL),
             ('Elite Four 1', 'slowbro', 4, 41, FALSE, ARRAY['curse', 'amnesia', 'body-slam', 'psychic'], NULL),
             ('Elite Four 1', 'xatu', 5, 42, TRUE, ARRAY['quick-attack', 'future-sight', 'confuse-ray', 'psychic'], NULL),

             -- Koga
             ('Elite Four 2', 'ariados', 1, 40, FALSE, ARRAY['double-team', 'spider-web', 'baton-pass', 'giga-drain'], NULL),
             ('Elite Four 2', 'venomoth', 2, 41, FALSE, ARRAY['supersonic', 'gust', 'psychic', 'toxic'], NULL),
             ('Elite Four 2', 'forretress', 3, 43, FALSE, ARRAY['protect', 'swift', 'explosion', 'spikes'], NULL),
             ('Elite Four 2', 'muk', 4, 42, FALSE, ARRAY['minimize', 'acid-armor', 'sludge-bomb', 'toxic'], NULL),
             ('Elite Four 2', 'crobat', 5, 44, TRUE, ARRAY['double-team', 'quick-attack', 'wing-attack', 'toxic'], NULL),

             -- Bruno 
             ('Elite Four 3', 'hitmontop', 1, 42, FALSE, ARRAY['pursuit', 'quick-attack', 'dig', 'detect'], NULL),
             ('Elite Four 3', 'hitmonlee', 2, 42, FALSE, ARRAY['swagger', 'double-kick', 'hi-jump-kick', 'foresight'], NULL),
             ('Elite Four 3', 'hitmonchan', 3, 42, FALSE, ARRAY['thunder-punch', 'fire-punch', 'ice-punch', 'mach-punch'], NULL),
             ('Elite Four 3', 'onix', 4, 43, FALSE, ARRAY['bind', 'earthquake', 'sandstorm', 'rock-slide'], NULL),
             ('Elite Four 3', 'machamp', 5, 46, TRUE, ARRAY['rock-slide', 'foresight', 'vital-throw', 'cross-chop'], NULL),

             -- Karen 
             ('Elite Four 4', 'umbreon', 1, 42, FALSE, ARRAY['sand-attack', 'confuse-ray', 'faint-attack', 'mean-look'], NULL),
             ('Elite Four 4', 'vileplume', 2, 42, FALSE, ARRAY['stun-spore', 'acid', 'moonlight', 'petal-dance'], NULL),
             ('Elite Four 4', 'gengar', 3, 45, FALSE, ARRAY['lick', 'spite', 'curse', 'destiny-bond'], NULL),
             ('Elite Four 4', 'murkrow', 4, 44, FALSE, ARRAY['quick-attack', 'whirlwind', 'pursuit', 'faint-attack'], NULL),
             ('Elite Four 4', 'houndoom', 5, 47, TRUE, ARRAY['roar', 'pursuit', 'flamethrower', 'crunch'], NULL),

             -- Lance 
             ('Champion', 'gyarados', 1, 44, FALSE, ARRAY['flail', 'rain-dance', 'surf', 'hyper-beam'], NULL),
             ('Champion', 'dragonite', 2, 47, FALSE, ARRAY['thunder-wave', 'twister', 'thunder', 'hyper-beam'], NULL),
             ('Champion', 'dragonite', 3, 47, FALSE, ARRAY['thunder-wave', 'twister', 'blizzard', 'hyper-beam'], NULL),
             ('Champion', 'aerodactyl', 4, 46, FALSE, ARRAY['wing-attack', 'ancient-power', 'rock-slide', 'hyper-beam'], NULL),
             ('Champion', 'charizard', 5, 46, FALSE, ARRAY['flamethrower', 'wing-attack', 'slash', 'hyper-beam'], NULL),
             ('Champion', 'dragonite', 6, 50, TRUE, ARRAY['fire-blast', 'safeguard', 'outrage', 'hyper-beam'], NULL),

             -- Lt. Surge
             ('Vermilion City - Gym 9', 'raichu', 1, 44, FALSE, ARRAY['thunder-wave', 'quick-attack', 'thunderbolt', 'thunder'], NULL),
             ('Vermilion City - Gym 9', 'electrode', 2, 40, FALSE, ARRAY['screech', 'double-team', 'swift', 'explosion'], NULL),
             ('Vermilion City - Gym 9', 'electrode', 3, 40, FALSE, ARRAY['screech', 'double-team', 'swift', 'explosion'], NULL),
             ('Vermilion City - Gym 9', 'magneton', 4, 40, FALSE, ARRAY['lock-on', 'double-team', 'swift', 'zap-cannon'], NULL),
             ('Vermilion City - Gym 9', 'electabuzz', 5, 45, TRUE, ARRAY['quick-attack', 'thunder-punch', 'light-screen', 'thunder'], NULL),

             -- Sabrina
             ('Saffron City - Gym 10', 'espeon', 1, 46, FALSE, ARRAY['sand-attack', 'quick-attack', 'swift', 'psychic'], NULL),
             ('Saffron City - Gym 10', 'mr-mime', 2, 46, FALSE, ARRAY['barrier', 'reflect', 'baton-pass', 'psychic'], NULL),
             ('Saffron City - Gym 10', 'alakazam', 3, 48, TRUE, ARRAY['recover', 'future-sight', 'psychic', 'reflect'], NULL),

             -- Erika
             ('Celadon City - Gym 11', 'tangela', 1, 42, FALSE, ARRAY['vine-whip', 'bind', 'giga-drain', 'sleep-powder'], NULL),
             ('Celadon City - Gym 11', 'jumpluff', 2, 41, FALSE, ARRAY['mega-drain', 'leech-seed', 'cotton-spore', 'giga-drain'], NULL),
             ('Celadon City - Gym 11', 'victreebel', 3, 46, FALSE, ARRAY['sunny-day', 'synthesis', 'acid', 'razor-leaf'], NULL),
             ('Celadon City - Gym 11', 'bellossom', 4, 46, TRUE, ARRAY['sunny-day', 'synthesis', 'petal-dance', 'solar-beam'], NULL),

             -- Janine
             ('Fuchsia City - Gym 12', 'crobat', 1, 36, FALSE, ARRAY['screech', 'supersonic', 'confuse-ray', 'wing-attack'], NULL),
             ('Fuchsia City - Gym 12', 'weezing', 2, 36, FALSE, ARRAY['smog', 'sludge-bomb', 'toxic', 'explosion'], NULL),
             ('Fuchsia City - Gym 12', 'weezing', 3, 36, FALSE, ARRAY['smog', 'sludge-bomb', 'toxic', 'explosion'], NULL),
             ('Fuchsia City - Gym 12', 'ariados', 4, 33, FALSE, ARRAY['scary-face', 'giga-drain', 'string-shot', 'night-shade'], NULL),
             ('Fuchsia City - Gym 12', 'venomoth', 5, 39, TRUE, ARRAY['foresight', 'double-team', 'gust', 'psychic'], NULL),

             -- Misty
             ('Cerulean City - Gym 13', 'golduck', 1, 42, FALSE, ARRAY['surf', 'disable', 'psych-up', 'psychic'], NULL),
             ('Cerulean City - Gym 13', 'quagsire', 2, 42, FALSE, ARRAY['surf', 'amnesia', 'earthquake', 'rain-dance'], NULL),
             ('Cerulean City - Gym 13', 'lapras', 3, 44, FALSE, ARRAY['surf', 'perish-song', 'blizzard', 'rain-dance'], NULL),
             ('Cerulean City - Gym 13', 'starmie', 4, 47, TRUE, ARRAY['surf', 'confuse-ray', 'recover', 'ice-beam'], NULL),

             -- Brock
             ('Pewter City - Gym 14', 'graveler', 1, 41, FALSE, ARRAY['defense-curl', 'rock-slide', 'rollout', 'earthquake'], NULL),
             ('Pewter City - Gym 14', 'rhyhorn', 2, 41, FALSE, ARRAY['fury-attack', 'scary-face', 'earthquake', 'horn-drill'], NULL),
             ('Pewter City - Gym 14', 'omastar', 3, 42, FALSE, ARRAY['bite', 'surf', 'protect', 'spike-cannon'], NULL),
             ('Pewter City - Gym 14', 'onix', 4, 44, TRUE, ARRAY['bind', 'rock-slide', 'bide', 'sandstorm'], NULL),
             ('Pewter City - Gym 14', 'kabutops', 5, 42, FALSE, ARRAY['slash', 'surf', 'endure', 'giga-drain'], NULL),

             -- Blaine
             ('Seafoam Islands - Gym 15', 'magcargo', 1, 45, FALSE, ARRAY['curse', 'smog', 'flamethrower', 'rock-slide'], NULL),
             ('Seafoam Islands - Gym 15', 'magmar', 2, 45, FALSE, ARRAY['thunder-punch', 'fire-punch', 'sunny-day', 'confuse-ray'], NULL),
             ('Seafoam Islands - Gym 15', 'rapidash', 3, 50, TRUE, ARRAY['quick-attack', 'fire-spin', 'fury-attack', 'fire-blast'], NULL),

             -- Blue
             ('Viridian City - Gym 16', 'pidgeot', 1, 56, FALSE, ARRAY['quick-attack', 'whirlwind', 'wing-attack', 'mirror-move'], NULL),
             ('Viridian City - Gym 16', 'alakazam', 2, 54, FALSE, ARRAY['disable', 'recover', 'psychic', 'reflect'], NULL),
             ('Viridian City - Gym 16', 'rhydon', 3, 56, FALSE, ARRAY['fury-attack', 'sandstorm', 'rock-slide', 'earthquake'], NULL),
             ('Viridian City - Gym 16', 'gyarados', 4, 58, FALSE, ARRAY['twister', 'hydro-pump', 'rain-dance', 'hyper-beam'], NULL),
             ('Viridian City - Gym 16', 'exeggutor', 5, 58, FALSE, ARRAY['sunny-day', 'leech-seed', 'egg-bomb', 'solar-beam'], NULL),
             ('Viridian City - Gym 16', 'arcanine', 6, 58, TRUE, ARRAY['roar', 'swift', 'flamethrower', 'extreme-speed'], NULL),

             -- Red
             ('Mt. Silver - Final Boss', 'pikachu', 1, 81, TRUE, ARRAY['charm', 'quick-attack', 'thunderbolt', 'thunder'], NULL),
             ('Mt. Silver - Final Boss', 'espeon', 2, 73, FALSE, ARRAY['mud-slap', 'reflect', 'swift', 'psychic'], NULL),
             ('Mt. Silver - Final Boss', 'snorlax', 3, 75, FALSE, ARRAY['amnesia', 'snore', 'rest', 'body-slam'], NULL),
             ('Mt. Silver - Final Boss', 'venusaur', 4, 77, FALSE, ARRAY['sunny-day', 'giga-drain', 'synthesis', 'solar-beam'], NULL),
             ('Mt. Silver - Final Boss', 'charizard', 5, 77, FALSE, ARRAY['flamethrower', 'wing-attack', 'slash', 'fire-spin'], NULL),
             ('Mt. Silver - Final Boss', 'blastoise', 6, 77, FALSE, ARRAY['rain-dance', 'surf', 'blizzard', 'whirlpool'], NULL)

     ) AS t(stage_search, p_name, slot, lvl, ace, moves_arr,condition)
         JOIN pokemon p ON p.name = t.p_name
         JOIN milestones m ON m.stage_name = t.stage_search
         JOIN games g ON m.game_id = g.id
WHERE g.name IN ('crystal', NULL);

INSERT INTO milestone_teams (milestone_id, pokemon_id, slot_number, level, is_ace, moves, ability, condition)
SELECT m.id, p.id, t.slot, t.lvl, t.ace, t.moves_arr, t.ability,condition
FROM (
         VALUES
             -- ROXANNE
             ('Rustboro City - Gym 1', 'geodude', 1, 14, FALSE, ARRAY['tackle', 'defense-curl', 'rock-throw', 'rock-tomb'], 'sturdy', NULL),
             ('Rustboro City - Gym 1', 'nosepass', 2, 15, TRUE, ARRAY['tackle', 'harden', 'rock-throw', 'rock-tomb'],'sturdy', NULL),

             -- BRAWLY
             ('Dewford Town - Gym 2', 'machop', 1, 17, FALSE, ARRAY['bulk-up', 'leer', 'karate-chop', 'seismic-toss'],'guts', NULL),
             ('Dewford Town - Gym 2', 'makuhita', 2, 18, TRUE, ARRAY['bulk-up', 'knock-off', 'arm-thrust', 'sand-attack'],'guts', NULL),

             -- WATTSON
             ('Mauville City - Gym 3', 'magnemite', 1, 22, FALSE, ARRAY['thundershock', 'supersonic', 'sonic-boom', 'thunder-wave'],'magnet-pull', NULL),
             ('Mauville City - Gym 3', 'voltorb', 2, 20, FALSE, ARRAY['rollout', 'spark', 'sonic-boom', 'self-destruct'],'soundproof', NULL),
             ('Mauville City - Gym 3', 'magneton', 3, 23, TRUE, ARRAY['shock-wave', 'supersonic', 'sonic-boom', 'thunder-wave'],'magnet-pull', NULL),

             -- FLANNERY
             ('Lavaridge Town - Gym 4', 'slugma', 1, 26, FALSE, ARRAY['overheat', 'smog', 'light-screen', 'sunny-day'],'magma-armor', NULL),
             ('Lavaridge Town - Gym 4', 'slugma', 2, 26, FALSE, ARRAY['flamethrower', 'rock-slide', 'light-screen', 'sunny-day'],'magma-armor', NULL),
             ('Lavaridge Town - Gym 4', 'torkoal', 3, 28, TRUE, ARRAY['overheat', 'body-slam', 'flail', 'attract'],'white-smoke', NULL),

             -- NORMAN
             ('Petalburg City - Gym 5', 'slaking', 1, 28, FALSE, ARRAY['encore', 'facade', 'yawn', 'faint-attack'],'truant', NULL),
             ('Petalburg City - Gym 5', 'vigoroth', 2, 30, FALSE, ARRAY['slash', 'faint-attack', 'facade', 'encore'], 'vital-spirit', NULL),
             ('Petalburg City - Gym 5', 'slaking', 3, 31, TRUE, ARRAY['focus-punch', 'slack-off', 'facade', 'faint-attack'],'truant', NULL),

             -- WINONA
             ('Fortree City - Gym 6', 'swellow', 1, 31, FALSE, ARRAY['quick-attack', 'aerial-ace', 'double-team', 'endeavor'],'guts', NULL),
             ('Fortree City - Gym 6', 'pelipper', 2, 30, FALSE, ARRAY['water-gun', 'supersonic', 'protect', 'aerial-ace'],'keen-eye', NULL),
             ('Fortree City - Gym 6', 'skarmory', 3, 32, FALSE, ARRAY['sand-attack', 'fury-attack', 'steel-wing', 'aerial-ace'],'keen-eye', NULL),
             ('Fortree City - Gym 6', 'altaria', 4, 33, TRUE, ARRAY['earthquake', 'dragon-breath', 'dragon-dance', 'aerial-ace'],'natural-cure', NULL),

             -- TATE AND LIZA
             ('Mossdeep City - Gym 7', 'lunatone', 1, 42, TRUE, ARRAY['light-screen', 'psychic', 'hypnosis', 'calm-mind'],'levitate', NULL),
             ('Mossdeep City - Gym 7', 'solrock', 2, 42, TRUE, ARRAY['sunny-day', 'solar-beam', 'psychic', 'flamethrower'],'levitate', NULL),

             -- WALLACE
             ('Sootopolis City - Gym 8', 'luvdisc', 1, 40, FALSE, ARRAY['flail', 'attract', 'sweet-kiss', 'water-pulse'],'swift-swim', NULL),
             ('Sootopolis City - Gym 8', 'sealeo', 2, 40, FALSE, ARRAY['encore', 'body-slam', 'aurora-beam', 'water-pulse'],'thick-fat', NULL),
             ('Sootopolis City - Gym 8', 'seaking', 3, 42, FALSE, ARRAY['horn-drill', 'fury-attack', 'rain-dance', 'water-pulse'],'swift-swim', NULL),
             ('Sootopolis City - Gym 8', 'whiscash', 4, 42, FALSE, ARRAY['amnesia', 'rain-dance', 'earthquake', 'water-pulse'],'oblivious', NULL),
             ('Sootopolis City - Gym 8', 'milotic', 5, 43, TRUE, ARRAY['recover', 'twister', 'ice-beam', 'water-pulse'],'marvel-scale', NULL),

             -- SIDNEY
             ('Elite Four 1', 'mightyena', 1, 46, FALSE, ARRAY['crunch', 'take-down', 'sand-attack', 'roar'], 'intimidate', NULL),
             ('Elite Four 1', 'shiftry', 2, 48, FALSE, ARRAY['fake-out', 'double-team', 'swagger', 'extrasensory'], 'chlorophyll', NULL),
             ('Elite Four 1', 'cacturne', 3, 46, FALSE, ARRAY['needle-arm', 'leech-seed', 'faint-attack', 'cotton-spore'], 'sand-veil', NULL),
             ('Elite Four 1', 'sharpedo', 4, 48, FALSE, ARRAY['crunch', 'surf', 'slash', 'swagger'], 'rough-skin', NULL),
             ('Elite Four 1', 'absol', 5, 49, TRUE, ARRAY['aerial-ace', 'snatch', 'swords-dance', 'slash'], 'pressure', NULL),

             -- PHOEBE
             ('Elite Four 2', 'dusclops', 1, 48, FALSE, ARRAY['shadow-punch', 'confuse-ray', 'curse', 'future-sight'], 'pressure', NULL),
             ('Elite Four 2', 'banette', 2, 49, FALSE, ARRAY['shadow-ball', 'spite', 'will-o-wisp', 'faint-attack'], 'insomnia', NULL),
             ('Elite Four 2', 'sableye', 3, 50, FALSE, ARRAY['shadow-ball', 'psychic', 'faint-attack', 'attract'], 'keen-eye', NULL),
             ('Elite Four 2', 'banette', 4, 49, FALSE, ARRAY['psychic', 'shadow-ball', 'toxic', 'skill-swap'], 'insomnia', NULL),
             ('Elite Four 2', 'dusclops', 5, 51, TRUE, ARRAY['shadow-ball', 'ice-beam', 'earthquake', 'confuse-ray'], 'pressure', NULL),

             -- GLACIA
             ('Elite Four 3', 'glalie', 1, 50, FALSE, ARRAY['crunch', 'hail', 'ice-beam', 'light-screen'], 'inner-focus', NULL),
             ('Elite Four 3', 'sealeo', 2, 50, FALSE, ARRAY['surf', 'ice-ball', 'body-slam', 'hail'], 'thick-fat', NULL),
             ('Elite Four 3', 'sealeo', 3, 52, FALSE, ARRAY['blizzard', 'dive', 'attract', 'hail'], 'thick-fat', NULL),
             ('Elite Four 3', 'glalie', 4, 52, FALSE, ARRAY['crunch', 'ice-beam', 'shadow-ball', 'hail'], 'inner-focus', NULL),
             ('Elite Four 3', 'walrein', 5, 53, TRUE, ARRAY['surf', 'blizzard', 'body-slam', 'sheer-cold'], 'thick-fat', NULL),

             -- DRAKE
             ('Elite Four 4', 'shelgon', 1, 52, FALSE, ARRAY['dragon-claw', 'crunch', 'rock-tomb', 'protect'], 'rock-head', NULL),
             ('Elite Four 4', 'altaria', 2, 54, FALSE, ARRAY['take-down', 'dragon-breath', 'refresh', 'dragon-dance'], 'natural-cure', NULL),
             ('Elite Four 4', 'flygon', 3, 53, FALSE, ARRAY['dragon-breath', 'dig', 'fly', 'sandstorm'], 'levitate', NULL),
             ('Elite Four 4', 'flygon', 4, 53, FALSE, ARRAY['dragon-breath', 'flamethrower', 'crunch', 'sand-attack'], 'levitate', NULL),
             ('Elite Four 4', 'salamence', 5, 55, TRUE, ARRAY['dragon-claw', 'flamethrower', 'crunch', 'fly'], 'intimidate', NULL),

             -- STEVEN
             ('Champion', 'skarmory', 1, 57, FALSE, ARRAY['aerial-ace', 'steel-wing', 'spikes', 'toxic'], 'keen-eye', NULL),
             ('Champion', 'aggron', 2, 56, FALSE, ARRAY['thunder', 'earthquake', 'dragon-claw', 'solar-beam'], 'sturdy', NULL),
             ('Champion', 'claydol', 3, 55, FALSE, ARRAY['earthquake', 'ancient-power', 'reflect', 'light-screen'], 'levitate', NULL),
             ('Champion', 'cradily', 4, 56, FALSE, ARRAY['giga-drain', 'ancient-power', 'sludge-bomb', 'confuse-ray'], 'suction-cups', NULL),
             ('Champion', 'armaldo', 5, 56, FALSE, ARRAY['ancient-power', 'aerial-ace', 'water-pulse', 'slash'], 'battle-armor', NULL),
             ('Champion', 'metagross', 6, 58, TRUE, ARRAY['earthquake', 'psychic', 'meteor-mash', 'hyper-beam'], 'clear-body', NULL)

     ) AS t(stage_search, p_name, slot, lvl, ace, moves_arr, ability,condition)
         JOIN pokemon p ON p.name = t.p_name
         JOIN milestones m ON m.stage_name = t.stage_search
         JOIN games g ON m.game_id = g.id
WHERE g.name IN ('ruby', 'sapphire', NULL);

INSERT INTO milestone_teams (milestone_id, pokemon_id, slot_number, level, is_ace, moves, ability, condition)
SELECT m.id, p.id, t.slot, t.lvl, t.ace, t.moves_arr, t.ability, t.condition
FROM (
         VALUES
             -- ROXANNE
             ('Rustboro City - Gym 1', 'geodude', 1, 12, FALSE, ARRAY['tackle', 'defense-curl', 'rock-throw', 'rock-tomb'], 'rock-head', NULL),
             ('Rustboro City - Gym 1', 'geodude', 2, 12, FALSE, ARRAY['tackle', 'defense-curl', 'rock-throw', 'rock-tomb'], 'rock-head', NULL),
             ('Rustboro City - Gym 1', 'nosepass', 3, 15, TRUE, ARRAY['block', 'harden', 'tackle', 'rock-tomb'], 'sturdy', NULL),

             -- BRAWLY
             ('Dewford Town - Gym 2', 'machop', 1, 16, FALSE, ARRAY['karate-chop', 'low-kick', 'seismic-toss', 'bulk-up'], 'guts', NULL),
             ('Dewford Town - Gym 2', 'meditite', 2, 16, FALSE, ARRAY['focus-punch', 'light-screen', 'reflect', 'bulk-up'], 'pure-power', NULL),
             ('Dewford Town - Gym 2', 'makuhita', 3, 19, TRUE, ARRAY['arm-thrust', 'vital-throw', 'reversal', 'bulk-up'], 'thick-fat', NULL),

             -- WATTSON
             ('Mauville City - Gym 3', 'voltorb', 1, 20, FALSE, ARRAY['rollout', 'spark', 'self-destruct', 'shock-wave'], 'soundproof', NULL),
             ('Mauville City - Gym 3', 'electrike', 2, 20, FALSE, ARRAY['shock-wave', 'leer', 'quick-attack', 'howl'], 'static', NULL),
             ('Mauville City - Gym 3', 'magneton', 3, 22, FALSE, ARRAY['supersonic', 'shock-wave', 'thunder-wave', 'sonic-boom'], 'magnet-pull', NULL),
             ('Mauville City - Gym 3', 'manectric', 4, 24, TRUE, ARRAY['quick-attack', 'thunder-wave', 'shock-wave', 'howl'], 'static', NULL),

             -- FLANNERY
             ('Lavaridge Town - Gym 4', 'numel', 1, 24, FALSE, ARRAY['overheat', 'take-down', 'magnitude', 'sunny-day'], 'oblivious', NULL),
             ('Lavaridge Town - Gym 4', 'slugma', 2, 24, FALSE, ARRAY['overheat', 'smog', 'light-screen', 'sunny-day'], 'magma-armor', NULL),
             ('Lavaridge Town - Gym 4', 'camerupt', 3, 26, FALSE, ARRAY['overheat', 'tackle', 'sunny-day', 'attract'], 'magma-armor', NULL),
             ('Lavaridge Town - Gym 4', 'torkoal', 4, 29, TRUE, ARRAY['overheat', 'sunny-day', 'body-slam', 'attract'], 'white-smoke', NULL),

             -- NORMAN
             ('Petalburg City - Gym 5', 'spinda', 1, 27, FALSE, ARRAY['teeter-dance', 'psybeam', 'facade', 'encore'], 'own-tempo', NULL),
             ('Petalburg City - Gym 5', 'vigoroth', 2, 27, FALSE, ARRAY['slash', 'facade', 'encore', 'feint-attack'], 'vital-spirit', NULL),
             ('Petalburg City - Gym 5', 'linoone', 3, 29, FALSE, ARRAY['slash', 'belly-drum', 'facade', 'headbutt'], 'pickup', NULL),
             ('Petalburg City - Gym 5', 'slaking', 4, 31, TRUE, ARRAY['counter', 'yawn', 'facade', 'feint-attack'], 'truant', NULL),

             -- WINONA
             ('Fortree City - Gym 6', 'swablu', 1, 29, FALSE, ARRAY['perish-song', 'mirror-move', 'safeguard', 'aerial-ace'], 'natural-cure', NULL),
             ('Fortree City - Gym 6', 'tropius', 2, 29, FALSE, ARRAY['sunny-day', 'aerial-ace', 'solar-beam', 'synthesis'], 'chlorophyll', NULL),
             ('Fortree City - Gym 6', 'pelipper', 3, 30, FALSE, ARRAY['water-gun', 'supersonic', 'protect', 'aerial-ace'], 'keen-eye', NULL),
             ('Fortree City - Gym 6', 'skarmory', 4, 31, FALSE, ARRAY['sand-attack', 'fury-attack', 'steel-wing', 'aerial-ace'], 'keen-eye', NULL),
             ('Fortree City - Gym 6', 'altaria', 5, 33, TRUE, ARRAY['earthquake', 'dragon-breath', 'dragon-dance', 'aerial-ace'], 'natural-cure', NULL),

             -- TATE AND LIZA (Double Battle)
             ('Mossdeep City - Gym 7', 'claydol', 1, 41, FALSE, ARRAY['earthquake', 'ancient-power', 'psychic', 'light-screen'], 'levitate', NULL),
             ('Mossdeep City - Gym 7', 'xatu', 2, 41, FALSE, ARRAY['psychic', 'sunny-day', 'confuse-ray', 'calm-mind'], 'synchronize', NULL),
             ('Mossdeep City - Gym 7', 'lunatone', 3, 42, TRUE, ARRAY['light-screen', 'psychic', 'hypnosis', 'calm-mind'], 'levitate', NULL),
             ('Mossdeep City - Gym 7', 'solrock', 4, 42, TRUE, ARRAY['sunny-day', 'solar-beam', 'psychic', 'flamethrower'], 'levitate', NULL),

             -- JUAN
             ('Sootopolis City - Gym 8', 'luvdisc', 1, 41, FALSE, ARRAY['water-pulse', 'attract', 'sweet-kiss', 'flail'], 'swift-swim', NULL),
             ('Sootopolis City - Gym 8', 'whiscash', 2, 41, FALSE, ARRAY['rain-dance', 'water-pulse', 'amnesia', 'earthquake'], 'oblivious', NULL),
             ('Sootopolis City - Gym 8', 'sealeo', 3, 43, FALSE, ARRAY['encore', 'body-slam', 'aurora-beam', 'water-pulse'], 'thick-fat', NULL),
             ('Sootopolis City - Gym 8', 'crawdaunt', 4, 43, FALSE, ARRAY['water-pulse', 'crabhammer', 'taunt', 'leer'], 'hyper-cutter', NULL),
             ('Sootopolis City - Gym 8', 'kingdra', 5, 46, TRUE, ARRAY['water-pulse', 'double-team', 'ice-beam', 'rest'], 'swift-swim', NULL),
             
             -- SIDNEY
             ('Elite Four 1', 'mightyena', 1, 46, FALSE, ARRAY['roar', 'double-edge', 'sand-attack', 'crunch'], 'intimidate', NULL),
             ('Elite Four 1', 'shiftry', 2, 48, FALSE, ARRAY['torment', 'double-team', 'swagger', 'extrasensory'], 'chlorophyll', NULL),
             ('Elite Four 1', 'cacturne', 3, 46, FALSE, ARRAY['leech-seed', 'faint-attack', 'needle-arm', 'cotton-spore'], 'sand-veil', NULL),
             ('Elite Four 1', 'crawdaunt', 4, 48, FALSE, ARRAY['surf', 'swords-dance', 'strength', 'facade'], 'hyper-cutter', NULL),
             ('Elite Four 1', 'absol', 5, 49, TRUE, ARRAY['aerial-ace', 'rock-slide', 'swords-dance', 'slash'], 'pressure', NULL),
    
            -- PHOEBE
            ('Elite Four 2', 'dusclops', 1, 48, FALSE, ARRAY['shadow-punch', 'confuse-ray', 'curse', 'protect'], 'pressure', NULL),
            ('Elite Four 2', 'banette', 2, 49, FALSE, ARRAY['shadow-ball', 'grudge', 'will-o-wisp', 'faint-attack'], 'insomnia', NULL),
            ('Elite Four 2', 'sableye', 3, 50, FALSE, ARRAY['shadow-ball', 'double-team', 'night-shade', 'faint-attack'], 'keen-eye', NULL),
            ('Elite Four 2', 'banette', 4, 49, FALSE, ARRAY['shadow-ball', 'psychic', 'thunderbolt', 'facade'], 'insomnia', NULL),
            ('Elite Four 2', 'dusclops', 5, 51, TRUE, ARRAY['shadow-ball', 'ice-beam', 'rock-slide', 'earthquake'], 'pressure', NULL),
    
            -- GLACIA
            ('Elite Four 3', 'sealeo', 1, 50, FALSE, ARRAY['encore', 'body-slam', 'hail', 'ice-ball'], 'thick-fat', NULL),
            ('Elite Four 3', 'glalie', 2, 50, FALSE, ARRAY['light-screen', 'crunch', 'icy-wind', 'ice-beam'], 'inner-focus', NULL),
            ('Elite Four 3', 'sealeo', 3, 52, FALSE, ARRAY['attract', 'double-edge', 'hail', 'blizzard'], 'thick-fat', NULL),
            ('Elite Four 3', 'glalie', 4, 52, FALSE, ARRAY['shadow-ball', 'explosion', 'hail', 'ice-beam'], 'inner-focus', NULL),
            ('Elite Four 3', 'walrein', 5, 53, TRUE, ARRAY['surf', 'body-slam', 'ice-beam', 'sheer-cold'], 'thick-fat', NULL),
    
            -- DRAKE
            ('Elite Four 4', 'shelgon', 1, 52, FALSE, ARRAY['rock-tomb', 'dragon-claw', 'protect', 'double-edge'], 'rock-head', NULL),
            ('Elite Four 4', 'altaria', 2, 54, FALSE, ARRAY['double-edge', 'dragon-breath', 'dragon-dance', 'aerial-ace'], 'natural-cure', NULL),
            ('Elite Four 4', 'kingdra', 3, 53, FALSE, ARRAY['smokescreen', 'dragon-dance', 'surf', 'body-slam'], 'swift-swim', NULL),
            ('Elite Four 4', 'flygon', 4, 53, FALSE, ARRAY['flamethrower', 'crunch', 'dragon-breath', 'earthquake'], 'levitate', NULL),
            ('Elite Four 4', 'salamence', 5, 55, TRUE, ARRAY['flamethrower', 'dragon-claw', 'rock-slide', 'crunch'], 'intimidate', NULL),
    
            -- WALLACE (Champion)
            ('Champion', 'wailord', 1, 57, FALSE, ARRAY['rain-dance', 'water-spout', 'double-edge', 'blizzard'], 'water-veil', NULL),
            ('Champion', 'tentacruel', 2, 55, FALSE, ARRAY['toxic', 'hydro-pump', 'sludge-bomb', 'ice-beam'], 'clear-body', NULL),
            ('Champion', 'ludicolo', 3, 56, FALSE, ARRAY['giga-drain', 'surf', 'leech-seed', 'double-team'], 'swift-swim', NULL),
            ('Champion', 'whiscash', 4, 56, FALSE, ARRAY['earthquake', 'surf', 'amnseia', 'hyper-beam'], 'oblivious', NULL),
            ('Champion', 'gyarados', 5, 56, FALSE, ARRAY['dragon-dance', 'earthquake', 'hyper-beam', 'surf'], 'intimidate', NULL),
            ('Champion', 'milotic', 6, 58, TRUE, ARRAY['recover', 'surf', 'ice-beam', 'toxic'], 'marvel-scale', NULL)
     ) AS t(stage_search, p_name, slot, lvl, ace, moves_arr, ability,condition)
         JOIN pokemon p ON p.name = t.p_name
         JOIN milestones m ON m.stage_name = t.stage_search
         JOIN games g ON m.game_id = g.id
WHERE g.name IN ('emerald', NULL);

INSERT INTO milestone_teams (milestone_id, pokemon_id, slot_number, level, is_ace, moves, ability, condition)
SELECT m.id, p.id, t.slot, t.lvl, t.ace, t.moves_arr, t.ability, t.condition
FROM (
         VALUES
             -- BROCK
             ('Pewter City - Gym 1', 'geodude', 1, 12, FALSE, ARRAY['tackle', 'defense-curl', 'rock-throw', 'rock-tomb'], 'rock-head', NULL),
             ('Pewter City - Gym 1', 'onix', 2, 14, TRUE, ARRAY['tackle', 'bind', 'rock-throw', 'rock-tomb'], 'rock-head', NULL),

             -- MISTY
             ('Cerulean City - Gym 2', 'staryu', 1, 18, FALSE, ARRAY['tackle', 'harden', 'recover', 'water-pulse'], 'natural-cure', NULL),
             ('Cerulean City - Gym 2', 'starmie', 2, 21, TRUE, ARRAY['swift', 'water-pulse', 'recover', 'rapid-spin'], 'natural-cure', NULL),

             -- LT. SURGE
             ('Vermilion City - Gym 3', 'voltorb', 1, 21, FALSE, ARRAY['tackle', 'screech', 'sonic-boom', 'shock-wave'], 'soundproof', NULL),
             ('Vermilion City - Gym 3', 'pikachu', 2, 18, FALSE, ARRAY['thunder-wave', 'quick-attack', 'double-team', 'shock-wave'], 'static', NULL),
             ('Vermilion City - Gym 3', 'raichu', 3, 24, TRUE, ARRAY['thunderbolt', 'thunder-wave', 'shock-wave', 'quick-attack'], 'static', NULL),

             -- ERIKA
             ('Celadon City - Gym 4', 'victreebel', 1, 29, FALSE, ARRAY['poison-powder', 'stun-spore', 'acid', 'giga-drain'], 'chlorophyll', NULL),
             ('Celadon City - Gym 4', 'tangela', 2, 24, FALSE, ARRAY['constrict', 'poison-powder', 'giga-drain', 'ingrain'], 'chlorophyll', NULL),
             ('Celadon City - Gym 4', 'vileplume', 3, 29, TRUE, ARRAY['poison-powder', 'stun-spore', 'acid', 'giga-drain'], 'chlorophyll', NULL),

             -- KOGA
             ('Fuchsia City - Gym 5', 'koffing', 1, 37, FALSE, ARRAY['smog', 'sludge', 'self-destruct', 'toxic'], 'levitate', NULL),
             ('Fuchsia City - Gym 5', 'muk', 2, 39, FALSE, ARRAY['sludge', 'minimize', 'acid-armor', 'toxic'], 'sticky-hold', NULL),
             ('Fuchsia City - Gym 5', 'koffing', 3, 37, FALSE, ARRAY['smog', 'sludge', 'self-destruct', 'toxic'], 'levitate', NULL),
             ('Fuchsia City - Gym 5', 'weezing', 4, 43, TRUE, ARRAY['sludge', 'smokescreen', 'toxic', 'tackle'], 'levitate', NULL),

             -- SABRINA
             ('Saffron City - Gym 6', 'kadabra', 1, 38, FALSE, ARRAY['psychic', 'reflect', 'future-sight', 'calm-mind'], 'inner-focus', NULL),
             ('Saffron City - Gym 6', 'mr-mime', 2, 37, FALSE, ARRAY['confusion', 'barrier', 'light-screen', 'calm-mind'], 'soundproof', NULL),
             ('Saffron City - Gym 6', 'venomoth', 3, 38, FALSE, ARRAY['psybeam', 'silver-wind', 'supersonic', 'gust'], 'shield-dust', NULL),
             ('Saffron City - Gym 6', 'alakazam', 4, 43, TRUE, ARRAY['psychic', 'recover', 'future-sight', 'calm-mind'], 'synchronize', NULL),

             -- BLAINE
             ('Cinnabar Island - Gym 7', 'growlithe', 1, 42, FALSE, ARRAY['ember', 'roar', 'take-down', 'fire-blast'], 'intimidate', NULL),
             ('Cinnabar Island - Gym 7', 'ponyta', 2, 40, FALSE, ARRAY['ember', 'stomp', 'fire-spin', 'fire-blast'], 'run-away', NULL),
             ('Cinnabar Island - Gym 7', 'rapidash', 3, 42, FALSE, ARRAY['ember', 'stomp', 'fire-spin', 'fire-blast'], 'run-away', NULL),
             ('Cinnabar Island - Gym 7', 'arcanine', 4, 47, TRUE, ARRAY['bite', 'roar', 'extreme-speed', 'fire-blast'], 'intimidate', NULL),

             -- GIOVANNI
             ('Viridian City - Gym 8', 'rhyhorn', 1, 45, FALSE, ARRAY['take-down', 'scary-face', 'rock-blast', 'earthquake'], 'lightning-rod', NULL),
             ('Viridian City - Gym 8', 'dugtrio', 2, 42, FALSE, ARRAY['slash', 'sand-attack', 'mud-slap', 'earthquake'], 'sand-veil', NULL),
             ('Viridian City - Gym 8', 'nidoqueen', 3, 44, FALSE, ARRAY['poison-sting', 'body-slam', 'double-kick', 'earthquake'], 'poison-point', NULL),
             ('Viridian City - Gym 8', 'nidoking', 4, 45, FALSE, ARRAY['poison-sting', 'thrash', 'double-kick', 'earthquake'], 'poison-point', NULL),
             ('Viridian City - Gym 8', 'rhyhorn', 5, 50, TRUE, ARRAY['take-down', 'scary-face', 'rock-blast', 'earthquake'], 'lightning-rod', NULL),
             -- LORELEI
             ('Elite Four 1', 'dewgong', 1, 52, FALSE, ARRAY['hail', 'surf', 'ice-beam', 'safeguard'], 'thick-fat', NULL),
             ('Elite Four 1', 'cloyster', 2, 51, FALSE, ARRAY['spikes', 'surf', 'ice-beam', 'protect'], 'shell-armor', NULL),
             ('Elite Four 1', 'slowbro', 3, 52, FALSE, ARRAY['surf', 'ice-beam', 'amnesia', 'yawn'], 'own-tempo', NULL),
             ('Elite Four 1', 'jynx', 4, 54, FALSE, ARRAY['ice-punch', 'lovely-kiss', 'doubleslap', 'attract'], 'oblivious', NULL),
             ('Elite Four 1', 'lapras', 5, 54, TRUE, ARRAY['surf', 'ice-beam', 'body-slam', 'confuse-ray'], 'water-absorb', NULL),

             -- BRUNO
             ('Elite Four 2', 'onix', 1, 51, FALSE, ARRAY['rock-tomb', 'earthquake', 'double-edge', 'iron-tail'], 'sturdy', NULL),
             ('Elite Four 2', 'hitmonchan', 2, 53, FALSE, ARRAY['sky-uppercut', 'mach-punch', 'fire-punch', 'ice-punch'], 'keen-eye', NULL),
             ('Elite Four 2', 'hitmonlee', 3, 53, FALSE, ARRAY['mega-kick', 'hi-jump-kick', 'facade', 'foresight'], 'limber', NULL),
             ('Elite Four 2', 'onix', 4, 54, FALSE, ARRAY['roar', 'earthquake', 'double-edge', 'sandstorm'], 'sturdy', NULL),
             ('Elite Four 2', 'machamp', 5, 56, TRUE, ARRAY['cross-chop', 'scary-face', 'submission', 'bulk-up'], 'guts', NULL),

             -- AGATHA
             ('Elite Four 3', 'gengar', 1, 54, FALSE, ARRAY['confuse-ray', 'shadow-punch', 'toxic', 'double-team'], 'levitate', NULL),
             ('Elite Four 3', 'golbat', 2, 54, FALSE, ARRAY['air-cutter', 'bite', 'poison-fang', 'confuse-ray'], 'inner-focus', NULL),
             ('Elite Four 3', 'haunter', 3, 53, FALSE, ARRAY['night-shade', 'confuse-ray', 'dream-eater', 'hypnosis'], 'levitate', NULL),
             ('Elite Four 3', 'arbok', 4, 56, FALSE, ARRAY['sludge-bomb', 'bite', 'glare', 'screech'], 'intimidate', NULL),
             ('Elite Four 3', 'gengar', 5, 58, TRUE, ARRAY['shadow-ball', 'sludge-bomb', 'psychic', 'nightmare'], 'levitate', NULL),

             -- LANCE
             ('Elite Four 4', 'gyarados', 1, 56, FALSE, ARRAY['hyper-beam', 'dragon-rage', 'bite', 'twister'], 'intimidate', NULL),
             ('Elite Four 4', 'dragonair', 2, 54, FALSE, ARRAY['hyper-beam', 'dragon-rage', 'thunder-wave', 'twister'], 'shed-skin', NULL),
             ('Elite Four 4', 'dragonair', 3, 54, FALSE, ARRAY['hyper-beam', 'dragon-rage', 'thunder-wave', 'twister'], 'shed-skin', NULL),
             ('Elite Four 4', 'aerodactyl', 4, 58, FALSE, ARRAY['hyper-beam', 'wing-attack', 'ancient-power', 'scary-face'], 'pressure', NULL),
             ('Elite Four 4', 'dragonite', 5, 60, TRUE, ARRAY['hyper-beam', 'dragon-claw', 'outrage', 'safeguard'], 'inner-focus', NULL),

             -- IF PLAYER CHOSE SQUIRTLE (Blue has Venusaur)
             ('Champion', 'pidgeot', 1, 59, FALSE, ARRAY['aerial-ace', 'feather-dance', 'sand-attack', 'whirlwind'], 'keen-eye', NULL),
             ('Champion', 'alakazam', 2, 57, FALSE, ARRAY['psychic', 'recover', 'reflect', 'future-sight'], 'synchronize', NULL),
             ('Champion', 'rhydon', 3, 59, FALSE, ARRAY['earthquake', 'rock-tomb', 'take-down', 'scary-face'], 'lightning-rod', NULL),
             ('Champion', 'gyarados', 4, 59, FALSE, ARRAY['hydro-pump', 'dragon-rage', 'bite', 'thrash'], 'intimidate', NULL),
             ('Champion', 'arcanine', 5, 61, FALSE, ARRAY['fire-blast', 'extreme-speed', 'flamethrower', 'bite'], 'intimidate', NULL),
             ('Champion', 'venusaur', 6, 63, TRUE, ARRAY['solar-beam', 'growth', 'synthesis', 'sunny-day'], 'overgrow', NULL),
    
            -- IF PLAYER CHOSE CHARMANDER (Blue has Blastoise)
            ('Champion', 'exeggutor', 4, 59, FALSE, ARRAY['giga-drain', 'egg-bomb', 'sleep-powder', 'light-screen'], 'chlorophyll', NULL),
            ('Champion', 'blastoise', 6, 63, TRUE, ARRAY['hydro-pump', 'rain-dance', 'skull-bash', 'bite'], 'torrent', NULL),
    
            -- IF PLAYER CHOSE BULBASAUR (Blue has Charizard)
            ('Champion', 'charizard', 6, 63, TRUE, ARRAY['fire-blast', 'wing-attack', 'slash', 'dragon-claw'], 'blaze', NULL),
             
            -- LORELEI REMATCH
             ('Elite Four 1 Rematch', 'dewgong', 1, 64, FALSE, ARRAY['surf', 'ice-beam', 'signal-beam', 'safeguard'], 'thick-fat', NULL),
             ('Elite Four 1 Rematch', 'cloyster', 2, 63, FALSE, ARRAY['spikes', 'surf', 'ice-beam', 'rain-dance'], 'shell-armor', NULL),
             ('Elite Four 1 Rematch', 'piloswine', 3, 63, FALSE, ARRAY['earthquake', 'blizzard', 'hail', 'rock-slide'], 'oblivious', NULL),
             ('Elite Four 1 Rematch', 'jynx', 4, 66, FALSE, ARRAY['psychic', 'ice-beam', 'lovely-kiss', 'attract'], 'oblivious', NULL),
             ('Elite Four 1 Rematch', 'lapras', 5, 66, TRUE, ARRAY['surf', 'ice-beam', 'thunder', 'confuse-ray'], 'water-absorb', NULL),

             -- BRUNO REMATCH
             ('Elite Four 2 Rematch', 'steelix', 1, 65, FALSE, ARRAY['earthquake', 'iron-tail', 'crunch', 'rock-tomb'], 'sturdy', NULL),
             ('Elite Four 2 Rematch', 'hitmonchan', 2, 65, FALSE, ARRAY['sky-uppercut', 'mach-punch', 'fire-punch', 'ice-punch'], 'keen-eye', NULL),
             ('Elite Four 2 Rematch', 'hitmonlee', 3, 65, FALSE, ARRAY['mega-kick', 'hi-jump-kick', 'facade', 'blaze-kick'], 'limber', NULL),
             ('Elite Four 2 Rematch', 'steelix', 4, 66, FALSE, ARRAY['earthquake', 'dragon-breath', 'iron-tail', 'double-edge'], 'sturdy', NULL),
             ('Elite Four 2 Rematch', 'machamp', 5, 68, TRUE, ARRAY['cross-chop', 'scary-face', 'earthquake', 'bulk-up'], 'guts', NULL),

             -- AGATHA REMATCH
             ('Elite Four 3 Rematch', 'gengar', 1, 66, FALSE, ARRAY['shadow-ball', 'psychic', 'confuse-ray', 'sludge-bomb'], 'levitate', NULL),
             ('Elite Four 3 Rematch', 'crobat', 2, 66, FALSE, ARRAY['air-cutter', 'shadow-ball', 'poison-fang', 'confuse-ray'], 'inner-focus', NULL),
             ('Elite Four 3 Rematch', 'misdreavus', 3, 65, FALSE, ARRAY['shadow-ball', 'psychic', 'thunderbolt', 'confuse-ray'], 'levitate', NULL),
             ('Elite Four 3 Rematch', 'arbok', 4, 68, FALSE, ARRAY['sludge-bomb', 'giga-drain', 'earthquake', 'crunch'], 'intimidate', NULL),
             ('Elite Four 3 Rematch', 'gengar', 5, 70, TRUE, ARRAY['shadow-ball', 'psychic', 'thunderbolt', 'hypnosis'], 'levitate', NULL),

             -- LANCE REMATCH
             ('Elite Four 4 Rematch', 'gyarados', 1, 68, FALSE, ARRAY['dragon-dance', 'surf', 'hyper-beam', 'thunderbolt'], 'intimidate', NULL),
             ('Elite Four 4 Rematch', 'dragonite', 2, 66, FALSE, ARRAY['dragon-claw', 'flamethrower', 'thunderbolt', 'hyper-beam'], 'inner-focus', NULL),
             ('Elite Four 4 Rematch', 'kingdra', 3, 66, FALSE, ARRAY['surf', 'ice-beam', 'dragon-dance', 'hyper-beam'], 'swift-swim', NULL),
             ('Elite Four 4 Rematch', 'aerodactyl', 4, 70, FALSE, ARRAY['ancient-power', 'wing-attack', 'earthquake', 'hyper-beam'], 'pressure', NULL),
             ('Elite Four 4 Rematch', 'dragonite', 5, 72, TRUE, ARRAY['outrage', 'ice-beam', 'thunderbolt', 'hyper-beam'], 'inner-focus', NULL),
             -- CORE TEAM (Always Present)
             ('Champion Rematch', 'heracross', 1, 72, FALSE, ARRAY['megahorn', 'rock-tomb', 'counter', 'earthquake'], 'swarm', NULL),
             ('Champion Rematch', 'alakazam', 2, 73, FALSE, ARRAY['psychic', 'recover', 'reflect', 'calm-mind'], 'synchronize', NULL),
             ('Champion Rematch', 'tyranitar', 3, 72, FALSE, ARRAY['thunderbolt', 'crunch', 'aerial-ace', 'earthquake'], 'sand-stream', NULL),

             -- STARTER VARIATION: BLUE HAS VENUSAUR
             ('Champion Rematch', 'gyarados', 4, 73, FALSE, ARRAY['hydro-pump', 'dragon-dance', 'hyper-beam', 'thrash'], 'intimidate', NULL),
             ('Champion Rematch', 'arcanine', 5, 73, FALSE, ARRAY['fire-blast', 'extreme-speed', 'overheat', 'iron-tail'], 'intimidate', NULL),
             ('Champion Rematch', 'venusaur', 6, 75, TRUE, ARRAY['frenzy-plant', 'sludge-bomb', 'solar-beam', 'sunny-day'], 'overgrow', NULL),

             -- STARTER VARIATION: BLUE HAS BLASTOISE
             ('Champion Rematch', 'arcanine', 4, 73, FALSE, ARRAY['fire-blast', 'extreme-speed', 'overheat', 'bite'], 'intimidate', NULL),
             ('Champion Rematch', 'exeggutor', 5, 73, FALSE, ARRAY['giga-drain', 'psychic', 'sleep-powder', 'light-screen'], 'chlorophyll', NULL),
             ('Champion Rematch', 'blastoise', 6, 75, TRUE, ARRAY['hydro-cannon', 'ice-beam', 'surf', 'rain-dance'], 'torrent', NULL),

             -- STARTER VARIATION: BLUE HAS CHARIZARD
             ('Champion Rematch', 'exeggutor', 4, 73, FALSE, ARRAY['giga-drain', 'psychic', 'sleep-powder', 'solar-beam'], 'chlorophyll', NULL),
             ('Champion Rematch', 'gyarados', 5, 73, FALSE, ARRAY['hydro-pump', 'dragon-dance', 'hyper-beam', 'bite'], 'intimidate', NULL),
             ('Champion Rematch', 'charizard', 6, 75, TRUE, ARRAY['blast-burn', 'aerial-ace', 'fire-blast', 'dragon-claw'], 'blaze', NULL)
     ) AS t(stage_search, p_name, slot, lvl, ace, moves_arr, ability,condition)
         JOIN pokemon p ON p.name = t.p_name
         JOIN milestones m ON m.stage_name = t.stage_search
         JOIN games g ON m.game_id = g.id
WHERE g.name IN ('firered', 'leafgreen', NULL);

INSERT INTO milestone_teams (milestone_id, pokemon_id, slot_number, level, is_ace, moves, ability,condition)
SELECT m.id, p.id, t.slot, t.lvl, t.ace, t.moves_arr, t.ability, t.condition
FROM (
         VALUES
             -- ROARK
             ('Oreburgh City - Gym 1', 'geodude', 1, 12, FALSE, ARRAY['rock-throw', 'stealth-rock', 'defense-curl'], 'rock-head', NULL),
             ('Oreburgh City - Gym 1', 'onix', 2, 12, FALSE, ARRAY['rock-throw', 'stealth-rock', 'screech', 'bind'], 'sturdy', NULL),
             ('Oreburgh City - Gym 1', 'cranidos', 3, 14, TRUE, ARRAY['headbutt', 'pursuit', 'leer'], 'mold-breaker', NULL),

             -- GARDENIA
             ('Eterna City - Gym 2', 'cherubi', 1, 19, FALSE, ARRAY['grass-knot', 'growth', 'helping-hand', 'safeguard'], 'chlorophyll', NULL),
             ('Eterna City - Gym 2', 'turtwig', 2, 19, FALSE, ARRAY['razor-leaf', 'reflect', 'sunny-day', 'withdraw'], 'overgrow', NULL),
             ('Eterna City - Gym 2', 'roserade', 3, 22, TRUE, ARRAY['magical-leaf', 'grass-knot', 'poison-sting', 'stun-spore'], 'natural-cure', NULL),

             -- MAYLENE
             ('Veilstone City - Gym 3', 'meditite', 1, 27, FALSE, ARRAY['drain-punch', 'confusion', 'detect', 'light-screen'], 'pure-power', NULL),
             ('Veilstone City - Gym 3', 'machoke', 2, 27, FALSE, ARRAY['karate-chop', 'low-kick', 'foresight', 'rock-tomb'], 'guts', NULL),
             ('Veilstone City - Gym 3', 'lucario', 3, 30, TRUE, ARRAY['drain-punch', 'force-palm', 'metal-claw', 'bulk-up'], 'inner-focus', NULL),

             -- CRASHER WAKE
             ('Pastoria City - Gym 4', 'gyarados', 1, 27, FALSE, ARRAY['brine', 'bite', 'swagger', 'twister'], 'intimidate', NULL),
             ('Pastoria City - Gym 4', 'quagsire', 2, 27, FALSE, ARRAY['mud-shot', 'water-pulse', 'slam', 'rock-tomb'], 'damp', NULL),
             ('Pastoria City - Gym 4', 'floatzel', 3, 30, TRUE, ARRAY['brine', 'swift', 'pursuit', 'ice-fang'], 'swift-swim', NULL),

             -- FANTINA
             ('Hearthome City - Gym 5', 'drifblim', 1, 32, FALSE, ARRAY['ominous-wind', 'gust', 'focus-energy', 'payback'], 'aftermath', NULL),
             ('Hearthome City - Gym 5', 'gengar', 2, 34, FALSE, ARRAY['shadow-claw', 'confuse-ray', 'sucker-punch', 'poison-jab'], 'levitate', NULL),
             ('Hearthome City - Gym 5', 'mismagius', 3, 36, TRUE, ARRAY['shadow-ball', 'magical-leaf', 'confuse-ray', 'psybeam'], 'levitate', NULL),

             -- BYRON
             ('Canalave City - Gym 6', 'bronzor', 1, 36, FALSE, ARRAY['flash-cannon', 'confuse-ray', 'hypnosis', 'iron-defense'], 'levitate', NULL),
             ('Canalave City - Gym 6', 'steelix', 2, 36, FALSE, ARRAY['flash-cannon', 'ice-fang', 'thunder-fang', 'dragon-breath'], 'rock-head', NULL),
             ('Canalave City - Gym 6', 'bastiodon', 3, 39, TRUE, ARRAY['flash-cannon', 'ancient-power', 'iron-defense', 'rest'], 'sturdy', NULL),

             -- CANDICE
             ('Snowpoint City - Gym 7', 'snover', 1, 38, FALSE, ARRAY['grass-knot', 'ice-shard', 'ingrain', 'mist'], 'snow-warning', NULL),
             ('Snowpoint City - Gym 7', 'sneasel', 2, 38, FALSE, ARRAY['faint-attack', 'ice-shard', 'slash', 'aerial-ace'], 'inner-focus', NULL),
             ('Snowpoint City - Gym 7', 'medicham', 3, 40, FALSE, ARRAY['force-palm', 'ice-punch', 'confusion', 'detect'], 'pure-power', NULL),
             ('Snowpoint City - Gym 7', 'abomasnow', 4, 42, TRUE, ARRAY['avalanche', 'wood-hammer', 'water-pulse', 'grass-knot'], 'snow-warning', NULL),

             -- VOLKNER
             ('Sunyshore City - Gym 8', 'raichu', 1, 46, FALSE, ARRAY['charge-beam', 'thunderbolt', 'light-screen', 'thunder-wave'], 'static', NULL),
             ('Sunyshore City - Gym 8', 'ambipom', 2, 47, FALSE, ARRAY['shock-wave', 'baton-pass', 'agility', 'double-hit'], 'technician', NULL),
             ('Sunyshore City - Gym 8', 'octillery', 3, 48, FALSE, ARRAY['charge-beam', 'octazooka', 'bullet-seed', 'aurora-beam'], 'suction-cups', NULL),
             ('Sunyshore City - Gym 8', 'luxray', 4, 49, TRUE, ARRAY['thunder-fang', 'crunch', 'iron-tail', 'fire-fang'], 'rivalry', NULL),

             -- AARON
             ('Elite Four 1', 'dustox', 1, 53, FALSE, ARRAY['toxic', 'bug-buzz', 'light-screen', 'protect'], 'shield-dust', NULL),
             ('Elite Four 1', 'heracross', 2, 54, FALSE, ARRAY['stone-edge', 'close-combat', 'night-slash', 'aerial-ace'], 'swarm', NULL),
             ('Elite Four 1', 'vespiquen', 3, 54, FALSE, ARRAY['power-gem', 'attack-order', 'defend-order', 'heal-order'], 'pressure', NULL),
             ('Elite Four 1', 'beautifly', 4, 53, FALSE, ARRAY['bug-buzz', 'shadow-ball', 'psychic', 'energy-ball'], 'swarm', NULL),
             ('Elite Four 1', 'drapion', 5, 57, TRUE, ARRAY['x-scissor', 'cross-poison', 'ice-fang', 'aerial-ace'], 'battle-armor', NULL),

             -- BERTHA
             ('Elite Four 2', 'quagsire', 1, 55, FALSE, ARRAY['double-team', 'protect', 'dig', 'sandstorm'], 'water-absorb', NULL),
             ('Elite Four 2', 'hippowdon', 2, 59, TRUE, ARRAY['stone-edge', 'earthquake', 'crunch', 'curse'], 'sand-stream', NULL),
             ('Elite Four 2', 'sudowoodo', 3, 57, FALSE, ARRAY['low-kick', 'rock-slide', 'sucker-punch', 'sandstorm'], 'sturdy', NULL),
             ('Elite Four 2', 'whiscash', 4, 55, FALSE, ARRAY['zen-headbutt', 'earthquake', 'aqua-tail', 'sandstorm'], 'oblivious', NULL),
             ('Elite Four 2', 'golem', 5, 56, FALSE, ARRAY['fire-punch', 'earthquake', 'gyro-ball', 'brick-break'], 'sturdy', NULL),

             -- FLINT
             ('Elite Four 3', 'rapidash', 1, 58, FALSE, ARRAY['flare-blitz', 'solar-beam', 'bounce', 'sunny-day'], 'run-away', NULL),
             ('Elite Four 3', 'infernape', 2, 61, TRUE, ARRAY['flare-blitz', 'thunder-punch', 'mach-punch', 'earthquake'], 'blaze', NULL),
             ('Elite Four 3', 'steelix', 3, 57, FALSE, ARRAY['fire-fang', 'rock-tomb', 'screech', 'sunny-day'], 'rock-head', NULL),
             ('Elite Four 3', 'lopunny', 4, 57, FALSE, ARRAY['fire-punch', 'mirror-coat', 'charm', 'sunny-day'], 'cute-charm', NULL),
             ('Elite Four 3', 'drifblim', 5, 58, FALSE, ARRAY['will-o-wisp', 'ominous-wind', 'baton-pass', 'double-team'], 'aftermath', NULL),

             -- LUCIAN
             ('Elite Four 4', 'mr-mime', 1, 59, FALSE, ARRAY['psychic', 'thunderbolt', 'reflect', 'light-screen'], 'filter', NULL),
             ('Elite Four 4', 'girafarig', 2, 59, FALSE, ARRAY['psychic', 'crunch', 'double-hit', 'shadow-ball'], 'inner-focus', NULL),
             ('Elite Four 4', 'medicham', 3, 60, FALSE, ARRAY['drain-punch', 'fire-punch', 'ice-punch', 'thunder-punch'], 'pure-power', NULL),
             ('Elite Four 4', 'alakazam', 4, 60, FALSE, ARRAY['psychic', 'focus-blast', 'energy-ball', 'recover'], 'synchronize', NULL),
             ('Elite Four 4', 'bronzong', 5, 63, TRUE, ARRAY['psychic', 'gyro-ball', 'payback', 'calm-mind'], 'levitate', NULL),

             -- CYNTHIA
             ('Champion', 'spiritomb', 1, 61, FALSE, ARRAY['dark-pulse', 'psychic', 'silver-wind', 'embargo'], 'pressure', NULL),
             ('Champion', 'garchomp', 2, 66, TRUE, ARRAY['dragon-rush', 'earthquake', 'brick-break', 'giga-impact'], 'sand-veil', NULL),
             ('Champion', 'gastrodon', 3, 60, FALSE, ARRAY['muddy-water', 'earthquake', 'stone-edge', 'sludge-bomb'], 'sticky-hold', NULL),
             ('Champion', 'milotic', 4, 63, FALSE, ARRAY['surf', 'ice-beam', 'mirror-coat', 'aqua-ring'], 'marvel-scale', NULL),
             ('Champion', 'roserade', 5, 60, FALSE, ARRAY['energy-ball', 'sludge-bomb', 'shadow-ball', 'extrasensory'], 'natural-cure', NULL),
             ('Champion', 'lucario', 6, 63, FALSE, ARRAY['aura-sphere', 'dragon-pulse', 'psychic', 'earthquake'], 'inner-focus', NULL)
     ) AS t(stage_search, p_name, slot, lvl, ace, moves_arr, ability,condition)
         JOIN pokemon p ON p.name = t.p_name
         JOIN milestones m ON m.stage_name = t.stage_search
         JOIN games g ON m.game_id = g.id
WHERE g.name IN ('diamond', 'pearl', NULL);

INSERT INTO milestone_teams (milestone_id, pokemon_id, slot_number, level, is_ace, moves, ability,condition)
SELECT m.id, p.id, t.slot, t.lvl, t.ace, t.moves_arr, t.ability, t.condition
FROM (
         VALUES
             -- ROARK
             ('Oreburgh City - Gym 1', 'geodude', 1, 12, FALSE, ARRAY['rock-throw', 'stealth-rock', 'defense-curl'], 'rock-head', NULL),
             ('Oreburgh City - Gym 1', 'onix', 2, 12, FALSE, ARRAY['rock-throw', 'stealth-rock', 'screech', 'bind'], 'sturdy', NULL),
             ('Oreburgh City - Gym 1', 'cranidos', 3, 14, TRUE, ARRAY['headbutt', 'pursuit', 'leer'], 'mold-breaker', NULL),

             -- GARDENIA
             ('Eterna City - Gym 2', 'turtwig', 1, 20, FALSE, ARRAY['razor-leaf', 'reflect', 'sunny-day', 'grass-knot'], 'overgrow', NULL),
             ('Eterna City - Gym 2', 'cherrim', 2, 20, FALSE, ARRAY['leech-seed', 'magical-leaf', 'grass-knot', 'safeguard'], 'flower-gift', NULL),
             ('Eterna City - Gym 2', 'roserade', 3, 22, TRUE, ARRAY['magical-leaf', 'grass-knot', 'poison-sting', 'stun-spore'], 'natural-cure', NULL),

             -- FANTINA (Now Gym 3)
             ('Hearthome City - Gym 3', 'duskull', 1, 24, FALSE, ARRAY['shadow-sneak', 'pursuit', 'will-o-wisp', 'future-sight'], 'levitate', NULL),
             ('Hearthome City - Gym 3', 'haunter', 2, 24, FALSE, ARRAY['shadow-claw', 'confuse-ray', 'sucker-punch', 'hypnosis'], 'levitate', NULL),
             ('Hearthome City - Gym 3', 'mismagius', 3, 26, TRUE, ARRAY['shadow-ball', 'magical-leaf', 'confuse-ray', 'psybeam'], 'levitate', NULL),

             -- MAYLENE
             ('Veilstone City - Gym 4', 'meditite', 1, 28, FALSE, ARRAY['drain-punch', 'confusion', 'fake-out', 'rock-tomb'], 'pure-power', NULL),
             ('Veilstone City - Gym 4', 'machoke', 2, 29, FALSE, ARRAY['karate-chop', 'low-kick', 'foresight', 'rock-tomb'], 'guts', NULL),
             ('Veilstone City - Gym 4', 'lucario', 3, 32, TRUE, ARRAY['drain-punch', 'force-palm', 'metal-claw', 'bone-rush'], 'inner-focus', NULL),

             -- CRASHER WAKE
             ('Pastoria City - Gym 5', 'gyarados', 1, 33, FALSE, ARRAY['brine', 'bite', 'waterfall', 'twister'], 'intimidate', NULL),
             ('Pastoria City - Gym 5', 'quagsire', 2, 34, FALSE, ARRAY['mud-shot', 'water-pulse', 'slam', 'yawn'], 'water-absorb', NULL),
             ('Pastoria City - Gym 5', 'floatzel', 3, 37, TRUE, ARRAY['brine', 'swift', 'crunch', 'ice-fang'], 'swift-swim', NULL),

             -- BYRON
             ('Canalave City - Gym 6', 'magneton', 1, 37, FALSE, ARRAY['tri-attack', 'thunderbolt', 'flash-cannon', 'thunder-wave'], 'sturdy', NULL),
             ('Canalave City - Gym 6', 'steelix', 2, 38, FALSE, ARRAY['earthquake', 'ice-fang', 'sandstorm', 'flash-cannon'], 'rock-head', NULL),
             ('Canalave City - Gym 6', 'bastiodon', 3, 41, TRUE, ARRAY['metal-burst', 'ancient-power', 'iron-defense', 'stone-edge'], 'sturdy', NULL),

             -- CANDICE
             ('Snowpoint City - Gym 7', 'sneasel', 1, 40, FALSE, ARRAY['faint-attack', 'ice-shard', 'slash', 'aerial-ace'], 'inner-focus', NULL),
             ('Snowpoint City - Gym 7', 'piloswine', 2, 40, FALSE, ARRAY['earthquake', 'ancient-power', 'hail', 'avalanche'], 'oblivious', NULL),
             ('Snowpoint City - Gym 7', 'abomasnow', 3, 42, FALSE, ARRAY['avalanche', 'wood-hammer', 'water-pulse', 'ingrain'], 'snow-warning', NULL),
             ('Snowpoint City - Gym 7', 'froslass', 4, 44, TRUE, ARRAY['blizzard', 'shadow-ball', 'confuse-ray', 'hail'], 'snow-cloak', NULL),

             -- VOLKNER
             ('Sunyshore City - Gym 8', 'jolteon', 1, 46, FALSE, ARRAY['thunderbolt', 'double-kick', 'charge-beam', 'thunder-wave'], 'volt-absorb', NULL),
             ('Sunyshore City - Gym 8', 'raichu', 2, 46, FALSE, ARRAY['charge-beam', 'thunderbolt', 'focus-blast', 'quick-attack'], 'static', NULL),
             ('Sunyshore City - Gym 8', 'luxray', 3, 48, FALSE, ARRAY['thunder-fang', 'crunch', 'fire-fang', 'ice-fang'], 'rivalry', NULL),
             ('Sunyshore City - Gym 8', 'electivire', 4, 50, TRUE, ARRAY['thunder-punch', 'fire-punch', 'giga-impact', 'quick-attack'], 'motor-drive', NULL),
             
             -- AARON
             ('Elite Four 1', 'yanmega', 1, 49, FALSE, ARRAY['bug-buzz', 'air-slash', 'u-turn', 'double-team'], 'speed-boost', NULL),
             ('Elite Four 1', 'scizor', 2, 49, FALSE, ARRAY['iron-head', 'x-scissor', 'night-slash', 'quick-attack'], 'technician', NULL),
             ('Elite Four 1', 'vespiquen', 3, 50, FALSE, ARRAY['attack-order', 'defend-order', 'heal-order', 'power-gem'], 'pressure', NULL),
             ('Elite Four 1', 'heracross', 4, 51, FALSE, ARRAY['close-combat', 'megahorn', 'stone-edge', 'night-slash'], 'guts', NULL),
             ('Elite Four 1', 'drapion', 5, 53, TRUE, ARRAY['cross-poison', 'x-scissor', 'ice-fang', 'aerial-ace'], 'battle-armor', NULL),

             -- BERTHA
             ('Elite Four 2', 'whiscash', 1, 50, FALSE, ARRAY['earthquake', 'aqua-tail', 'zen-headbutt', 'sandstorm'], 'oblivious', NULL),
             ('Elite Four 2', 'gliscor', 2, 53, FALSE, ARRAY['earthquake', 'ice-fang', 'fire-fang', 'thunder-fang'], 'hyper-cutter', NULL),
             ('Elite Four 2', 'golem', 3, 52, FALSE, ARRAY['earthquake', 'stone-edge', 'fire-punch', 'thunder-punch'], 'sturdy', NULL),
             ('Elite Four 2', 'rhyperior', 4, 55, TRUE, ARRAY['earthquake', 'rock-wrecker', 'megahorn', 'avalanche'], 'solid-rock', NULL),
             ('Elite Four 2', 'hippowdon', 5, 52, FALSE, ARRAY['earthquake', 'stone-edge', 'crunch', 'yawn'], 'sand-stream', NULL),

             -- FLINT
             ('Elite Four 3', 'houndoom', 1, 52, FALSE, ARRAY['flamethrower', 'dark-pulse', 'sludge-bomb', 'sunny-day'], 'flash-fire', NULL),
             ('Elite Four 3', 'flareon', 2, 55, FALSE, ARRAY['fire-blast', 'giga-impact', 'quick-attack', 'will-o-wisp'], 'flash-fire', NULL),
             ('Elite Four 3', 'rapidash', 3, 53, FALSE, ARRAY['flare-blitz', 'solar-beam', 'bounce', 'sunny-day'], 'run-away', NULL),
             ('Elite Four 3', 'infernape', 4, 55, FALSE, ARRAY['flare-blitz', 'thunder-punch', 'mach-punch', 'shadow-claw'], 'blaze', NULL),
             ('Elite Four 3', 'magmortar', 5, 57, TRUE, ARRAY['fire-blast', 'thunder-bolt', 'solar-beam', 'hyper-beam'], 'flame-body', NULL),

             -- LUCIAN
             ('Elite Four 4', 'mr-mime', 1, 53, FALSE, ARRAY['psychic', 'thunderbolt', 'reflect', 'light-screen'], 'filter', NULL),
             ('Elite Four 4', 'espeon', 2, 55, FALSE, ARRAY['psychic', 'shadow-ball', 'quick-attack', 'signal-beam'], 'synchronize', NULL),
             ('Elite Four 4', 'bronzong', 3, 54, FALSE, ARRAY['psychic', 'gyro-ball', 'payback', 'earthquake'], 'levitate', NULL),
             ('Elite Four 4', 'alakazam', 4, 56, FALSE, ARRAY['psychic', 'focus-blast', 'energy-ball', 'recover'], 'synchronize', NULL),
             ('Elite Four 4', 'gallade', 5, 59, TRUE, ARRAY['drain-punch', 'psycho-cut', 'stone-edge', 'night-slash'], 'steadfast', NULL),

             -- CYNTHIA
             ('Champion', 'spiritomb', 1, 58, FALSE, ARRAY['dark-pulse', 'psychic', 'silver-wind', 'ominous-wind'], 'pressure', NULL),
             ('Champion', 'roserade', 2, 58, FALSE, ARRAY['energy-ball', 'sludge-bomb', 'shadow-ball', 'extrasensory'], 'natural-cure', NULL),
             ('Champion', 'togekiss', 3, 60, FALSE, ARRAY['air-slash', 'aura-sphere', 'water-pulse', 'shock-wave'], 'serene-grace', NULL),
             ('Champion', 'lucario', 4, 60, FALSE, ARRAY['aura-sphere', 'extreme-speed', 'shadow-ball', 'stone-edge'], 'inner-focus', NULL),
             ('Champion', 'milotic', 5, 58, FALSE, ARRAY['surf', 'ice-beam', 'mirror-coat', 'dragon-pulse'], 'marvel-scale', NULL),
             ('Champion', 'garchomp', 6, 62, TRUE, ARRAY['dragon-rush', 'earthquake', 'flamethrower', 'giga-impact'], 'sand-veil', NULL),

             -- BATTLE FRONTIER TAG (Volkner & Flint)
             ('Battle Frontier Tag', 'jolteon', 1, 56, FALSE, ARRAY['thunderbolt', 'double-kick', 'pin-missile', 'quick-attack'], 'volt-absorb', NULL),
             ('Battle Frontier Tag', 'luxray', 2, 56, FALSE, ARRAY['thunder-fang', 'crunch', 'ice-fang', 'fire-fang'], 'intimidate', NULL),
             ('Battle Frontier Tag', 'electivire', 3, 58, TRUE, ARRAY['thunder-punch', 'fire-punch', 'ice-punch', 'low-kick'], 'motor-drive', NULL),
             ('Battle Frontier Tag', 'houndoom', 4, 56, FALSE, ARRAY['flamethrower', 'dark-pulse', 'crunch', 'thunder-fang'], 'flash-fire', NULL),
             ('Battle Frontier Tag', 'flareon', 5, 56, FALSE, ARRAY['fire-blast', 'giga-impact', 'quick-attack', 'will-o-wisp'], 'flash-fire', NULL),
             ('Battle Frontier Tag', 'magmortar', 6, 58, TRUE, ARRAY['fire-blast', 'thunderbolt', 'solar-beam', 'hyper-beam'], 'flame-body', NULL),

             -- AARON REMATCH
             ('Elite Four 1 Rematch', 'yanmega', 1, 65, FALSE, ARRAY['bug-buzz', 'air-slash', 'u-turn', 'detect'], 'speed-boost', NULL),
             ('Elite Four 1 Rematch', 'scizor', 2, 65, FALSE, ARRAY['iron-head', 'x-scissor', 'night-slash', 'bullet-punch'], 'technician', NULL),
             ('Elite Four 1 Rematch', 'vespiquen', 3, 66, FALSE, ARRAY['attack-order', 'defend-order', 'heal-order', 'confuse-ray'], 'pressure', NULL),
             ('Elite Four 1 Rematch', 'heracross', 4, 67, FALSE, ARRAY['close-combat', 'megahorn', 'stone-edge', 'night-slash'], 'guts', NULL),
             ('Elite Four 1 Rematch', 'drapion', 5, 69, TRUE, ARRAY['cross-poison', 'x-scissor', 'ice-fang', 'crunch'], 'battle-armor', NULL),

             -- BERTHA REMATCH
             ('Elite Four 2 Rematch', 'whiscash', 1, 66, FALSE, ARRAY['earthquake', 'aqua-tail', 'zen-headbutt', 'fissure'], 'oblivious', NULL),
             ('Elite Four 2 Rematch', 'gliscor', 2, 69, FALSE, ARRAY['earthquake', 'ice-fang', 'x-scissor', 'guillotine'], 'hyper-cutter', NULL),
             ('Elite Four 2 Rematch', 'golem', 3, 68, FALSE, ARRAY['earthquake', 'stone-edge', 'explosion', 'heavy-slam'], 'sturdy', NULL),
             ('Elite Four 2 Rematch', 'rhyperior', 4, 71, TRUE, ARRAY['earthquake', 'rock-wrecker', 'megahorn', 'thunder-punch'], 'solid-rock', NULL),
             ('Elite Four 2 Rematch', 'hippowdon', 5, 68, FALSE, ARRAY['earthquake', 'stone-edge', 'crunch', 'yawn'], 'sand-stream', NULL),

             -- FLINT REMATCH
             ('Elite Four 3 Rematch', 'houndoom', 1, 68, FALSE, ARRAY['flamethrower', 'dark-pulse', 'sludge-bomb', 'sunny-day'], 'flash-fire', NULL),
             ('Elite Four 3 Rematch', 'flareon', 2, 71, FALSE, ARRAY['fire-blast', 'giga-impact', 'quick-attack', 'superpower'], 'flash-fire', NULL),
             ('Elite Four 3 Rematch', 'rapidash', 3, 69, FALSE, ARRAY['flare-blitz', 'solar-beam', 'bounce', 'sunny-day'], 'run-away', NULL),
             ('Elite Four 3 Rematch', 'infernape', 4, 71, FALSE, ARRAY['flare-blitz', 'thunder-punch', 'close-combat', 'mach-punch'], 'blaze', NULL),
             ('Elite Four 3 Rematch', 'magmortar', 5, 73, TRUE, ARRAY['fire-blast', 'thunderbolt', 'solar-beam', 'hyper-beam'], 'flame-body', NULL),

             -- LUCIAN REMATCH
             ('Elite Four 4 Rematch', 'mr-mime', 1, 69, FALSE, ARRAY['psychic', 'thunderbolt', 'reflect', 'light-screen'], 'filter', NULL),
             ('Elite Four 4 Rematch', 'espeon', 2, 71, FALSE, ARRAY['psychic', 'shadow-ball', 'quick-attack', 'signal-beam'], 'synchronize', NULL),
             ('Elite Four 4 Rematch', 'bronzong', 3, 70, FALSE, ARRAY['psychic', 'gyro-ball', 'payback', 'calm-mind'], 'levitate', NULL),
             ('Elite Four 4 Rematch', 'alakazam', 4, 72, FALSE, ARRAY['psychic', 'focus-blast', 'energy-ball', 'recover'], 'synchronize', NULL),
             ('Elite Four 4 Rematch', 'gallade', 5, 75, TRUE, ARRAY['drain-punch', 'psycho-cut', 'stone-edge', 'leaf-blade'], 'steadfast', NULL),

             -- CYNTHIA REMATCH
             ('Champion Rematch', 'spiritomb', 1, 74, FALSE, ARRAY['dark-pulse', 'psychic', 'silver-wind', 'ominous-wind'], 'pressure', NULL),
             ('Champion Rematch', 'roserade', 2, 74, FALSE, ARRAY['energy-ball', 'sludge-bomb', 'shadow-ball', 'extrasensory'], 'natural-cure', NULL),
             ('Champion Rematch', 'togekiss', 3, 76, FALSE, ARRAY['air-slash', 'aura-sphere', 'water-pulse', 'shock-wave'], 'serene-grace', NULL),
             ('Champion Rematch', 'lucario', 4, 76, FALSE, ARRAY['aura-sphere', 'extreme-speed', 'shadow-ball', 'stone-edge'], 'inner-focus', NULL),
             ('Champion Rematch', 'milotic', 5, 74, FALSE, ARRAY['surf', 'ice-beam', 'mirror-coat', 'dragon-pulse'], 'marvel-scale', NULL),
             ('Champion Rematch', 'garchomp', 6, 78, TRUE, ARRAY['dragon-rush', 'earthquake', 'flamethrower', 'giga-impact'], 'sand-veil', NULL)
     ) AS t(stage_search, p_name, slot, lvl, ace, moves_arr, ability,condition)
         JOIN pokemon p ON p.name = t.p_name
         JOIN milestones m ON m.stage_name = t.stage_search
         JOIN games g ON m.game_id = g.id
WHERE g.name IN ('platinum', NULL);
INSERT INTO milestone_teams (milestone_id, pokemon_id, slot_number, level, is_ace, moves, ability,condition)
SELECT m.id, p.id, t.slot, t.lvl, t.ace, t.moves_arr, t.ability,t.condition
FROM (
         VALUES
             -- FALKNER
             ('Violet City - Gym 1', 'pidgey', 1, 9, FALSE, ARRAY['tackle', 'sand-attack'], 'keen-eye', NULL),
             ('Violet City - Gym 1', 'pidgeotto', 2, 13, TRUE, ARRAY['tackle', 'sand-attack', 'roost', 'gust'], 'keen-eye', NULL),
             -- BUGSY
             ('Azalea Town - Gym 2', 'scyther', 1, 17, TRUE, ARRAY['u-turn', 'quick-attack', 'leer', 'focus-energy'], 'technician', NULL),
             ('Azalea Town - Gym 2', 'metapod', 2, 15, FALSE, ARRAY['tackle', 'harden'], 'shed-skin', NULL),
             ('Azalea Town - Gym 2', 'kakuna', 3, 15, FALSE, ARRAY['poison-sting', 'harden'], 'shed-skin', NULL),
             -- WHITNEY
             ('Goldenrod City - Gym 3', 'clefairy', 1, 17, FALSE, ARRAY['encore', 'mimic', 'double-slap', 'metronome'], 'cute-charm', NULL),
             ('Goldenrod City - Gym 3', 'miltank', 2, 19, TRUE, ARRAY['stomp', 'attract', 'milk-drink', 'rollout'], 'scrappy', NULL),
             -- MORTY
             ('Ecruteak City - Gym 4', 'gastly', 1, 21, FALSE, ARRAY['curse', 'spite', 'mean-look', 'confuse-ray'], 'levitate', NULL),
             ('Ecruteak City - Gym 4', 'haunter', 2, 21, FALSE, ARRAY['curse', 'night-shade', 'confuse-ray', 'sucker-punch'], 'levitate', NULL),
             ('Ecruteak City - Gym 4', 'haunter', 3, 23, FALSE, ARRAY['curse', 'mean-look', 'night-shade', 'sucker-punch'], 'levitate', NULL),
             ('Ecruteak City - Gym 4', 'gengar', 4, 25, TRUE, ARRAY['shadow-ball', 'mean-look', 'hypnosis', 'confuse-ray'], 'levitate', NULL),
             -- CHUCK
             ('Cianwood City - Gym 5', 'primeape', 1, 29, FALSE, ARRAY['leer', 'focus-energy', 'double-team', 'rock-slide'], 'vital-spirit', NULL),
             ('Cianwood City - Gym 5', 'poliwrath', 2, 31, TRUE, ARRAY['hypnosis', 'surf', 'focus-punch', 'body-slam'], 'water-absorb', NULL),
             -- JASMINE
             ('Olivine City - Gym 6', 'magnemite', 1, 30, FALSE, ARRAY['thunderbolt', 'supersonic', 'sonic-boom', 'thunder-wave'], 'magnet-pull', NULL),
             ('Olivine City - Gym 6', 'magnemite', 2, 30, FALSE, ARRAY['thunderbolt', 'supersonic', 'sonic-boom', 'thunder-wave'], 'magnet-pull', NULL),
             ('Olivine City - Gym 6', 'steelix', 3, 35, TRUE, ARRAY['iron-tail', 'rock-throw', 'screech', 'sandstorm'], 'rock-head', NULL),
             -- PRYCE
             ('Mahogany Town - Gym 7', 'seel', 1, 30, FALSE, ARRAY['icy-wind', 'hail', 'rest', 'snore'], 'thick-fat', NULL),
             ('Mahogany Town - Gym 7', 'dewgong', 2, 32, FALSE, ARRAY['icy-wind', 'aurora-beam', 'rest', 'sleep-talk'], 'thick-fat', NULL),
             ('Mahogany Town - Gym 7', 'piloswine', 3, 34, TRUE, ARRAY['icy-wind', 'mud-bomb', 'ancient-power', 'hail'], 'oblivious', NULL),
             -- CLAIR
             ('Blackthorn City - Gym 8', 'gyarados', 1, 38, FALSE, ARRAY['dragon-rage', 'bite', 'twister', 'dragon-pulse'], 'intimidate', NULL),
             ('Blackthorn City - Gym 8', 'dragonair', 2, 38, FALSE, ARRAY['thunder-wave', 'twister', 'dragon-pulse', 'slam'], 'shed-skin', NULL),
             ('Blackthorn City - Gym 8', 'dragonair', 3, 38, FALSE, ARRAY['thunder-wave', 'twister', 'dragon-pulse', 'fire-blast'], 'shed-skin', NULL),
             ('Blackthorn City - Gym 8', 'kingdra', 4, 41, TRUE, ARRAY['hydro-pump', 'dragon-pulse', 'smoke-screen', 'hyper-beam'], 'swift-swim', NULL),

             -- LT. SURGE
             ('Vermilion City - Kanto 1', 'raichu', 1, 51, TRUE, ARRAY['shock-wave', 'thunder-wave', 'quick-attack', 'double-team'], 'static', NULL),
             ('Vermilion City - Kanto 1', 'electrode', 2, 47, FALSE, ARRAY['charge-beam', 'swift', 'screech', 'double-team'], 'soundproof', NULL),
             ('Vermilion City - Kanto 1', 'electrode', 3, 47, FALSE, ARRAY['charge-beam', 'swift', 'screech', 'double-team'], 'static', NULL),
             ('Vermilion City - Kanto 1', 'magneton', 4, 47, FALSE, ARRAY['discharge', 'mirror-shot', 'supersonic', 'thunder-wave'], 'sturdy', NULL),
             ('Vermilion City - Kanto 1', 'electabuzz', 5, 53, FALSE, ARRAY['discharge', 'low-kick', 'light-screen', 'quick-attack'], 'static', NULL),
             -- SABRINA
             ('Saffron City - Kanto 2', 'espeon', 1, 53, FALSE, ARRAY['psychic', 'shadow-ball', 'calm-mind', 'skill-swap'], 'synchronize', NULL),
             ('Saffron City - Kanto 2', 'mr-mime', 2, 53, FALSE, ARRAY['psychic', 'mimic', 'reflect', 'light-screen'], 'filter', NULL),
             ('Saffron City - Kanto 2', 'alakazam', 3, 55, TRUE, ARRAY['psychic', 'reflect', 'skill-swap', 'energy-ball'], 'synchronize', NULL),
             -- ERIKA
             ('Celadon City - Kanto 3', 'jumpluff', 1, 51, FALSE, ARRAY['giga-drain', 'leech-seed', 'u-turn', 'sunny-day'], 'chlorophyll', NULL),
             ('Celadon City - Kanto 3', 'tangela', 2, 52, FALSE, ARRAY['ancient-power', 'giga-drain', 'sleep-powder', 'sunny-day'], 'chlorophyll', NULL),
             ('Celadon City - Kanto 3', 'victreebel', 3, 56, FALSE, ARRAY['leaf-storm', 'sludge-bomb', 'grass-knot', 'sunny-day'], 'chlorophyll', NULL),
             ('Celadon City - Kanto 3', 'bellossom', 4, 56, TRUE, ARRAY['solar-beam', 'giga-drain', 'sunny-day', 'synthesis'], 'chlorophyll', NULL),
             -- MISTY
             ('Cerulean City - Kanto 4', 'golduck', 1, 49, FALSE, ARRAY['surf', 'psychic', 'disable', 'water-pulse'], 'cloud-nine', NULL),
             ('Cerulean City - Kanto 4', 'quagsire', 2, 49, FALSE, ARRAY['earthquake', 'surf', 'amnesia', 'rain-dance'], 'water-absorb', NULL),
             ('Cerulean City - Kanto 4', 'lapras', 3, 52, FALSE, ARRAY['surf', 'ice-beam', 'body-slam', 'perish-song'], 'water-absorb', NULL),
             ('Cerulean City - Kanto 4', 'starmie', 4, 54, TRUE, ARRAY['surf', 'ice-beam', 'psychic', 'recover'], 'natural-cure', NULL),
             -- JANINE
             ('Fuchsia City - Kanto 5', 'crobat', 1, 47, FALSE, ARRAY['poison-fang', 'confuse-ray', 'wing-attack', 'screech'], 'inner-focus', NULL),
             ('Fuchsia City - Kanto 5', 'weezing', 2, 44, FALSE, ARRAY['sludge-bomb', 'toxic', 'explosion', 'double-hit'], 'levitate', NULL),
             ('Fuchsia City - Kanto 5', 'ariados', 3, 47, FALSE, ARRAY['poison-jab', 'night-shade', 'pin-missile', 'scary-face'], 'insomnia', NULL),
             ('Fuchsia City - Kanto 5', 'ariados', 4, 47, FALSE, ARRAY['poison-jab', 'night-shade', 'pin-missile', 'scary-face'], 'swarm', NULL),
             ('Fuchsia City - Kanto 5', 'venomoth', 5, 50, TRUE, ARRAY['sludge-bomb', 'psychic', 'double-team', 'silver-wind'], 'shield-dust', NULL),
             -- BROCK
             ('Pewter City - Kanto 6', 'graveler', 1, 51, FALSE, ARRAY['earthquake', 'rock-slide', 'rollout', 'defense-curl'], 'sturdy', NULL),
             ('Pewter City - Kanto 6', 'rhyhorn', 2, 51, FALSE, ARRAY['earthquake', 'horn-drill', 'scary-face', 'stomp'], 'lightning-rod', NULL),
             ('Pewter City - Kanto 6', 'omastar', 3, 53, FALSE, ARRAY['ancient-power', 'brine', 'protect', 'spike-cannon'], 'shell-armor', NULL),
             ('Pewter City - Kanto 6', 'onix', 4, 54, TRUE, ARRAY['iron-tail', 'rock-slide', 'screech', 'sandstorm'], 'sturdy', NULL),
             ('Pewter City - Kanto 6', 'kabutops', 5, 52, FALSE, ARRAY['aqua-jet', 'rock-slide', 'endure', 'giga-drain'], 'battle-armor', NULL),
             -- BLAINE
             ('Seafoam Island - Kanto 7', 'magmar', 1, 54, FALSE, ARRAY['lava-plume', 'sunny-day', 'confuse-ray', 'thunder-punch'], 'flame-body', NULL),
             ('Seafoam Island - Kanto 7', 'magcargo', 2, 54, FALSE, ARRAY['lava-plume', 'rock-slide', 'sunny-day', 'smog'], 'magma-armor', NULL),
             ('Seafoam Island - Kanto 7', 'rapidash', 3, 59, TRUE, ARRAY['flare-blitz', 'bounce', 'sunny-day', 'quick-attack'], 'run-away', NULL),
             -- BLUE
             ('Viridian City - Kanto 8', 'exeggutor', 1, 55, FALSE, ARRAY['psychic', 'leaf-storm', 'hypnosis', 'trick-room'], 'chlorophyll', NULL),
             ('Viridian City - Kanto 8', 'machamp', 2, 56, FALSE, ARRAY['dynamic-punch', 'stone-edge', 'no-guard', 'thunder-punch'], 'no-guard', NULL),
             ('Viridian City - Kanto 8', 'arcanine', 3, 58, FALSE, ARRAY['flare-blitz', 'extreme-speed', 'roar', 'dragon-pulse'], 'intimidate', NULL),
             ('Viridian City - Kanto 8', 'rhydon', 4, 58, FALSE, ARRAY['earthquake', 'stone-edge', 'megahorn', 'thunder-fang'], 'lightning-rod', NULL),
             ('Viridian City - Kanto 8', 'gyarados', 5, 52, FALSE, ARRAY['waterfall', 'ice-fang', 'return', 'dragon-dance'], 'intimidate', NULL),
             ('Viridian City - Kanto 8', 'pidgeot', 6, 60, TRUE, ARRAY['return', 'air-slash', 'roost', 'whirlwind'], 'keen-eye', NULL),
         -- WILL
        ('Elite Four 1', 'xatu', 1, 40, FALSE, ARRAY['psychic', 'confuse-ray', 'u-turn', 'me-first'], 'synchronize', NULL),
        ('Elite Four 1', 'jynx', 2, 41, FALSE, ARRAY['psychic', 'ice-punch', 'lovely-kiss', 'double-slap'], 'oblivious', NULL),
        ('Elite Four 1', 'exeggutor', 3, 41, FALSE, ARRAY['psychic', 'egg-bomb', 'wood-hammer', 'reflect'], 'chlorophyll', NULL),
        ('Elite Four 1', 'slowbro', 4, 41, FALSE, ARRAY['psychic', 'surf', 'curse', 'amnesia'], 'own-tempo', NULL),
        ('Elite Four 1', 'xatu', 5, 42, TRUE, ARRAY['psychic', 'confuse-ray', 'aerial-ace', 'psychic-shift'], 'early-bird', NULL),

        -- KOGA
        ('Elite Four 1', 'ariados', 1, 40, FALSE, ARRAY['poison-jab', 'spider-web', 'baton-pass', 'giga-drain'], 'insomnia', NULL),
        ('Elite Four 1', 'venomoth', 2, 41, FALSE, ARRAY['psychic', 'silver-wind', 'gust', 'supersonic'], 'shield-dust', NULL),
        ('Elite Four 1', 'forretress', 3, 43, FALSE, ARRAY['spikes', 'toxic-spikes', 'explosion', 'swift'], 'sturdy', NULL),
        ('Elite Four 1', 'muk', 4, 42, FALSE, ARRAY['sludge-bomb', 'minimize', 'screech', 'gunk-shot'], 'sticky-hold', NULL),
        ('Elite Four 1', 'crobat', 5, 44, TRUE, ARRAY['poison-fang', 'wing-attack', 'confuse-ray', 'double-team'], 'inner-focus', NULL),

        -- BRUNO
        ('Elite Four 1', 'hitmontop', 1, 42, FALSE, ARRAY['triple-kick', 'quick-attack', 'counter', 'dig'], 'technician', NULL),
        ('Elite Four 1', 'hitmonlee', 2, 42, FALSE, ARRAY['hi-jump-kick', 'blaze-kick', 'swagger', 'focus-energy'], 'limber', NULL),
        ('Elite Four 1', 'hitmonchan', 3, 42, FALSE, ARRAY['fire-punch', 'ice-punch', 'thunder-punch', 'bullet-punch'], 'keen-eye', NULL),
        ('Elite Four 1', 'onix', 4, 43, FALSE, ARRAY['earthquake', 'rock-slide', 'sandstorm', 'dragon-breath'], 'sturdy', NULL),
        ('Elite Four 1', 'machamp', 5, 46, TRUE, ARRAY['dynamic-punch', 'stone-edge', 'revenge', 'foresight'], 'no-guard', NULL),

        -- KAREN
        ('Elite Four 1', 'umbreon', 1, 42, FALSE, ARRAY['faint-attack', 'confuse-ray', 'double-team', 'payback'], 'synchronize', NULL),
        ('Elite Four 1', 'vileplume', 2, 42, FALSE, ARRAY['petall-dance', 'stun-spore', 'acid', 'moonlight'], 'chlorophyll', NULL),
        ('Elite Four 1', 'gengar', 3, 45, FALSE, ARRAY['shadow-ball', 'focus-blast', 'confuse-ray', 'spite'], 'levitate', NULL),
        ('Elite Four 1', 'murkrow', 4, 44, FALSE, ARRAY['faint-attack', 'sucker-punch', 'astonish', 'whirlwind'], 'insomnia', NULL),
        ('Elite Four 1', 'houndoom', 5, 47, TRUE, ARRAY['dark-pulse', 'flamethrower', 'crunch', 'nasty-plot'], 'flash-fire', NULL),

        -- LANCE
        ('Champion', 'gyarados', 1, 44, FALSE, ARRAY['waterfall', 'ice-fang', 'bite', 'dragon-dance'], 'intimidate', NULL),
        ('Champion', 'dragonite', 2, 49, FALSE, ARRAY['dragon-rush', 'thunder-wave', 'thunder', 'hyper-beam'], 'inner-focus', NULL),
        ('Champion', 'dragonite', 3, 49, FALSE, ARRAY['dragon-rush', 'thunder-wave', 'blizzard', 'hyper-beam'], 'inner-focus', NULL),
        ('Champion', 'aerodactyl', 4, 48, FALSE, ARRAY['aerial-ace', 'rock-slide', 'crunch', 'thunder-fang'], 'pressure', NULL),
        ('Champion', 'charizard', 5, 48, FALSE, ARRAY['fire-fang', 'air-slash', 'slash', 'dragon-claw'], 'blaze', NULL),
        ('Champion', 'dragonite', 6, 50, TRUE, ARRAY['outrage', 'fire-blast', 'safeguard', 'hyper-beam'], 'inner-focus', NULL),
         
         -- WILL REMATCH
        ('Elite Four 1 Rematch', 'bronzong', 1, 58, FALSE, ARRAY['psychic', 'gyro-ball', 'payback', 'confuse-ray'], 'levitate', NULL),
        ('Elite Four 1 Rematch', 'jynx', 2, 60, FALSE, ARRAY['psychic', 'ice-beam', 'lovely-kiss', 'fake-out'], 'oblivious', NULL),
        ('Elite Four 1 Rematch', 'grumpig', 3, 59, FALSE, ARRAY['psychic', 'confuse-ray', 'power-gem', 'signal-beam'], 'own-tempo', NULL),
        ('Elite Four 1 Rematch', 'slowbro', 4, 60, FALSE, ARRAY['psychic', 'surf', 'flamethrower', 'amnesia'], 'own-tempo', NULL),
        ('Elite Four 1 Rematch', 'gardevoir', 5, 61, FALSE, ARRAY['psychic', 'focus-blast', 'calm-mind', 'double-team'], 'trace', NULL),
        ('Elite Four 1 Rematch', 'xatu', 6, 62, TRUE, ARRAY['psychic', 'shadow-ball', 'aerial-ace', 'confuse-ray'], 'early-bird', NULL),

        -- KOGA REMATCH
        ('Elite Four 2 Rematch', 'skuntank', 1, 61, FALSE, ARRAY['poison-jab', 'crunch', 'explosion', 'sucker-punch'], 'aftermath', NULL),
        ('Elite Four 2 Rematch', 'toxicroak', 2, 60, FALSE, ARRAY['poison-jab', 'cross-chop', 'x-scissor', 'swagger'], 'anticipation', NULL),
        ('Elite Four 2 Rematch', 'swalot', 3, 62, FALSE, ARRAY['sludge-bomb', 'ice-beam', 'yawn', 'amnesia'], 'liquid-ooze', NULL),
        ('Elite Four 2 Rematch', 'venomoth', 4, 63, FALSE, ARRAY['bug-buzz', 'psychic', 'sleep-powder', 'double-team'], 'shield-dust', NULL),
        ('Elite Four 2 Rematch', 'muk', 5, 62, FALSE, ARRAY['gunk-shot', 'screech', 'minimize', 'fire-punch'], 'sticky-hold', NULL),
        ('Elite Four 2 Rematch', 'crobat', 6, 64, TRUE, ARRAY['cross-poison', 'brave-bird', 'zen-headbutt', 'confuse-ray'], 'inner-focus', NULL),

        -- BRUNO REMATCH
        ('Elite Four 3 Rematch', 'hitmontop', 1, 62, FALSE, ARRAY['triple-kick', 'quick-attack', 'mach-punch', 'counter'], 'technician', NULL),
        ('Elite Four 3 Rematch', 'hitmonlee', 2, 61, FALSE, ARRAY['hi-jump-kick', 'blaze-kick', 'rock-slide', 'stop-reversal'], 'limber', NULL),
        ('Elite Four 3 Rematch', 'hariyama', 3, 62, FALSE, ARRAY['force-palm', 'bulk-up', 'payback', 'stone-edge'], 'thick-fat', NULL),
        ('Elite Four 3 Rematch', 'machamp', 4, 64, TRUE, ARRAY['dynamic-punch', 'stone-edge', 'fire-punch', 'bullet-punch'], 'no-guard', NULL),
        ('Elite Four 3 Rematch', 'lucario', 5, 64, FALSE, ARRAY['aura-sphere', 'extreme-speed', 'dragon-pulse', 'iron-defense'], 'inner-focus', NULL),
        ('Elite Four 3 Rematch', 'hitmonchan', 6, 61, FALSE, ARRAY['fire-punch', 'ice-punch', 'thunder-punch', 'bullet-punch'], 'keen-eye', NULL),

        -- KAREN REMATCH
        ('Elite Four 4 Rematch', 'weavile', 1, 62, FALSE, ARRAY['night-slash', 'ice-shard', 'ice-punch', 'low-kick'], 'pressure', NULL),
        ('Elite Four 4 Rematch', 'spiritomb', 2, 62, FALSE, ARRAY['dark-pulse', 'curse', 'confuse-ray', 'pain-split'], 'pressure', NULL),
        ('Elite Four 4 Rematch', 'honchkrow', 3, 64, FALSE, ARRAY['drill-peck', 'night-slash', 'sucker-punch', 'thunder-wave'], 'insomnia', NULL),
        ('Elite Four 4 Rematch', 'umbreon', 4, 64, FALSE, ARRAY['payback', 'curse', 'confuse-ray', 'double-team'], 'synchronize', NULL),
        ('Elite Four 4 Rematch', 'houndoom', 5, 63, FALSE, ARRAY['dark-pulse', 'flamethrower', 'sludge-bomb', 'nasty-plot'], 'flash-fire', NULL),
        ('Elite Four 4 Rematch', 'absol', 6, 63, TRUE, ARRAY['night-slash', 'psycho-cut', 'perish-song', 'detect'], 'super-luck', NULL),

        -- LANCE REMATCH
        ('Champion Rematch', 'salamence', 1, 72, FALSE, ARRAY['dragon-claw', 'flamethrower', 'rest', 'shadow-claw'], 'intimidate', NULL),
        ('Champion Rematch', 'garchomp', 2, 72, FALSE, ARRAY['outrage', 'earthquake', 'swords-dance', 'roar'], 'sand-veil', NULL),
        ('Champion Rematch', 'dragonite', 3, 75, TRUE, ARRAY['extreme-speed', 'outrage', 'hyper-beam', 'fire-blast'], 'inner-focus', NULL),
        ('Champion Rematch', 'charizard', 4, 68, FALSE, ARRAY['fire-blast', 'air-slash', 'dragon-pulse', 'hyper-beam'], 'blaze', NULL),
        ('Champion Rematch', 'altaria', 5, 73, FALSE, ARRAY['dragon-pulse', 'sky-attack', 'perish-song', 'double-team'], 'natural-cure', NULL),
        ('Champion Rematch', 'gyarados', 6, 68, FALSE, ARRAY['waterfall', 'ice-fang', 'thunder-bolt', 'dragon-dance'], 'intimidate', NULL)
     ) AS t(stage_search, p_name, slot, lvl, ace, moves_arr, ability,condition)
         JOIN pokemon p ON p.name = t.p_name
         JOIN milestones m ON m.stage_name = t.stage_search
         JOIN games g ON m.game_id = g.id
WHERE g.name IN ('heartgold-soulsilver', NULL);
