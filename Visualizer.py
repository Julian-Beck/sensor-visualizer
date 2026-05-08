from matplotlib import pyplot as plt

class Visualizer:
    def __init__(self):
        self.fig = plt.figure() 

        self.axis = plt.axes(xlim =(0, 60),
                        ylim =(0, 50)) 

        self.time = []
        self.data = []
    
    def update(self, new_time, new_data):
        self.time.append(new_time)
        self.data.append(new_data)

        if len(self.data) > 50:
            self.data.pop(0)
            self.time.pop(0)

        self.axis.clear()
        self.axis.plot(self.time, self.data)

        return self.fig
        
    def show(self):    
        plt.show()