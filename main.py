from Collector import Collector, Data

def main():
    sensor = Collector("localhost", 5005)
    sensor.connect()

    while (True):
        data: Data = sensor.read()

        print(data)


if __name__ == "__main__":
    main()