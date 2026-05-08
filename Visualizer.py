from matplotlib import pyplot as plt
from Collector import Data
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from tkinter import Tk
import queue

class Visualizer:
    def __init__(self, queue_in: queue.Queue, window, val_min, val_max):
        self.window = window
        self.canvas = None
        self.fig = plt.figure()
        self.ax = plt.axes()
        self.ax.set(xlim=(30, 60), ylim=(0,50))
        self.ax.set_autoscale_on(False)

        self.queue_in = queue_in
        self.val_min = val_min
        self.val_max = val_max

        self.time = []
        self.data = []

    def validate(self, to_check):
        return to_check > self.val_min and to_check < self.val_max 

    def update_loop(self):
        if self.canvas is None:
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
            self.canvas.get_tk_widget().pack(fill='both', expand=True)
        while True:
            try:
                next_data: Data = self.queue_in.get(timeout=1)

                if not self.validate(next_data.temp):
                    continue
                
                self.time.append(next_data.time)
                self.data.append(next_data.temp)

                if len(self.data) > 300:
                    self.data.pop(0)
                    self.time.pop(0)
                
                self.ax.clear()
                self.ax.plot(self.time, self.data)
                
                self.canvas.draw_idle()
            except queue.Empty:
                pass