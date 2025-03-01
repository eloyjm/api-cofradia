import logging.config

import yaml
from config.app import config_app

# Load the logging config file
with open(config_app.logger_config_path, "rt") as f:
    config = yaml.safe_load(f.read())

# Configure the logging module with the config file
logging.config.dictConfig(config)

# Get a logger object
logger = logging.getLogger(config_app.logger_env)
