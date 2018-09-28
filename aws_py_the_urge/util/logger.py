"""
Setup logging from logging.yaml in resources, or specified via env var LOG_CFG
"""
import logging.config
import os

import yaml


def setup(
        default_path=os.path.join(
            os.path.dirname(__file__), '../resources/logging.yaml'),
        default_level=logging.INFO,
        env_key='LOG_CFG'):
    """
    No Ddc
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as file:
            config = yaml.safe_load(file.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
