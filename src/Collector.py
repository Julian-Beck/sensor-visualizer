import socket
import json
from datetime import datetime
import time

class Collector:
    def __init__(self, host="localhost", port=5005):
        self.host = host
        self.port = port
        self.client = socket.socket()

    def connect(self):
        while True:
            try:
                self.client.connect((self.host, self.port))
                return
            except:
                print(f"Connection to {self.host}:{self.port} failed! Next try in 5s")
                time.sleep(5)

    
    def disconnect(self):
        self.client.close()

    def read_loop(self, queue_out):
        while True:
            recv_data = self.client.recv(1024).decode('utf-8')

            json_data = json.loads(recv_data)

            time = datetime.strptime(json_data["timestamp"], "%Y-%m-%dT%H:%M:%S.%f")
            
            data = {
                "time": time,
                "temp": json_data["temperatur_C"], 
                "humid": json_data["luftfeuchte_pct"], 
                "pres": json_data["druck_hPa"]
                }
            
            queue_out.put(data)
    