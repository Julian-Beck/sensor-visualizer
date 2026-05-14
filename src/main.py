from Collector import Collector
from SensorPlot import SensorPlot
from tkinter import Tk, Frame
import tkinter as tk
import threading
import queue
from dataclasses import dataclass

SCALE_FACTOR = 1

@dataclass
class DataType:
    key: str
    label: str
    unit: str
    min: int
    max: int

def main():
    sensor_datatypes = [
        DataType(
            "temp",
            "Temperature",
            "°C",
            15,
            30    
        ),
        DataType(
            "humid",
            "Humidity",
            "%",
            25,
            80    
        ),
        DataType(
            "pres",
            "Pressure",
            "hPa ",
            1000,
            1025   
        )
    ]

    root = Tk()
    root.title('Sensor Data Visualizer')

    width= root.winfo_screenwidth() 
    height= root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height))
    print(f"{width}, {height}")
    window = Frame(root, background="white")
    window.pack(fill=tk.BOTH, expand=True)

    for i, datatype in enumerate(sensor_datatypes):
        frame = Frame(window, background="white")
        frame.grid(column=1, row=i)
        SensorPlot(frame, datatype, SCALE_FACTOR)

    sensor = Collector("localhost", 5005)
    data_queue = queue.Queue()
    
    sensor.connect()
    threading.Thread(target=sensor.read_loop, args=(data_queue,), daemon=True).start()
    threading.Thread(target=SensorPlot.update_loop, args=(data_queue,), daemon=True).start()

    window.mainloop()

if __name__ == "__main__":
    main()