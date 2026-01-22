



NUZLOCKE_VALIDATION_QUERY = """
query NuzlockeCatchableForms($versionIds: [Int!]!, $validMethods: [String!]!) {
  encounter( 
    where: {
      version_id: {_in: $versionIds},
      encounterslot: {
        encountermethod: { 
          name: {_in: $validMethods} 
        }
      }
    }
    distinct_on: [pokemon_id] 
    order_by: {pokemon_id: asc}
  ) {
    pokemon_id 
  }
}
"""
"""This is used to try and filter out Pokemon that are obtainable, versus those that are not
For example, where a previous form is only obtainable via breeding, or by trading with another game
It does this by checking the encounter methods, such as whether it is obtained by running in grass, etc
This list is changeable in the .env

Response looks like this:
{
  "data": {
    "encounter": [
      {
        "pokemon_id": 1
      },
      {
        "pokemon_id": 4
      },
}
"""

ENCOUNTER_QUERY = """
query GetVersionEncounters($versionIds: [Int!]!, $validMethods: [String!]!) {
  pokemon: pokemon(
    where: {
      encounters: { version_id: { _in: $versionIds } }
    }
  ) {
    id
    name
    pokemontypes(
        where: { type: { generation_id: { _lte: $versionIds } } } 
        order_by: { slot: asc }
      ) {
        slot
        type {
          name
        }
      }
    pokemonabilities(order_by: { slot: asc }) {
        slot
        ability {
          name,
          abilityflavortexts(
            where: { language_id: { _eq: 9 } }
            limit: 1
          ) {
            flavor_text
          }
        }
      }
    pokemonspecy 
   {
    evolves_from_species_id
    } 
    encounters: encounters(
      distinct_on: [location_area_id, version_id],
      where: {
        version_id: { _in: $versionIds },
        encounterslot: { 
          encountermethod: { name: { _in: $validMethods } } 
        }
      }
    ) {
      version_id
      max_level
      min_level
      method: encounterslot {
        encountermethod { name }
      }
      location_area: locationarea {
        id
        name
        location: location {
          id
          name
          region_id
        }
      }
    }
  }
}
"""
"""

"""


GENERATION_DATA_QUERY = """
query GenData($genId: Int!) {
  pokemonspecies(
    where: { generation_id: { _lte: $genId } } 
    order_by: { id: asc }
  ) {
    id
    name
    evolves_from_species_id

    pokemons {
      id
      name

      pokemontypes(
        where: { type: { generation_id: { _lte: $genId } } } 
        order_by: { slot: asc }
      ) {
        slot
        type {
          name
        }
      }

      pokemonabilities(order_by: { slot: asc }) {
        slot
        ability {
          name,
          abilityflavortexts(
            where: { language_id: { _eq: 9 } }
            limit: 1
          ) {
            flavor_text
          }
        }
      }
    }
  }
}
"""
"""
This uses the genId variable to determine what generation to fetch data for
It also uses this for filtering, such as where there are differences in Pokemon's
Types between generations

Response looks like this:
{
  "data": {
    "pokemonspecies": [
      {
        "id": 1,
        "name": "bulbasaur",
        "evolves_from_species_id": null,
        "pokemons": [
          {
            "id": 1,
            "name": "bulbasaur",
            "pokemontypes": [
              {
                "slot": 1,
                "type": {
                  "name": "grass"
                }
              },
              {
                "slot": 2,
                "type": {
                  "name": "poison"
                }
              }
            ],
            "pokemonabilities": [
              {
                "slot": 1,
                "ability": {
                  "name": "overgrow"
                }
              },
              {
                "slot": 3,
                "ability": {
                  "name": "chlorophyll"
                }
              }
            ]
          }
        ]
      },
"""