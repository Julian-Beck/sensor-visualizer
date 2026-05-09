from Collector import Collector
from Visualizer import Visualizer
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from tkinter import Tk, Frame, Scrollbar, Label
import threading
import queue



def main():

    root = Tk()
    root.title('Sensor Data Visualizer')
    window = Frame(root, background="white")
    window.pack(fill="both", expand=True)

    temp_frame = Frame(window)
    humidity_frame = Frame(window)
    pressure_frame = Frame(window)

    label_texts = ["Temprature in °C", "Humidity", "Pressure"]

    for i, text in enumerate(label_texts):
        Label(window, text=text, background="white").grid(column=0, row=i)

    temp_frame.grid(column=1, row=0)
    humidity_frame.grid(column=1, row=1)
    pressure_frame.grid(column=1, row=2)
    temp_frame.grid_propagate(False)


    Visualizer(temp_frame, "temp", 15, 35)
    Visualizer(humidity_frame, "humidity", 25, 80)
    Visualizer(pressure_frame, "pressure", 1000, 1025)

    sensor = Collector("localhost", 5005)
    
    data_queue = queue.Queue()
    #sensor.connect()
    threading.Thread(target=sensor.read_loop, args=(data_queue,), daemon=True).start()
    threading.Thread(target=Visualizer.update_loop, args=(data_queue,), daemon=True).start()
    
    window.mainloop()

if __name__ == "__main__":
    main()