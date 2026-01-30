"""
Models for representing Pokémon data structures.
"""
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator, field_validator
class Region(BaseModel):
    id: int
    name: str

class FamilyMember(BaseModel):
    """Represents a single relative in the evolution line."""
    id: int
    name: str

class EvolutionChain(BaseModel):
    """
    Represents the 'evolutionchain' block from the GraphQL response.
    Maps the API's 'pokemonspecies' array to a Python list.
    """
    pokemonspecies: List[FamilyMember]
    
class VersionGroupRegion(BaseModel):
    region: Region

class VersionGroup(BaseModel):
    versiongroupregions: List[VersionGroupRegion]

class GameVersion(BaseModel):
    """
    Represents a Pokémon Game Version (e.g. Red, Blue)
    See fetch_all_games.graphql for the exact response structure
    """
    id: int
    name: str
    version_group_id: int
    versiongroup: VersionGroup

# --- Nested Helper Models ---

class PokemonType(BaseModel):
    name: str

class PokemonTypeSlot(BaseModel):
    slot: int
    type: PokemonType

class AbilityFlavorText(BaseModel):
    flavor_text: str

class AbilityDetail(BaseModel):
    name: str
    abilityflavortexts: List[AbilityFlavorText]

class PokemonAbilitySlot(BaseModel):
    slot: int
    ability: AbilityDetail

class NatDexNumber(BaseModel):
    pokedex_number: int

class PokemonSpecies(BaseModel):
    evolves_from_species_id: Optional[int]
    national_dex_number: int = Field(alias="pokemondexnumbers")
    evolution_chain: Optional[EvolutionChain] = Field(None, alias="evolutionchain")
    
    @field_validator("national_dex_number", mode="before")
    @classmethod
    def flatten_dex_number(cls, v):
        if isinstance(v, list) and len(v) > 0:
            dex_entry = v[0]
            if isinstance(dex_entry, dict) and "pokedex_number" in dex_entry:
                return int(dex_entry["pokedex_number"])
    
        if isinstance(v, int):
            return v
    
        return 0

class EncounterMethod(BaseModel):
    name: str

class MethodWrapper(BaseModel):
    encountermethod: EncounterMethod

class Location(BaseModel):
    id: int
    name: str
    region_id: int

class LocationArea(BaseModel):
    id: int
    name: str
    location: Location

class Encounter(BaseModel):
    version_id: int
    max_level: int
    min_level: int
    method: MethodWrapper
    location_area: LocationArea

    @model_validator(mode='after')
    def check_level_range(self) -> 'Encounter':
        if self.min_level > self.max_level:
            raise ValueError(
                f"min_level ({self.min_level}) cannot be higher than "
                f"max_level ({self.max_level})"
            )
        return self

class Pokemon(BaseModel):
    id: int
    raw_name: str = Field(alias="name") # "avalugg-hisui"
    clean_name: str = ""                # Will become "Avalugg"
    form_label: Optional[str] = None    # Will become "Hisui" or None (in the case of standard)
    types: List[PokemonTypeSlot] = Field(alias="pokemontypes")
    pokemonabilities: List[PokemonAbilitySlot]
    pokemonspecy: PokemonSpecies
    encounters: List[Encounter] = Field(default_factory=list)
    
    @model_validator(mode='after')
    def split_name_and_form(self) -> 'Pokemon':
        # Common suffixes that indicate a regional form or special variant
        variants = {'hisui', 'alola', 'galar', 'paldea'}

        parts = self.raw_name.split("-")

        # If the last part of the name is in our variant list
        if len(parts) > 1 and parts[-1].lower() in variants:
            # Join back the first parts (handles "mr-mime-galar" -> "Mr-Mime")
            self.clean_name = "-".join(parts[:-1]).lower()
            self.form_label = parts[-1].lower()
        else:
            self.clean_name = self.raw_name.lower()
            self.form_label = None

        return self
    
    @property
    def name(self) -> str:
        # will give you the clean name (cyndaquil) or raw name as fall-back (cyndaquil-hisui)
        return self.clean_name or self.raw_name
class PokemonData(BaseModel):
    pokemon: List[Pokemon]

class FetchAllPokemon(BaseModel):
    data: PokemonData
