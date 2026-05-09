from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from tkinter import Tk
import queue

class Visualizer:
    visuals = []

    @staticmethod
    def update_loop(queue_in: queue.Queue):
        while True:
            try:
                next_data: dict = queue_in.get(timeout=1)
                for visual in Visualizer.visuals:
                    visual.update(next_data["time"], next_data[visual.data_key])
            except queue.Empty:
                pass

    def __init__(self, window, data_key, val_min, val_max):
        self.window = window
        self.fig = plt.figure(figsize=(16, 4), dpi=50)
        self.ax = plt.axes()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.data_key = data_key
        self.val_min = val_min
        self.val_max = val_max

        self.ax.set(xlim=(0, 60), ylim=(self.val_min, self.val_max))
        self.ax.set_autoscale_on(False)

        self.time = []
        self.data = []

        Visualizer.visuals.append(self)

    def validate(self, to_check):
        return to_check > self.val_min and to_check < self.val_max 

    def update(self, next_time, next_data):
        if not self.validate(next_data):
            print(f"{self.data_key} -> {next_data}")
            return  

        self.time.append(next_time)
        self.data.append(next_data)

        if len(self.data) > 300:
            self.data.pop(0)
            self.time.pop(0)
        
        self.ax.clear()
        self.ax.plot(self.time, self.data)
        
        self.canvas.draw_idle()