from Collector import Collector, Data
from Visualizer import Visualizer
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from tkinter import Tk
import threading
import queue


def main():
    window = Tk()
    window.title('Embedded plot')
    window.geometry()
    
    temp_data_queue = queue.Queue()
    temp_visual = Visualizer(temp_data_queue, window, 12, 35)

    sensor = Collector("localhost", 5005)
    sensor.connect()
    
    threading.Thread(target=sensor.read_loop, args=(temp_data_queue,), daemon=True).start()
    threading.Thread(target=temp_visual.update_loop, daemon=True).start()
    window.mainloop()

if __name__ == "__main__":
    main()