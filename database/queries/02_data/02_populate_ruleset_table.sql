INSERT INTO rulesets (id, name, description)
VALUES
    (1, 'Vanilla Gen 1', 'All types and abilities as of Generation 1: Red, Yellow, Blue and Green'),
    (2, 'Vanilla Gen 2', 'All types and abilities as of Generation 2: Gold, Silver and Crystal'),
    (3, 'Vanilla Gen 3', 'All types and abilities as of Generation 3: Ruby, Sapphire and Emerald'),
    (4, 'Vanilla Gen 4', 'All types and abilities as of Generation 4: Diamond, Pearl, Platinum, Heartgold and Soulsilver'),
    (5, 'Vanilla Gen 5', 'All types and abilities as of Generation 5: Black, White, Black 2 and White 2'),
    (6, 'Vanilla Gen 6', 'All types and abilities as of Generation 6: X, Y, Omega Ruby and Alpha Sapphire'),
    (7, 'Vanilla Gen 7', 'All types and abilities as of Generation 7: Sun, Moon, Ultra Sun, Ultra Moon, Let''s Go Pikachu and Let''s Go Eevee'),
    (8, 'Vanilla Gen 8', 'All types and abilities as of Generation 8: Sword, Shield, Brilliant Diamond and Shining Pearl'),
    (9, 'Vanilla Gen 9', 'All types and abilities as of Generation 9: Scarlet and Violet')
ON CONFLICT (id) DO NOTHING;