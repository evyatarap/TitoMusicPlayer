import os.path
import json
import pathlib
import logging

CONFIG_FILE_PATH = pathlib.Path.joinpath(pathlib.Path(__file__).parent, "config.json")
logger = logging.getLogger('tito_control_service')

class Config(object):
    
    @staticmethod
    def getConfig():
        if os.path.isfile(CONFIG_FILE_PATH):
            with open(CONFIG_FILE_PATH) as json_data_file:
                try:
                    return json.load(json_data_file) 
                except Exception as ex:
                    logger.error("Failed to parse json configuration file: %s", ex)
                    return None
        else:
            logger.error("Configuration file not found: %s", CONFIG_FILE_PATH)