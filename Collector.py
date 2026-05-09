import socket
import json
from datetime import datetime

class Collector:
    def __init__(self, host="localhost", port=5005):
        self.host = host
        self.port = port
        self.client = socket.socket()

    def connect(self):
        self.client.connect((self.host, self.port))

    def read_loop(self, queue_out):
        self.connect()
        while True:
            recv_data = self.client.recv(1024).decode('utf-8')

            json_data = json.loads(recv_data)

            time = datetime.strptime(json_data["timestamp"], "%Y-%m-%dT%H:%M:%S.%f")
            
            data = {
                "time": time,
                "temp": json_data["temperatur_C"], 
                "humidity": json_data["luftfeuchte_pct"], 
                "pressure": json_data["druck_hPa"]
                }
            
            queue_out.put(data)
        
