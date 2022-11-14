import serial
from io import TextIOWrapper, BufferedRWPair as tty
from time import time
import string
import pynmea2 as nmea
import sys
# use serial
port = "/dev/serial0"
rw = serial.Serial(port, baudrate=9600, timeout=0.5)
gps_tty = TextIOWrapper(tty(rw, rw))
data: nmea.NMEASentence

class NoFixException(Exception):
    def what(self, e: str):
        return "Could not obtain GPS data: " + e + "\n"

# configure chip
# first log current setup
gps_tty.write(str(nmea.ubx.UBX('UBX', ('', '40'))))
print("Initialising NEO-6M...")
print("Current NEO-6M setup:\n" + str(gps_tty.readline()))

# filtering only GGA, GLL, VTG, GSV sentences
gps_tty.write(str(nmea.ubx.UBX('UBX', ('','40', 'GGA', '0', '1', '1', '0', '0', '0'))))
gps_tty.write(str(nmea.ubx.UBX('UBX', ('','40', 'VTG', '0', '1', '1', '0', '0', '0'))))
gps_tty.write(str(nmea.ubx.UBX('UBX', ('','40', 'GSV', '0', '1', '1', '0', '0', '0'))))
gps_tty.write(str(nmea.ubx.UBX('UBX', ('','40', 'GLL', '0', '1', '1', '0', '0', '0'))))
gps_tty.write(str(nmea.ubx.UBX('UBX', ('','40', 'DTM', '0', '0', '0', '0', '0', '0'))))
gps_tty.write(str(nmea.ubx.UBX('UBX', ('','40', 'GBS', '0', '0', '0', '0', '0', '0'))))
gps_tty.write(str(nmea.ubx.UBX('UBX', ('','40', 'GPQ', '0', '0', '0', '0', '0', '0'))))
gps_tty.write(str(nmea.ubx.UBX('UBX', ('','40', 'GRS', '0', '0', '0', '0', '0', '0'))))
gps_tty.write(str(nmea.ubx.UBX('UBX', ('','40', 'GSA', '0', '0', '0', '0', '0', '0'))))
gps_tty.write(str(nmea.ubx.UBX('UBX', ('','40', 'GST', '0', '0', '0', '0', '0', '0'))))
gps_tty.write(str(nmea.ubx.UBX('UBX', ('','40', 'RMC', '0', '0', '0', '0', '0', '0'))))
gps_tty.write(str(nmea.ubx.UBX('UBX', ('','40', 'TXT', '0', '0', '0', '0', '0', '0'))))
gps_tty.write(str(nmea.ubx.UBX('UBX', ('','40', 'ZDA', '0', '0', '0', '0', '0', '0'))))

class fix:
    lat: int = 0
    lng: int = 0

    
    def __init__(self, lat: int, lng: int) -> None:
        self.lat  = lat
        self.lng = lng
    

def get_loc() -> fix:
    global data
    start = time()
    while True:
        if (time() - start > 15):
            raise NoFixException()
        try:
            data = nmea.parse(gps_tty.readline())
        except Exception as e:
            print(f"Error: Dropping GPS sentence:\n{e}", file=sys.stderr)
        if (type(data) == nmea.GLL):
            lat = data.latitude
            lon = data.longitude
            return fix(lat, lon)

def get_speed() -> int:
    global data
    start = time()
    while True:
        if (time() - start > 15):
            raise NoFixException()
        try:
            data = nmea.parse(gps_tty.readline())
        except Exception as e:
            print(f"Error: Dropping GPS sentence:\n{e}", file=sys.stderr)
        if (type(data) == nmea.VTG):
            if data.spd_over_grnd_kmph is None:
                raise NoFixException()
            return data.spd_over_grnd_kmph
