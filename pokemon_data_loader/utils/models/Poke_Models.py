"""
Models for representing Pokémon data structures.
"""
from pydantic import BaseModel
from typing import List

class Region(BaseModel):
    id: int
    name: str

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