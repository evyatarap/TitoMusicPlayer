import os.path
import json
import pathlib
import logging

CONFIG_FILE_PATH = pathlib.Path.joinpath(pathlib.Path(__file__).parent, "config.json")
PLAYLISTS_CONFIG_FILE_PATH = pathlib.Path.joinpath(pathlib.Path(__file__).parent, "plalists_tags.json")

logger = logging.getLogger('tito_control_service')

class Config(object):

    def getConfig(self):
        return self._loadJsonFile(CONFIG_FILE_PATH)

    def getPlaylistsConfig(self):
        return self._loadJsonFile(PLAYLISTS_CONFIG_FILE_PATH)
        
    def _loadJsonFile(self, filePath):
        if os.path.isfile(filePath):
            with open(filePath) as json_data_file:
                try:
                    return json.load(json_data_file) 
                except Exception as ex:
                    logger.error("Failed to parse json configuration file: %s", ex)
                    return None
        else:
            logger.error("Configuration file not found: %s", filePath)
    
    def savePlaylistsConfig(self, jsonConfig):
        with open(PLAYLISTS_CONFIG_FILE_PATH, 'w') as json_file:
            json.dump(jsonConfig, json_file)

