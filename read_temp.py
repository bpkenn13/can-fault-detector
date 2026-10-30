import time

SENSOR = "/sys/bus/w1/devices/28-c01f373d6661/temperature"

def read_temp_c():
    with open(SENSOR) as f:
        return int(f.read()) / 1000

while True:
    print(f"{read_temp_c():.2f} C")
    time.sleep(1)
