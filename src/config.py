import os
import yaml
from pathlib import Path
from typing import Any, Dict

PROJECT_ROOT = Path(__file__).parent.parent


def load_config(config_file: str = "config.yaml") -> Dict[str, Any]:
    config_path = PROJECT_ROOT / "config" / config_file

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r") as f:
        return yaml.safe_load(f)


class Config:
    def __init__(self):
        self.config = load_config()
        self._setup_paths()

    def _setup_paths(self):
        self.RAW_DATA_DIR = PROJECT_ROOT / self.config["data"]["raw_dir"]
        self.PROCESSED_DATA_DIR = PROJECT_ROOT / self.config["data"]["processed_dir"]
        self.FEATURES_DIR = PROJECT_ROOT / self.config["data"]["features_dir"]
        self.EXTERNAL_DIR = PROJECT_ROOT / self.config["data"]["external_dir"]
        self.MODELS_DIR = PROJECT_ROOT / self.config["models"]["saved_dir"]
        self.REGISTRY_DIR = PROJECT_ROOT / self.config["models"]["registry_dir"]

        self.RAW_DATA_DIR.mkdir(exist_ok=True, parents=True)
        self.PROCESSED_DATA_DIR.mkdir(exist_ok=True, parents=True)
        self.FEATURES_DIR.mkdir(exist_ok=True, parents=True)
        self.MODELS_DIR.mkdir(exist_ok=True, parents=True)

    @property
    def project_name(self) -> str:
        return self.config["project"]["name"]

    @property
    def version(self) -> str:
        return self.config["project"]["version"]

    @property
    def data_config(self) -> Dict[str, Any]:
        return self.config["data"]

    @property
    def model_config(self) -> Dict[str, Any]:
        return self.config["models"]

    @property
    def api_config(self) -> Dict[str, Any]:
        return self.config["api"]


config = Config()