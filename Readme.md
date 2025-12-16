## To Create the DB

pre-requisities:
- in the pokemon_dataload_folder, open the .env file. 
  - whatever generations you want to load into your db, add them to the GENERATIONS_TO_LOAD variable, like so.  ```GENERATIONS_TO_LOAD=[1,2]```
- start docker-desktop, or run under docker-linux
- cd into db folder
- run docker-compose up

## To reset the DB
- run ./reset.ps1

## To teardown the DB
- run ./teardown.ps1

## To get logs
- docker logs nuzlucke  