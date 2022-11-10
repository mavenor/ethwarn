import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BOARD)

green = 15
relay = 13
red = 18
buzzer = 22
sensor = 11

class pin:
    num: int
    def __init__(self, inout):
        if (inout == 1):
            gpio.setup(self.num, gpio.OUT, initial=gpio.LOW)
        else:
            gpio.setup(self.num, gpio.IN)
    
    def set(self):
        gpio.output(self.num, gpio.HIGH)
    
    def clear(self):
        gpio.output(self.num, gpio.LOW)

    # def blink(self, ondur, freq):
    #     start = time.time_ns()
    #     gpio.output(self.num)
    #     time.sleep(ondur/1000000)
    def get(self):
        return gpio.input(self.num)


        

    
