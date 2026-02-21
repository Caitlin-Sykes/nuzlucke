A utility I wrote to extract possible mandatory battles from decompiled pokemon games 

- in the data folder, create a new folder for each game you want to generate a battle table for
  - ie, `data/red_blue`
  - It has to be seperated by an underscore for tables applying to more then one game. Firered, etc, are written as all one word, so it would be
  - `firered_leafgreen`
- You will need the moves file, the parties file, and the map scripts. place these in the folder you just created.
  - ie, the contents of the files might look like this:
    #### moves.asm 
    ```asm
      RhyhornEvosMoves:
      ; Evolutions
      db EVOLVE_LEVEL, 42, RHYDON
      db 0
      ; Learnset
      db 30, STOMP
      db 35, TAIL_WHIP
      db 40, FURY_ATTACK
      db 45, HORN_DRILL
      db 50, LEER
      db 55, TAKE_DOWN
      db 0
    ```
    
    #### parties.asm 
    ```asm
    ; Route 16
	db 29, GRIMER, KOFFING, 0
	db 33, WEEZING, 0
	db 26, GRIMER, GRIMER, GRIMER, GRIMER, 0
    ```
    #### scripts/ example file
    ```asm
     .LoadNames:
     ld hl, .CityName
     ld de, .LeaderName
     jp LoadGymLeaderAndCityName

    .CityName:
    db "CINNABAR ISLAND@"

    .LeaderName:
    db "BLAINE@"
    ```
    
- run `python3 main.py`
- the output will be in the `output` folder