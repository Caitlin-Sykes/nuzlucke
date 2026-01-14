import os
import tomllib

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from typing import Literal
load_dotenv()

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
    database: DatabaseSettings
    api: ApiConfig
    ruleset: RulesetConfig
    logging: LoggingConfig

def load_settings() -> Settings:
    """
    Loads configuration from config.toml and environment variables.
    Pydantic handles the merging and validation.
    """
    toml_path = "config.toml"
    conf_dict = {}

    if os.path.exists(toml_path):
        with open(toml_path, "rb") as f:
            conf_dict = tomllib.load(f)

    try:
        return Settings(**conf_dict)
    except ValidationError as e:
        print(f"Configuration Error detected in config.toml: {e}")
        print("Falling back to default settings and environment variables.")
        # Return default Settings if TOML is malformed
        return Settings(
            database=DatabaseSettings(),
            api=ApiConfig(),
            ruleset=RulesetConfig(),
            logging=LoggingConfig()
            
        )
# Settings.model_rebuild()
Config = load_settings()