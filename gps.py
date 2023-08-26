from serial import Serial
from pyubx2 import UBXReader, UBXMessage
from threading import Thread
import time
from gpiozero import LED

class GPSModule(Thread):
    gps = None
    streamReader = None
    lat = None
    lng = None
    active = True
    led = LED(3)

    def __init__(self, portname="/dev/ttyACM0", timeout=2, baudrate=9600):
        self.gps = Serial(portname, timeout=timeout, baudrate=baudrate)
        self.streamReader = UBXReader(self.gps)
        Thread.__init__(self)
        self.start()

    def run(self):
        if self.streamReader == None:
            return
        self.led.blink(on_time=1, off_time=1)
        while self.active:
            self.readData()
            if self.lat != None and self.lng != None:
                self.led.on()
                print("Latitude: " + str(self.lat) + ", Longitude: " + str(self.lng))
                time.sleep(1.0)
            
    def close(self):
        self.active = false
        self.gps.close()

    def readData(self):
        (_, data) = self.streamReader.read()
        if data.identity == "GPRMC":
            if type(data.__dict__["lat"]) == float:
                self.lat = data.__dict__["lat"]
            if type(data.__dict__["lon"]) == float:
                self.lng = data.__dict__["lon"]

module = GPSModule()
#module.Signal()
