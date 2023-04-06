from _mqtt_pub import *
from _face import *
from _gps import *
import _pin
from _pin import *
from RPi.GPIO import HIGH
import time
import random as rnd
from numpy import ndarray

# pin = my abstraction over RPi.GPIO
# blink(on_duration_ms, total_cycle_ms)
# set() = out(HIGH)
# clear() = out(LOW)
# get() = in(), no pull-up/pulldown resistor

green = outpin(35)
red = outpin(36)
buzzer = outpin(37)
relay = outpin(38, init=HIGH)  # relays are active-low
alcohol = inpin(11)
spy = facemon()

# "do_sentry":
# make the driver intermittently pick up the alcohol IID device and breathe into it
# alcohol sampled when face detected

try:
    # intermittent BrAC (breath-alc-conc) checker
    def do_sentry():
        print("in sentry mode...")
        # global spy, red, green, buzzer, relay, alcohol
        green.set()
        red.clear()
        buzzer.clear()
        # time.sleep(rnd.randint(120, 1800))
        time.sleep(10)
        red.blink(20, 1600)
        buzzer.blink(100, 1000)
        start = time.time()
        face_found = False
        while True:
            face_found = spy.has_face()
            if (time.time() - start >= 10) or face_found:
                break
        if face_found:
            print("FOUND FAce")
            buzzer.clear()
            if not spy.match_face():
                print("New face")
                green.clear()
                buzzer.blink(400, 800)
                red.blink(200, 400)
                viol_msg = "Unverified driver!\n"
                try:
                    pos: fix = fix(12.916517, 79.132500)
                    viol_msg += f"Location (lat, long): {pos.lat:#8.4g}, {pos.lng:#8.4g}\n"
                except NoFixException:
                    viol_msg += f"Cannot get fix on location\n"
                push_data(viol_msg, "avoiding")
                print("Registering face...")
                green.blink(200, 400)
                spy.reset_face()
                spy.init_face()
            else:
                print("MATCHED!!!!")
                spy.store_face()
            if alcohol.get():
                green.clear()
                red.set()
                buzzer.blink(400, 800)
                red.blink(50, 100)
                relay.set()
                try:
                    speed: float = 0  # in km/h
                    if (speed > 5):
                        viol_msg = f"Drunken driver\nLocation (lat, long): {pos.lat:#8.4g}, {pos.lng:#8.4g}\n"
                        push_data(viol_msg, "violating")
                    else:
                        main()
                except NoFixException:
                    viol_msg = f"Drunken driver\nCannot get fix on location\n"
                    push_data(viol_msg, "violating")
                time.sleep(5)

            else:
                green.set()
                red.clear()
                buzzer.clear()
                relay.clear()

        else:
            green.clear()
            buzzer.blink(400, 800)
            red.blink(200, 400)
            try:
                pos: fix = fix(12.916517, 79.132500)
                viol_msg = f"Measurement avoided\nLocation (lat, long): {pos.lat:#8.4g}, {pos.lng:#8.4g}\n"
            except NoFixException:
                viol_msg = f"Measurement avoided\nCannot get fix on location\n"
            push_data(viol_msg, "avoiding")
            time.sleep(5)
            buzzer.clear()

        do_sentry()


    def wait_on_all_clear():
        global spy
        spy.wait_face()
        if alcohol.get():
            green.clear()
            relay.set()
            red.set()
            time.sleep(5)
            wait_on_all_clear()

        print("non-drunk driver, proceed")
        print("remembering face...")
        green.clear()
        green.blink(200, 400)
        spy.init_face()
        sleep(1/2)
        green.set()
        red.clear()
        relay.clear()
        return


    def main():
        green.blink(20, 1600)
        buzzer.clear()
        red.set()
        relay.set()
        # time.sleep(10)
        print("waiting...")
        wait_on_all_clear()
        print("going into sentry mode...")
        do_sentry()


    if __name__ == "__main__":
        main()
except KeyboardInterrupt:
    print("Caught ^C, quitting!\n")
    del green
    del red
    del buzzer
    del relay
    del alcohol
    del spy
