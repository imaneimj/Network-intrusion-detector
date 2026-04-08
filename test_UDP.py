from scapy.all import IP, UDP, send
import time

dst = "127.0.0.1"

for i in range(200):
    send(IP(dst=dst)/UDP(), verbose=False)
    time.sleep(0.01)

print("UDP flood sent")
