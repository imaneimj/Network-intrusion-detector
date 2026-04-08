# Network-intrusion-detector
Un mini-projet IDS (Intrusion Detection System) en Python utilisant **Scapy** et **Flask** pour détecter les attaques réseau en temps réel : SYN scan, flood ICMP et UDP.

## Fonctionnalités

- Détection de **SYN scan** sur TCP.
- Détection de **flood ICMP** et **UDP**.
- Gestion d'une **blacklist IP**.
- Dashboard web avec :
  - Boutons **Start Detection** / **Stop Detection**
  - Affichage des **alertes en temps réel**
  - Interface colorée et centrée.


## Prérequis

- Python version 3.10 ou supérieure  
- Modules Python : `scapy` et `flask`  
- Système Linux ou WSL pour pouvoir capturer le trafic réseau  
- Droits root ou administrateur pour le sniffing réseau avec Scapy  
  
Structure du projet
IDS/
├─ app.py               # Dashboard Flask
├─trafic.py             # Module IDS
├─templates/
│   └─ index.html       # Template dashboard
├─static/
│   ├─ style.css        # Styles CSS
│   └─ script.js        # JS pour refresh automatique
├─alerts.log            # Log des alertes
└─blacklist.txt         # IP blacklist 
