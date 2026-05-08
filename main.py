from Collector import Collector, Data
from Visualizer import Visualizer

def main():
    temp_visual = Visualizer()

    sensor = Collector("localhost", 5005)
    sensor.connect()
    
    i = 0
    while (i < 50):
        data: Data = sensor.read()

        temp_visual.update(data.time, data.temp)
        i+=1

        
        print(data)
    temp_visual.show()

if __name__ == "__main__":
    main()