import can
import statistics

bus = can.Bus(interface="socketcan", channel="vcan0")

baseline = []
BASELINE_SIZE = 30
mean = ucl = lcl = None
recent = []

while True:
    msg = bus.recv(timeout=3)
    if msg is None:
        print("FAULT: timeout - sensor not responding")
        continue
    if msg.arbitration_id != 0x100:
        continue

    temp = int.from_bytes(msg.data, "big") / 100

    if len(baseline) < BASELINE_SIZE:
        baseline.append(temp)
        print(f"{temp:.2f} C  (learning normal {len(baseline)}/{BASELINE_SIZE})")
        if len(baseline) == BASELINE_SIZE:
            mean = statistics.mean(baseline)
            sigma = max(statistics.stdev(baseline), 0.1)
            ucl = mean + 3 * sigma
            lcl = mean - 3 * sigma
            print(f"Limits set: mean {mean:.2f}, UCL {ucl:.2f}, LCL {lcl:.2f}")
        continue

    recent.append(temp)
    if len(recent) > 7:
        recent.pop(0)

    rising = len(recent) == 7 and all(recent[i] < recent[i + 1] for i in range(6))
    falling = len(recent) == 7 and all(recent[i] > recent[i + 1] for i in range(6))

    if temp > ucl or temp < lcl:
        print(f"{temp:.2f} C  FAULT: out of control")
    elif rising or falling:
        print(f"{temp:.2f} C  WARNING: drift")
    else:
        print(f"{temp:.2f} C  OK")
