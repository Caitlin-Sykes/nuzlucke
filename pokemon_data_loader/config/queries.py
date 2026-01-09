
FETCH_ALL_VERSIONS_QUERY = """
    query ListAllVersions {
        version(order_by: {id: asc}, where: {version_group_id: {_nin: [28, 29]}}) {
        id
        name
        version_group_id
        versiongroup {
          versiongroupregions {
            region {
              id
              name
            }
          }
        }
      }
    }
    """
""" Fetches all the game versions and regions from PokeAPI.
version_group_id 28 and 29 are equivalent to Japanese Red and Blue so we exclude them.
Response looks like this:
{
    "data": {
    "version": [
      {
        "id": 1,
        "name": "red",
        "version_group_id": 1,
        "versiongroup": {
          "versiongroupregions": [
            {
              "region": {
                "id": 1,
                "name": "kanto"
              }
            }
          ]
        }
      },
     ]
"""


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
This is used to fetch all the encounters for a given version and list of encounter methods.
It also provides useful information like the minimum and maximum level of the encounter,
as well as the location and area of the encounter.
Response looks like this:
{
  "data": {
    "pokemon": [
      {
        "id": 1,
        "name": "bulbasaur",
        "encounters": [
          {
            "version_id": 3,
            "max_level": 10,
            "min_level": 10,
            "method": {
              "encountermethod": {
                "name": "gift"
              }
            },
            "location_area": {
              "id": 281,
              "name": "cerulean-city-area",
              "location": {
                "id": 68,
                "name": "cerulean-city",
                "region_id": 1
              }
            }
          },
          {
            "version_id": 1,
            "max_level": 5,
            "min_level": 5,
            "method": {
              "encountermethod": {
                "name": "gift"
              }
            },
            "location_area": {
              "id": 285,
              "name": "pallet-town-area",
              "location": {
                "id": 86,
                "name": "pallet-town",
                "region_id": 1
              }
            }
          },
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