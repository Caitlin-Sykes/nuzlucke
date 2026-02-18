## Table of Contents
-tbd

## Prerequisites:
### For Production
- Docker Desktop

### For Development
- Python 3.14
- Node (I use 25)
- Java 21

##
[NOTE! Please see #Configuration before running if you want to see configuration options]

## Build Steps
### Prod
  - in the root folder, run ```docker compose up --build```

### Local Development

  #### DB Development
  - `docker compose --profile db up`

  #### Backend Development
 - `docker compose --profile backend up`

  #### UI Development
  - `docker compose --profile ui up`
  - 
## Configuration
- in the pokemon_dataload_folder, open the `config.toml` file.
  - whatever generations you want to load into your db, add them to the GENERATIONS_TO_LOAD variable, like so.  ```GENERATIONS_TO_LOAD=[1,2]```

- in the .env file
  - POSTGRES_USER - change the user
  - POSTGRES_PASSWORD - change the password for the db


## TODO:
- seed more data, 
  - only done up to gen 4 right now
  - applies to milestone teams
  - and milestones
- add romhacks
- make custom covers of some variety
- make front end look better
- check for more overrides
- tidy up readmes
- ci/cd pipelines
- lock down python user for db
- FIX 05_populate_milestone_teams_table.sql
- look into python optimisation
- java logger
- kanban

## Credits
- [PokeAPI](https://pokeapi.co/) - for the data I populate the db with
- [Serebii](https://www.serebii.net/) – For being a resource of knowledge to cross-reference against
- [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Main_Page) - Game covers, further cross-referencing
- [PokemonDB](https://pokemondb.ne) - Sprite images