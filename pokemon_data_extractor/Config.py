import os
import tomllib
from pathlib import Path


def load_settings():
    """Loads the configuration from the TOML file."""
    conf_dict = {}
    toml_path = Path(os.getcwd()) / "config.toml"

    if not toml_path.exists():
        toml_path = Path(__file__).resolve().parents[2] / "config.toml"

    if toml_path.exists():
        with open(toml_path, "rb") as f:
            conf_dict = tomllib.load(f)

    return conf_dict

Config = load_settings()
