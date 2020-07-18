import pyttsx3
from mopidy_json_client import MopidyClient
from configurations import Config
from GPIOController import GPIOPlaybackController
from cli import CLI
from google_speech import Speech
from RFIDController import RFIDReader


class BussinessLogic(object):

    def __init__(self):
        self.config = Config()
        self.generalConfig = self.config.getGeneralConfig()
        self.playlistsTagsConfig = self.config.getPlaylistsConfig()

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
            print("Mopidy Connected!")
    
    def _on_server_error(self, error):
        print("Mopidy server error: " + error)

    def _on_play_pressed(self):

        print("play")        

        tagId = None
        if self.generalConfig['debug_rfid'] == "true":
            tagId = "1232145531"
        else:
            tagId = RFIDReader.ReadTag()
        
        if tagId is None: 
                print("No RFID Tag found")
                Speech("No RFID Tag foundd", "en").play()
        else:
            playlistInfo = self._getPlaylistInfoFromTagId(tagId)
            if playlistInfo is None:
                print("Tag is not associated with any playlist")
                Speech("Tag is not associated with any playlist", "en").play()
            else:
                Speech(f'Now playing: {playlistInfo["name"]}, playlist.', "en").play()
                self.mopidy.tracklist.clear()
                self.mopidy.tracklist.add(uris=[playlistInfo['uri']])
                self.mopidy.playback.play()
        
    def _getPlaylistInfoFromTagId(self, tagId):
        try:
            return self.playlistsTagsConfig[tagId]
        except Exception:
            return None

    def _on_stop_pressed(self):
        print("stop")
        self.mopidy.playback.pause()
        pass

    def _on_forward_pressed(self):
        print("next")
        self.mopidy.playback.next()
        pass

    def _on_backward_pressed(self):
        print("prev")
        self.mopidy.playback.previous()
        pass

    def _on_pair_tag(self):
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
            print("Failed to read RFID tag, try again.")
            return
        
        # Get playlist uri and save it to a local config file with related rfid 
        self.playlistsTagsConfig = self.config.addPlaylistConfig(playlist[playlistIndex]['uri'], playlist[playlistIndex]['name'] ,tagId)
        
        print(f'Playlist: {playlist[playlistIndex]["name"]} attached to Tag: {tagId}')

    
    def run(self):
        self.mopidy.connect()
        self.cli.start()


def main():
    bl = BussinessLogic()
    bl.run()

    #engine = pyttsx3.init()
    #engine.say("I will speak this text")
    #engine.runAndWait()

if __name__ == '__main__':
    main()
