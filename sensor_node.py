import time
import can

SENSOR = "/sys/bus/w1/devices/28-c01f373d6661/temperature"

def read_temp_c():
    with open(SENSOR) as f:
        return int(f.read()) / 1000

bus = can.Bus(interface="socketcan", channel="vcan0")

while True:
    value = int(read_temp_c() * 100)
    data = value.to_bytes(2, "big")
    msg = can.Message(arbitration_id=0x100, data=data, is_extended_id=False)
    bus.send(msg)
    time.sleep(1)
