from scapy.all import ARP, Ether, srp
import socket
import requests


def get_vendor(mac_address):
    """Récupère la marque du constructeur via l'adresse MAC"""
    try:
        # Utilisation d'une API gratuite pour le lookup MAC
        url = f"https://api.macvendors.com/{mac_address}"
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return response.text
        return "Inconnu"
    except:
        return "N/A"


def get_hostname(ip):
    """Tente de récupérer le nom de l'appareil (ex: iPhone-de-Luc)"""
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Nom inconnu"


def scan_network(ip_range):
    print(f"Scan en cours sur {ip_range}...\n")
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        ip = received.psrc
        mac = received.hwsrc

        # Récupération des détails supplémentaires
        brand = get_vendor(mac)
        name = get_hostname(ip)

        devices.append({'ip': ip, 'mac': mac, 'brand': brand, 'name': name})

    return devices


# --- Exécution ---
# On récupère l'IP locale pour déduire le réseau
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0]
s.close()

network_prefix = ".".join(local_ip.split('.')[:-1]) + ".0/24"
devices_list = scan_network(network_prefix)

print(f"{'IP':<15} | {'MAC':<18} | {'MARQUE':<20} | {'NOM'}")
print("-" * 70)

for dev in devices_list:
    print(f"{dev['ip']:<15} | {dev['mac']:<18} | {dev['brand']:<20} | {dev['name']}")

print(f"\nNombre total d'appareils trouvés : **{len(devices_list)}**")