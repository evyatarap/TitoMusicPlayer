from gpiozero import Button
from time import sleep



if __name__ == '__main__':

    PIN_WIFI_RESET=5
    PIN_SPEAKER_EN=4

    print("GPIOListener Service started...")
    btn_reset_wifi = Button(PIN_WIFI_RESET)
    btn_spk_en = Button(PIN_WIFI_RESET)
    while True:
        if btn_reset_wifi.is_pressed:
            print("Wifi reset pressed")
        if btn_spk_en.is_pressed:
            print("Speaker is enabled")
        sleep(1)
