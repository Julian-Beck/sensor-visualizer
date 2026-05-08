import socket
import json

class Data:
    def __init__(self, time, temp, humidity, pressure):
        self.time = time
        self.temp = temp
        self.humidity = humidity
        self.pressure = pressure

    def __str__(self):
        return "{" + f"\"time\": {self.time}, \"temp\":{self.temp}, \"humidity\": {self.humidity}, \"pressure\": {self.pressure}" + "}"


class Collector:
    def __init__(self, host="localhost", port=5005):
        self.host = host
        self.port = port
        self.client = socket.socket()

    def connect(self):
        self.client.connect((self.host, self.port))

    def read(self):
        recv_data = self.client.recv(1024).decode('utf-8')

        json_data = json.loads(recv_data)

        return Data(
            json_data["timestamp"],
            json_data["temperatur_C"], 
            json_data["luftfeuchte_pct"], 
            json_data["druck_hPa"]
            )
        
