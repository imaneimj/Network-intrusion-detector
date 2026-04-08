from scapy.all import IP, TCP, send
import time
import random

dst = "127.0.0.1"

for i in range(200):
    sport = random.randint(1024, 65535)
    dport = random.randint(1, 1000)

    send(IP(dst=dst)/TCP(sport=sport, dport=dport, flags="S"), verbose=False)
    time.sleep(0.01)

print("SYN flood sent")
