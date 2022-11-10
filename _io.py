import RPi.GPIO as gpio
from time import time, sleep
import threading
gpio.setmode(gpio.BOARD)

green   = 15
relay   = 13
red     = 18
buzzer  = 22
sensor  = 11

class blinker(threading.Thread):
    thePin: int
    on_duration: float
    off_duration: float
    _stop_event: threading.Event
    def __init__(self, thePin: int, on: float, t: float):
        super(blinker, self).__init__()
        self._stop_event = threading.Event()
        self.on_duration = on/1000
        self.off_duration = (t - on)/1000
        
    def run(self):
        while not self.stopped():
            gpio.output(self.thePin, gpio.HIGH)
            sleep(self.on_duration)
            gpio.output(self.thePin, gpio.LOW)
            sleep(self.off_duration)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

class pin:
    thread: blinker = None
    num: int
    def __init__(self, inout):
        if (inout == 1):
            gpio.setup(self.num, gpio.OUT, initial=gpio.LOW)
        else:
            gpio.setup(self.num, gpio.IN)
    
    def set(self):
        if not self.thread is None:
            self.thread.stop()
        gpio.output(self.num, gpio.HIGH)
    
    def clear(self):
        if not self.thread is None:
            self.thread.stop()
        gpio.output(self.num, gpio.LOW)

    def blink(self, ondur: int , freq: int):
        if not self.thread is None:
            self.thread.stop()
        self.thread = blinker()
            
        
    def get(self):
        return gpio.input(self.num)
