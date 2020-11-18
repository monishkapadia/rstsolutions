import subprocess
import requests
from requests.auth import HTTPBasicAuth
import json


class DataUpload:
    def __init__(self):
        self.DEVICE_IP = subprocess.check_output(
            "hostname -I", shell=True).decode('utf-8').split(" ")[0]
        f = open('../config.txt', 'r')
        d = f.readlines()
        # Azure IoT Hub
        self.URI = 'temp-data.azure-devices.net'
        self.IOT_DEVICE_ID = d[1].strip('\n')
        self.SAS_TOKEN = d[4].strip('\n')

        # JD Edwards API
        self.JDEDWARDS_API_URL = 'https://50.243.34.141:10145/jderest/v3/orchestrator/IoTDeviceTelemetry?'
        self.JDEDWARDS_USER = d[2].strip('\n')
        self.JDEDWARDS_PASS = d[3].strip('\n')
        self.DEVICE_NUMBER = int(d[0])
        f.close()

    def send_mongo_db(self, message):
        try:
            url = 'https://rst-web.herokuapp.com/data/add'
            # url = 'http://10.0.0.252:5000/data/add'
            headers = {
                "Content-Type": "application/json",
            }
            data = json.dumps(message)
            print(data)
            response = requests.post(url, data=data, headers=headers)
            print("Data sent to DB")
        except:
            print("Connection error with DB")

    def send_message_azure(self, message):
        try:
            url = 'https://{0}/devices/{1}/messages/events?api-version=2016-11-14'.format(
                self.URI, self.IOT_DEVICE_ID)
            headers = {
                "Content-Type": "application/json",
                "Authorization": self.SAS_TOKEN
            }
            data = json.dumps(message)
            print(data)
            response = requests.post(url, data=data, headers=headers)
            print("Data sent to Azure")
        except:
            print("Connection error with Azure")

    def send_message_jdedwards(self, message):
        try:
            PARAMS = {
                'DeviceNumber': message["DeviceNumber"],
                'IOTUniversalID': message["UUID"],
                'IPAddress': message["IPAddress"],
                'Temperature': message["temp"],
                'TemperatureUM': message["temp_unit"],
                'Weight': '0',
                'WeightUM': 'kg',
                'Latitude': message["lat"],
                'Longitude': message["lon"],
                'Precipitation': '0',
                'PrecipitationUM': 'A',
                'Humidity': message["humidity"],
                'HumidityUM': message["humidity_unit"]
            }
            response = requests.get(url=self.JDEDWARDS_API_URL, params=PARAMS, verify=False,
                                    auth=HTTPBasicAuth(self.JDEDWARDS_USER, self.JDEDWARDS_PASS))
            print("Data sent to JD Edwards")
        except Exception as e:
            print(e)
            print("Connection error with JD Edwards")
