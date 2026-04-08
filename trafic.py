# trafic.py
from scapy.all import sniff, TCP, IP, ICMP, UDP
from collections import defaultdict, deque
import time
import logging
import threading

# --- Configuration ---
WINDOW_SECOND = 10
SYN_THRESHOLD = 50
ICMP_THRESHOLD = 100
UDP_THRESHOLD = 100
BLACKLIST = "blacklist.txt"

# --- Structures pour suivi des paquets ---
syn_times = defaultdict(deque)
icmp_times = defaultdict(deque)
udp_times = defaultdict(deque)

running = False
sniffer_thread = None
iface_used = None

# --- Logging ---
logging.basicConfig(
    filename="alerts.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Charger blacklist ---
def load_blacklist(path):
    try:
        with open(path, "r") as f:
            return set(l.strip() for l in f if l.strip() and not l.startswith("#"))
    except FileNotFoundError:
        print(f"[INFO] File {path} not found, continuing without blacklist")
        return set()

blacklist = load_blacklist(BLACKLIST)

# --- Dérouler deque ---
def update_deque(dq, now):
    while dq and now - dq[0] > WINDOW_SECOND:
        dq.popleft()
    return len(dq)

# --- Détection paquets ---
def detect(pkt):
    if not pkt.haslayer(IP):
        return

    src = pkt[IP].src
    now = time.time()

    # --- Blacklist ---
    if src in blacklist:
        msg = f"[ALERTE] IP blacklistée: {src}"
        print(msg)
        logging.warning(msg)

    # --- SYN Scan ---
    if pkt.haslayer(TCP):
        tcp = pkt[TCP]
        if tcp.flags & 0x02:  # SYN
            dq = syn_times[src]
            dq.append(now)
            if update_deque(dq, now) > SYN_THRESHOLD:
                msg = f"[ALERTE] SYN scan détecté depuis {src}"
                print(msg)
                logging.warning(msg)

    # --- ICMP Flood ---
    if pkt.haslayer(ICMP):
        dq = icmp_times[src]
        dq.append(now)
        if update_deque(dq, now) > ICMP_THRESHOLD:
            msg = f"[ALERTE] ICMP flood depuis {src}"
            print(msg)
            logging.warning(msg)

    # --- UDP Flood ---
    if pkt.haslayer(UDP):
        dq = udp_times[src]
        dq.append(now)
        if update_deque(dq, now) > UDP_THRESHOLD:
            msg = f"[ALERTE] UDP flood depuis {src}"
            print(msg)
            logging.warning(msg)

# --- Boucle sniffing ---
def sniff_loop(interface):
    sniff(prn=detect, store=False, iface=interface)

# --- Démarrer sniffer ---
def start_sniffer(interface="lo"):
    global running, sniffer_thread, iface_used

    if running:
        return False, "Sniffer déjà en cours"

    running = True
    iface_used = interface
    sniffer_thread = threading.Thread(target=sniff_loop, args=(interface,), daemon=True)
    sniffer_thread.start()

    return True, f"Sniffer démarré sur {interface}"

# --- Arrêter sniffer ---
def stop_sniffer():
    global running
    if not running:
        return False, "Sniffer déjà arrêté"

    running = False
    return True, "Sniffer arrêté"

# --- Statut sniffer ---
def sniffer_status():
    return {"running": running, "iface": iface_used}

# --- Pour test standalone ---
if __name__ == "__main__":
    print("Démarrage sniffer SYN/ICMP/UDP sur 'lo'...")
    start_sniffer("lo")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_sniffer()
        print("Sniffer arrêté")
