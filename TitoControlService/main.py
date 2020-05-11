import pyttsx3

def main():
    engine = pyttsx3.init()
    engine.say("I will speak this text")
    engine.runAndWait()



if __name__ == '__main__':
    main()