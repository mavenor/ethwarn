import _mqtt_pub as mqtt
import _face as face
import _gps as gps
import _io
import time
import random as rnd

# pin = my abstraction over RPi.GPIO
    # blink(on_duration_ms, total_cycle_ms)
    # set() = out(HIGH)
    # clear() = out(LOW)
    # get() = in(), no pullup/pulldown resistor

relay:      pin
red:        pin
green:      pin
buzzer:     pin
face0:      face.face
alcohol:    pin
spy:        face.facemon

# make the driver intermittently pick up the alcohol IID device and breathe into it
# alcohol sampled when face detected

# intermittent BrAC (breath-alc-conc) checker
def do_sentry():
    red.clear()
    time.sleep(rnd.randint(120, 1800))
    red.blink(20, 1600)
    buzzer.blink(100, 1000)
    start = time.time()
    while True:
        if (not ((time.time() - start < 90) or (spy.has_face() and spy.match_face()))):
            break
    
    if not spy.has_face():
        green.clear()
        try:
            pos: gps.fix = gps.get_fix()
            viol_msg = f"Measurement avoided\nLocation (lat, long): {pos.latit:#8.4g}, {pos.longit:#8.4g}\n"
        except gps.NoFixException:
            viol_msg = f"Measurement avoided\nCannot get fix on location\n"
        mqtt.push_data(viol_msg, "avoiding")
    else:
        if (alcohol.get() == 1):
            red.set()
            buzzer.blink(1000, 1100)
            time.sleep(10)
            relay.clear()
            try:
                speed: float = gps.getspeed() # in km/h
                if (speed > 5):
                    viol_msg = f"Drunken driver\nLocation (lat, long): {pos.latit:#8.4g}, {pos.longit:#8.4g}\n"
                    mqtt.push_data(viol_msg, "violating")
                else:
                    time.sleep(10)
                    main()
            except gps.NoFixException:
                viol_msg = f"Drunken driver\nCannot get fix on location\n"
                mqtt.push_data(viol_msg, "violating")

        
def waiton_all_clear():
    global face0
    face0 = face.wait_face()
    if (alcohol.get() == 1):
        green.clear()
        relay.clear()
        red.set()
        time.sleep(5)
        waiton_all_clear()
    green.set()
    red.clear()
    relay.set()
    return



def main():
    green.blink(20, 1600)
    red.clear()
    relay.clear()
    # time.sleep(10)
    waiton_all_clear()
    


    do_sentry()


if __name__ == "__main__":
    main()
