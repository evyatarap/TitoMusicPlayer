import pyttsx3
from mopidy_json_client import MopidyClient
from configurations import Config
from GPIOController import GPIOPlaybackController
from cli import CLI
#from RFIDController import RFIDReader


class BussinessLogic(object):

    def __init__(self):
        self.config = Config.getConfig()
        self.mopidy = MopidyClient(
            ws_url=f"ws://{self.config['mopidy_url']}/mopidy/ws",
            error_handler=self._on_server_error,
            connection_handler=self._on_connection,
            autoconnect=False,
            retry_max=10,
            retry_secs=10
        )

        self.gpioPlackbackController = GPIOPlaybackController(  self.config, 
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
        pass

    def _on_stop_pressed(self):
        pass

    def _on_forward_pressed(self):
        pass

    def _on_backward_pressed(self):
        pass

    def _on_pair_tag(self):
        # Print list of available playlists from mopidy
        self.mopidy.playlists.as_list(on_result=self._on_playlist_received)

    def _on_playlist_received(self, playlist):
        self.cli.show_playlists(playlist)

        # Get playlist index from the list
        playlistIndex = input("Select playlist (enter index number): ")

        # Read RFID
        print("Place your RFID tag ....")
        if self.config['debug'] == "true":
            tagId = "123214553"
        else
            tagId = ""

        # Get playlist uri and save it to a local config file with related rfid 
        
    
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