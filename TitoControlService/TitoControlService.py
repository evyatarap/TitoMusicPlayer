import sys
from mopidy_json_client import MopidyClient
from configurations import Config
from GPIOController import GPIOPlaybackController
from cli import CLI
from google_speech import Speech
from RFIDController import RFIDReader
import logging
from logging import handlers
from pathlib import Path
import os
import argparse
import time

logger = logging.getLogger("TitoControlService")

class BussinessLogic(object):
    
    def __init__(self):
        self.config = Config()
        self.generalConfig = self.config.getGeneralConfig()
        self.playlistsTagsConfig = self.config.getPlaylistsConfig()
        self.current_playlist_uri = None

        self.mopidy = MopidyClient(
            ws_url=f"ws://{self.generalConfig['mopidy_url']}/mopidy/ws",
            error_handler=self._on_server_error,
            connection_handler=self._on_connection,
            autoconnect=False,
            retry_max=10,
            retry_secs=10
        )

        self.gpioPlackbackController = GPIOPlaybackController(  self.generalConfig, 
                                                                self._on_play_pressed, 
                                                                self._on_stop_pressed, 
                                                                self._on_forward_pressed, 
                                                                self._on_backward_pressed)

        self.cli = CLI( self._on_play_pressed, 
                        self._on_stop_pressed, 
                        self._on_forward_pressed, 
                        self._on_backward_pressed,
                        self._on_pair_tag)

    def _on_connection(self, conn_state):
        if conn_state:
            logger.info("Mopidy Connected!")
        else:
            logger.error("Failed to connect to mopidy server")
    
    def _on_server_error(self, error):
        logger.error("Mopidy server error: " + error)

    def _on_play_pressed(self):

        logger.info("play button pressed")        
        playlist_uri = None

        if self.generalConfig['tagging_enabled'] == "true":
            tagId = None
            if self.generalConfig['debug_rfid'] == "true":
                tagId = "1232145531"
            else:
                tagId = RFIDReader.ReadTag()
            
            if tagId is None: 
                    logger.warning("No RFID Tag found")
                    Speech("No RFID Tag found", "en").play()
            else:
                playlistInfo = self._getPlaylistInfoFromTagId(tagId)
                if playlistInfo is None:
                    logger.warning("Tag is not associated with any playlist")
                    Speech("Tag is not associated with any playlist", "en").play()
                else:
                    speech_text = f'Now playing: {playlistInfo["name"]}, playlist.'
                    logger.info(speech_text)
                    playlist_uri = playlistInfo['uri']
        else:
            speech_text = 'Start playing default playlist'
            playlist_uri = self.generalConfig['default_playlist']
            logger.info(f'{speech_text}: {playlist_uri}')
        
        # Only if its a new playlist clear the current one 
        # and notify the user via speech to text
        if ((self.current_playlist_uri is None) or
            (self.current_playlist_uri != playlist_uri)):
            
            Speech(speech_text, "en").play()
            self.mopidy.tracklist.clear()
            self.mopidy.tracklist.add(uris=[playlist_uri])

        self.mopidy.playback.play()
        
    def _getPlaylistInfoFromTagId(self, tagId):
        try:
            return self.playlistsTagsConfig[tagId]
        except Exception:
            return None

    def _on_stop_pressed(self):
        logger.info("stop button pressed")
        self.mopidy.playback.pause()
        pass

    def _on_forward_pressed(self):
        logger.info("next button pressed")
        self.mopidy.playback.next()
        pass

    def _on_backward_pressed(self):
        logger.info("prev button pressed")
        self.mopidy.playback.previous()
        pass

    def _on_pair_tag(self):
        logger.info("Pair tag to playlist, retreiving playlists from spotify")

        # Print list of available playlists from mopidy
        self.mopidy.playlists.as_list(on_result=self._on_playlist_received)

    def _on_playlist_received(self, playlist):
        self.cli.show_playlists(playlist)
        
        # Get playlist index from the list
        playlistIndex = int(input("Select playlist (enter index number): "))

        # Read RFID
        tagId = None
        print("Place your RFID tag ....")
        if self.generalConfig['debug'] == "true":
            tagId = "123214553"
        else:
            tagId = RFIDReader.ReadTag()
            pass

        if tagId is None:
            logger.error("Failed to read RFID tag, try again.")
            return
        
        # Get playlist uri and save it to a local config file with related rfid 
        self.playlistsTagsConfig = self.config.addPlaylistConfig(playlist[playlistIndex]['uri'], playlist[playlistIndex]['name'] ,tagId)
        
        logger.info(f'Playlist: {playlist[playlistIndex]["name"]} attached to Tag: {tagId}')


    def run(self, cli_mode):
        self.mopidy.connect()
        if cli_mode:
            self.cli.start()
        else:
            logger.info("Starting TitoControlService as service")
            while True:
                time.sleep(1)

def setup_logging():
    logger.setLevel(logging.DEBUG)

    # setup file logging handler
    LOG_FILE_PATH = "/var/log/TitoControlService/TitoControlService.log"
    log_file_dir = Path(LOG_FILE_PATH).parent
    if os.path.isdir(log_file_dir):
        fileHandler = handlers.RotatingFileHandler(LOG_FILE_PATH, maxBytes=1024*5, backupCount=5)
        logger.addHandler(fileHandler)
    else:
        logger.warning("Fail to write log to file, logging directory: {} doest not exists".format(log_file_dir))

    # setup stdout logging
    logger.addHandler(logging.StreamHandler(sys.stdout))

def main():
    
    setup_logging()
    parser = argparse.ArgumentParser()
    parser.add_argument("--cli", help="increase output verbosity")
    args = parser.parse_args()
    
    bl = BussinessLogic()
    bl.run(args.cli)

if __name__ == '__main__':
    main()
