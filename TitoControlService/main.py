import pyttsx3
from mopidy_json_client import MopidyClient
from configurations import Config


class BussinessLogic(object):

    def __init__(self):
        self.config = Config.getConfig()
        self.mopidy = MopidyClient(
            ws_url=f'ws://{self.config.mopidy_url}/mopidy/ws',
            error_handler=self.on_server_error,
            connection_handler=self.on_connection,
            autoconnect=False,
            retry_max=10,
            retry_secs=10
        )

    def on_connection()
        print("On connection")
    
    def on_server_error()
        print("Server error")

def main():

    

    engine = pyttsx3.init()
    engine.say("I will speak this text")
    engine.runAndWait()

if __name__ == '__main__':
    main()