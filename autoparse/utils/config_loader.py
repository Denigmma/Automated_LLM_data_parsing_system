import os
import yaml
from types import SimpleNamespace

# Determine project root and configs directory
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
CONFIG_DIR = os.getenv("CONFIG_DIR", os.path.join(PROJECT_ROOT, "configs"))


def load_config(file_name: str = "default.yaml") -> SimpleNamespace:
    """
    Load a YAML config file from the configs directory and return
    a nested namespace for attribute-style access.

    Args:
        file_name: name of the YAML file in CONFIG_DIR

    Raises:
        FileNotFoundError if the file does not exist
        yaml.YAMLError on parse errors
    """
    path = os.path.join(CONFIG_DIR, file_name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "rt", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return _dict_to_namespace(data)


def _dict_to_namespace(d: dict) -> SimpleNamespace:
    """
    Recursively convert a dict into SimpleNamespace,
    so you can do cfg.section.option instead of cfg["section"]["option"].
    """
    for key, val in d.items():
        if isinstance(val, dict):
            d[key] = _dict_to_namespace(val)
    return SimpleNamespace(**d)
