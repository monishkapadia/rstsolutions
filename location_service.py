import serial
import requests
import json


class GPS:
    def __init__(self):
        self.SERIAL_PORT = "/dev/serial0"
        self.gps = serial.Serial(self.SERIAL_PORT, baudrate=9600, timeout=0.5)
        self.running = True
        self.count = 10

    def getLatLng(self, latString, lonString, latDir, lonDir):
        self.lat = float(latString[:2].lstrip(
            '0') + "." + "%.7s" % str(float(latString[2:])*1.0/60.0).lstrip("0."))
        self.lon = float(lonString[:3].lstrip(
            '0') + "." + "%.7s" % str(float(lonString[3:])*1.0/60.0).lstrip("0."))
        if(latDir == 'S'):
            self.lat = -self.lat
        if(lonDir == 'W'):
            self.lon = -self.lon

    def getData(self):
        self.__init__()
        while self.running and self.count:
            try:
                data = self.gps.readline().decode('utf-8')
                data = data.split(",")
                if (data[0] == '$GPRMC'):
                    self.getLatLng(
                        data[3], data[5], data[4], data[6])
                    self.running = False
                    self.gps.close()
                    return (self.lat, self.lon)
                self.count = self.count - 1
            except Exception as e:
                print(e)
        self.gps.close()

    def getLocation(self, lat, lon):
        response = requests.get(
            'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={}&lon={}'.format(lat, lon))
        response = json.loads(response.content.decode('utf-8'))
        return(response['display_name'])
