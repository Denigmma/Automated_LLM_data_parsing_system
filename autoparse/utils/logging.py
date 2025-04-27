import os
import logging
import logging.config
import yaml

from autoparse.utils.config_loader import CONFIG_DIR

def setup_logging(
    default_path: str = "logging.yaml",
    default_level: int = logging.INFO,
    env_key: str = "LOG_CFG"
):
    """
    Configure Python logging from a YAML file in CONFIG_DIR.

    1) Check environment variable <env_key> for override filename.
    2) If relative, resolve against CONFIG_DIR.
    3) If the file exists, load it with yaml.safe_load and apply dictConfig.
    4) Otherwise, fall back to basicConfig with default_level.
    """
    cfg_file = os.getenv(env_key, default_path)
    if not os.path.isabs(cfg_file):
        cfg_file = os.path.join(CONFIG_DIR, cfg_file)

    if os.path.exists(cfg_file):
        with open(cfg_file, "rt", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        logging.config.dictConfig(cfg)
    else:
        logging.basicConfig(level=default_level)


# Initialize logging as soon as this module is imported
setup_logging()

# Expose a module-level logger factory for convenience
def get_logger(name: str) -> logging.Logger:
    """
    Return a logger with the given name, after configuration has been applied.
    """
    return logging.getLogger(name)
