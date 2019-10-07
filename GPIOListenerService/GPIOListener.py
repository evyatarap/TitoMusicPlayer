from gpiozero import Button
from time import sleep

  


if __name__ == '__main__':
    print("GPIOListener Service started...")
    btn_reset_wifi = Button(5)
    while True:
        if btn_reset_wifi.is_pressed:
            print("Wifi reset pressed")
        sleep(1)
