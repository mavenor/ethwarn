import RPi.GPIO as gpio
from time import time, sleep
import threading
gpio.setmode(gpio.BOARD)

class blinker(threading.Thread):
    thePin: int
    on_duration: float
    off_duration: float
    _stop_event: threading.Event
    def __init__(self, thePin: int, on: float, t: float):
        super(blinker, self).__init__()
        self.thePin = thePin
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

class outpin:
    thread: blinker = None
    num: int
    def __init__(self, num: int, init=gpio.LOW):
        self.num = num
        gpio.setup(self.num, gpio.OUT, initial=init)
    
    def set(self):
        if not self.thread is None:
            self.thread.stop()
        gpio.output(self.num, gpio.HIGH)
    
    def clear(self):
        if not self.thread is None:
            self.thread.stop()
        gpio.output(self.num, gpio.LOW)

    def blink(self, ondur: int , t: int):
        if not self.thread is None:
            self.thread.stop()
        self.thread = blinker(self.num, ondur, t)
        self.thread.start()
