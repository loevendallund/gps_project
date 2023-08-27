from serial import Serial
from pyubx2 import UBXReader, UBXMessage
from threading import Thread
import time
from gpiozero import LED
import redis

# Simple class for managing the ublox gps module, that launches a thread to fetch and update gps information
class GPSModule(Thread):
    streamReader = None
    active = True
    signalFound = False
    led = LED(3)
    redis = None
    pullTime = None

    # Initialize GPSModule
    def __init__(self, redis_inst, portname="/dev/ttyACM0", timeout=2, baudrate=9600, pullTime=2.0, resetCach=True):
        self.redis = redis_inst
        if resetCach == True:
            self.redis.delete("lat")
            self.redis.delete("lng")
        self.pullTime = pullTime
        gps = Serial(portname, timeout=timeout, baudrate=baudrate)
        self.streamReader = UBXReader(gps)
        self.led.blink(on_time=1, off_time=1)
        Thread.__init__(self)
        self.start()

    # Run method from Thread
    def run(self):
        if self.streamReader == None:
            return
        while self.active:
            self.readData()
            if self.signalFound == True:
                time.sleep(self.pullTime)

    # Method for reading data from gps
    def readData(self):
        (_, data) = self.streamReader.read()
        # Checker for data from streamReader, sometimes when running through flask, the data can be NoneType or str
        if data == None or type(data) == str:
            return
        # Only handle for GPRMC, since this NMEA message identity contains latitude and longitude data
        if data.identity == "GPRMC":
            # Check if latitude and longitude contains data, this data is expected to be floating point data
            if type(data.__dict__["lat"]) == float and type(data.__dict__["lon"]) == float:
                # if signalFound is False update it to be true, and set the led to solid (signalFound is used to slowdown pull)
                if self.signalFound == False:
                    self.signalFound = True;
                    self.led.on()
                # set the redis values for latitude and longitude
                self.redis.set("lat", data.__dict__["lat"])
                self.redis.set("lng", data.__dict__["lon"])

# Used to test the GPSModule class without flask
if __name__ == '__main__':
    GPSModule(redis_inst=redis.Redis("localhost"))
