import os
import tomllib
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from typing import Literal
if not os.getenv("DOCKER_CONTAINER"):
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)

class ApiConfig(BaseModel):
    """Schema for external API endpoints and settings."""
    url: str = "https://graphql.pokeapi.co/v1beta2"

class DatabaseSettings(BaseModel):
    """Schema for Database credentials and connection info."""
    host: str = Field(default_factory=lambda: os.getenv("DB_HOST"))
    name: str = Field(default_factory=lambda: os.getenv("POSTGRES_DB"))
    user: str = Field(default_factory=lambda: os.getenv("POSTGRES_USER"))
    password: str = Field(default_factory=lambda: os.getenv("POSTGRES_PASSWORD"))

class RulesetConfig(BaseModel):
    """Schema for application-specific logic and filters."""
    target_generations: list[int] = [1, 2]
    valid_encounter_methods: list[str] = Field(
        default_factory=lambda: ["walk", "gift", "surf", "old-rod", "good-rod", "super-rod"]
    )

class LoggingConfig(BaseModel):
    """Schema for application-specific logic and filters."""
    logging_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    logging_file_name: str = "nuzlucke.log"


class Settings(BaseModel):
    """Root configuration object combining all sub-configs."""
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    api: ApiConfig = Field(default_factory=ApiConfig)
    ruleset: RulesetConfig = Field(default_factory=RulesetConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

def load_settings() -> Settings:
    conf_dict = {}
    toml_path = Path(os.getcwd()) / "config.toml"
        
    if not toml_path.exists():
        toml_path = Path(__file__).resolve().parents[2] / "config.toml"
            
    if toml_path.exists():
        with open(toml_path, "rb") as f:
            conf_dict = tomllib.load(f)

    try:
        return Settings(**conf_dict)
    except ValidationError as e:
        print(f"Configuration Error: {e}")
        return Settings()

Config = load_settings()
