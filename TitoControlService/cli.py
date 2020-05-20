from mopidy_json_client import formatting

class CLI(object):
    def __init__(self, on_play, on_stop, on_forward, on_backward, on_pair_tag):
        self.play = on_play
        self.stop = on_stop
        self.forward = on_forward
        self.backward = on_backward
        self.pair = on_pair_tag
    
    def show_playlists(self, playlists):
        formatting.print_nice('> User Playlists: ', playlists, format='browse')
    
    def start(self):
        cmd = ""
        while cmd != "exit" :
            cmd = input("TitoCLI >> ")

            if cmd == "help":
                print("play - Start playing current playlist\n \
                        stop - Stop playing current song \n\
                        forward - Move to the next song on the playlist \n\
                        backward - Move to the previous song on the playlist \n\
                        bind - Bind new RFID to a playlist \n")

            if cmd == "play":
                self.play()
            if cmd == "stop":
                self.stop()
            if cmd == "forward":
                self.forward()
            if cmd == "backward":
                self.backward()
            if cmd == "pair":
                self.pair()
        