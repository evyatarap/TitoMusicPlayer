from gpiozero import Button
from gpiozero import LED

class GPIOController(object):
    
    def __init__(self, config, on_play, on_stop, on_forward, on_backward):
        if config['debug'] == "false":
            gpios = config['playback_gpios']
            self.config = config
            self.btn_play = Button(int(gpios['play']))
            self.btn_stop = Button(int(gpios['stop']))
            self.btn_forward = Button(int(gpios['forward']))
            self.btn_backward = Button(int(gpios['backward']))

            self.btn_play.when_pressed = on_play
            self.btn_stop.when_pressed = on_stop
            self.btn_forward.when_pressed = on_forward
            self.btn_backward.when_pressed = on_backward

            self.power_led = LED(int(self.config['power_button_led']))

    def power_led_blink(self):
        self.power_led.blink()


