from Collector import Collector
from Visualizer import Visualizer
from tkinter import Tk, Frame, Label
import threading
import queue
from dataclasses import dataclass

@dataclass
class dataType:
    key: str
    label: str
    min: int
    max: int

def main():
    data = [
        dataType(
            "temp",
            "Temprature in °C",
            15,
            30    
        ),
        dataType(
            "humid",
            "Humidity in %",
            25,
            80    
        ),
        dataType(
            "pres",
            "Pressure in hPa ",
            1000,
            1025   
        )
    ]

    root = Tk()
    root.title('Sensor Data Visualizer')
    window = Frame(root, background="white")
    window.pack(fill="both", expand=True)

    for i, d in enumerate(data):
        #Label(window, text=d.label, background="white").grid(column=0, row=i)
        frame = Frame(window)
        frame.grid(column=1, row=i)
        frame.grid_propagate(False)
        Visualizer(frame, d.key, d.min, d.max, d.label)

    sensor = Collector("localhost", 5005)
    
    data_queue = queue.Queue()
    #sensor.connect()
    threading.Thread(target=sensor.read_loop, args=(data_queue,), daemon=True).start()
    threading.Thread(target=Visualizer.update_loop, args=(data_queue,), daemon=True).start()

    window.mainloop()

if __name__ == "__main__":
    main()