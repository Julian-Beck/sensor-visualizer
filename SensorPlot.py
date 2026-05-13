from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import tkinter as tk
from tkinter import Label, StringVar
import queue
import datetime

class SensorPlot:
    plots = []

    @staticmethod
    def update_loop(queue_in: queue.Queue):
        while True:
            try:
                next_data: dict = queue_in.get(timeout=1)
                for plot in SensorPlot.plots:
                    plot.update(next_data["time"], next_data[plot.data_type.key])
            except queue.Empty:
                pass

    def __init__(self, window, data_type, scale_facor):
        self.window = window
        self.data_type = data_type
        self.fig = plt.figure(figsize=(48*scale_facor, 8*scale_facor), dpi=50)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.avg = StringVar()
        self.avg.set(f"Average: 0{self.data_type.unit}")
        self.label_avg = Label(self.window, textvariable=self.avg, background="white", borderwidth=1, font=("arial", 15))
        self.label_avg.pack()

        self.ax.set(xlim=(0, 60), ylim=(self.data_type.min, self.data_type.max))
        self.ax.set_autoscale_on(False)

        self.time = []
        self.data = []

        SensorPlot.plots.append(self)

    def validate(self, to_check):
        return to_check > self.data_type.min and to_check < self.data_type.max 
    
    def calc_avg(self, data):
        if not data: return 0
        
        data_sum = 0
        for i in data:
            if i!=None: data_sum+=i

        avg = data_sum/len(data)
        return round(avg, 2)

    def update(self, next_time, next_data):
        self.time.append(next_time)
        
        ### Validierung der Messwerte über abgleich des festgelegten Bereiches
        ### Bei Ausreißern, wird die letzte Messung gekopiert
        if not self.validate(next_data):
            print(f"Invalid reading: {self.data_type.key} -> {next_data}")
            if self.data: self.data.append(self.data[-1])
            else: self.data.append(None)
        else:
            self.data.append(next_data)

        ### Es werden nur 150 Datensätze gleichzeitig gespeichert,
        ### da 5 Messungen/Sekunde * 30 Sekunden = 150 Messungen
        if len(self.data) > 150:
            self.data.pop(0)
            self.time.pop(0)

        self.ax.clear()
        self.ax.plot(list(self.time), list(self.data))
        self.ax.set_ylabel(f"{self.data_type.label} in {self.data_type.unit}", fontsize=32)
        self.ax.tick_params(axis='both', which='major', labelsize=24)

        ### Hier wird die x-Achse auf den Bereich der validen Werte festgesetzt
        self.ax.set_ylim(self.data_type.min, self.data_type.max) 
        ### Hier wird die y-Achse auf den Zeitraum der letzten 30 Sekunden festgesetzt
        # (exakt: von der ältesten Messung 30 Sekunden in die Zukunft)
        self.ax.set_xlim(min(self.time) if self.time else 0, 
            min(self.time) + datetime.timedelta(seconds=30) if self.time else 1)
        
        self.canvas.draw()
        self.avg.set(f"Average {self.data_type.label} (last 30s): {self.calc_avg(self.data)} {self.data_type.unit}")