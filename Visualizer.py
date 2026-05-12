from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import queue
import datetime

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

    def __init__(self, window, data_key, val_min, val_max, label):
        self.window = window
        self.fig = plt.figure(figsize=(24, 6), dpi=50)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.label = label
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
            print(f"Invalid reading: {self.data_key} -> {next_data}")
            return  

        self.time.append(next_time)
        self.data.append(next_data)

        if len(self.data) > 150:
            self.data.pop(0)
            self.time.pop(0)

        self.ax.clear()
        self.ax.plot(list(self.time), list(self.data))
        self.ax.set_xlabel('Time', fontsize=18)
        self.ax.set_ylabel(self.label, fontsize=18)
        self.ax.tick_params(axis='both', which='major', labelsize=18)
        self.ax.set_ylim(self.val_min, self.val_max) 
        self.ax.set_xlim(min(self.time) if self.time else 0, 
            min(self.time) + datetime.timedelta(seconds=30) if self.time else 1)
        self.canvas.draw()