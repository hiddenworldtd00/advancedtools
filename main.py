import socket
import requests
import dns.resolver
import dns.reversename
import dns.zone
import dns.query
import whois
import subprocess
import platform
import os
import json
import re
import time
import sys
from bs4 import BeautifulSoup

# Configuration des couleurs
GREEN = '\033[92m'
YELLOW = '\033[93m'
BOLD = '\033[1m'
END = '\033[0m'

LOGO = """
                       .                  ...:=*#%%@@@@@@%%#+=:..                  .                    
                                ..=*%@@@#*=--:::....:::-=+*%@@@%*=..           .                    
         .           .      .-*@@%*=....:-=+*#%%@@@@@%#*+=-:....=*%@@*-.                            
 . .            . .     .:*@@#-...:+%@@@%*=:..     .. ..:=*%@@@@+-...=%@@+:.                        
                     .:#@@=...=@@@#-.....    .      .    .  ....:#@@@=...+@@#.                      
                   .*@@=..-#@@+:.                                  .:=@@#-..=@@+..  .               
     .          .:#@*:.-#@%=..  .              .                      ..-#@#-.:#@#:.  .         .   
              .:%@+..=@@=.                       .                        .=%@+..*@#:. .         .  
            ..%@+..#@%. .                          .                     .   .#@#..*@#..            
         . .*@*..*@*..                    ...::-*%%%#-....                    ..*@#..#@=.        .  
         .:@%:.=@#:..     ... .      ..:-=====@@===%@@@+===-:..       .::.       .#@+.-@%:.         
       ..+@+.:%@-.    .:+@*.     ..:====--==:*@@#=-=@@@%==--===-:..  . .:%@*:.    .:@%:.#@=.        
    . ..#@-.-@#.  ...-@@@:    ..:-==-:..-=-. .+*:=-+@@@+-=-. .:-==-:..    +@@@:...  .*@=.+@+.  .    
    . .%@:.#@-. .=%.%@@#.    .-===:.  .-=-.     .==@@@-..-==:  ..:===-.   .:@@@+:%+...-@#.:@#.      
     .%@..#@:..:@%.%@@=-.  .--=-..   .-=-.      .=%*:.   .:=-.    ..-=-:.  =.+@@+-@%. .:@%.:@#.     
    .%@:.#@: .:@@--@+.++. .-=-:.    .-=-.       .+*. .    .-=-.    ..:-=-...%+:+%:#@%:. :%%.:@#..   
   .*@-.*@:.::*@%:-:#@#..-==-.      :=-.        .==.       .-=-..     .-==:..%@@-.-@@-=- .@#.=@=.   
  .=@= +@- -%.#@*-@@@- .-=======================+@@+=======================-..-@@@=%@=:@- :@*.+@-.  
   :%%.:@*.:%%.#%#@@=:..-==:::::::::-=-::::::::::@@@@-::::::::-=-::::::::::==-..-:%@%@--@%..+@-.%%.  
  +@:.%%..=@%:*@%::%. :=-.        .-=: . .      -##-.    .   .==:.        :-=:.-@-.#@-=@@- .%%.=@=  
 .@*.=@-  *@@-+-:%@= .==:. .      :=-.   .  ...-====-:..     .-=-.        .-==. +@@-::+@@-  -@+.#%. 
.+@-.%%...*@@=.#@@*..-=-.         -=-.    .:%=..+@@*. :%-.    :=-.   .     .-=-..+@@%:*@@-:..%%.-@=.
.%%.:@*.:--@@-%@@-. .-=:         .==:...-#@@@-  :@@-. :@@@#=...-=.         .:=-..::@@@+@%:+:.+@::%#.
:%#.=@- -*.#@#@%:+. :=-.         .=%@@@@@@@@%: .:-*:...#@@@@@@@@@-          .-=: -+.#@#@=.@- :@=.%%.
:@+ *@. +@:.@@#.=%..-=-..........:+@@@@@@@@@@:  .*%.  .%@@@@@@@@@+...........-=: .@+.*@*.*@=  @#.*@:
-@= #%  =@%.-%.*@*  -=============#@@@@@@@@@@-  .#%:  :@@@@@@@@@@@=============-  *@#.*:-@@-  #%.+@:
-@- %%  :@@#..=@@-  -=-..........:@@@@@@@@@@@#. .%@:  +@@@@@@@@@@@=..........-=:. -@@*.:@@%:  #% +@:
-@= #%  .%@@+:@@%.. :=-.        .=@@@@@@@@@@@@+..%@:.-@@@@@@@@@@@@#.. .     .-=:  .%@@-#@@*. .#%.+@:
:@+ *@. ::@@%*@@-=. .-=:.       .#@@@@@@@@@@@@@=:%@--@@@@@@@@@@@@@%:        :=-. -=-@@*@@#.-  %#.*@:
:@#.=@: =::%@#@#.**..-=-.       :@@@@@@@@@@@@@@@@@@%@@@@@@@@@@@@@@@-       .-=-..%*.+@#@*.+= .@+.%%.
.%%.:@+.-@-.*@@-.%%. :==:.      -@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*.     .:==. :@%.-@@:.#@: =@-:%#.
.+@:.%#..%@#.:@:-@@: .-=-.      *@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%.     .-=:. -@@--*.=@@*..#%:-@=.
 :@*.+@:.:@@@+..-@@-:..-=-......%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:.....-=-..:-@@-.-%@@*. :@*.#@. 
  *@:.@#. .%@@@--@@=:#..-=======@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+======-.-%.+@@:*@@@=.  *@:-@=  
  :@#.=@=...-@@@#%@*.#@:.-==:..:@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+ .:==-.=@*.#@#%@@*.=. -@=.%%.  
  .+@-.#%: -*.:%@%%@.=@@:.:==-..-@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*..-==:.=@@-.@@@@=.:%..:%%.=@=.  
   .#@:.%%. =@+..=@@+.@@%...-==-..#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-.-==-..:%@@.#@+..=%@: .#@.-@+.   
    .%%.:@#..:@@@*:.=:+@@=--..-==-.:#@@@@@@@@@@@@@@@@@@@@@@@@@@%-:-==-..+-+@@=:::+@@@*. .#@::@#.    
     .@%.:@#. .+@@@@@=.#@@:+@=..--==-#@@@@@@@@@@@@@@@@@@@@@@@@%-==--..*@=-@@+-#@@@@%.  .#@-.@%.     
      :%%.:%%.  .:@@@@@@=@%.+@@-  .-=%@@@@@@@@@@@@@@@@@@@@@@@@@=-...+@@=:@%#@@@@@=..  .%@::@%.      
      ..%@:.#@-...+.:-#@@@@@:=@@@-  .%@@@@@@@@@@@@@@@@@@@@@@@@@:  =@@@==@@@%+-:.-+. .-@#.-@#..      
   .    .*@=.+@*. .=@#+=:....:.+@@@*-@@@@@@@@@@@@@@@@@@@@@@@@@@+*@@%=..:-=++*#@%-. .*@+.+@+.        
         .-@%..%@=. .-#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*.. .-@%::%@:          
     ..    .#@+.-@%:.   .:*%%%#+-...+@@@@@@@@@@@@@@@@@@@@@@@@@@%....:-==-:... ..:%@-.*@*.           
  .         .:@@-.=@%:. .-%*=::-+#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#**#%%:.  :%@=.=@%:.            
     ..       .-@@=.-%@+....=#@@@@@@@*@@@@@@@@@@@@@@@@@@@@@@@@+*@@@@@@*-.. .+@@=.=@@-.              
                .=%@=.:*@%-.          *@@@@@@@@@@@@@@@@@@@@@@@.        ..-#@#:.+@%-.    .           
     .            .:%@#:.:%@@=..      =@@@@@@@@@@@@@@@@@@@@@@#.     ..-%@%-.-%@#..         ..       
   .               . .-@@%:..*@@@+.   -@@@@@@@@@@@@@@@@@@@@@@+.  .=@@@*..-%@@:.                     
   .                   ..-%@%+..:=%@@%#@@@@@@@@@@@@@@@@@@@@@@%%@@%=:.:*@@#-..          .            
                           .:+%@@#=:..-=*#@@@@@@@@@@@@@@@@#*=-..:+#@@#=:..      . .             .   
          .                     .-*%@@@#+=-::..........::-=*%@@@%*-..     .  .            .         
     .           .                    ..-+#%@@@@@@@@@@@@%*=:..   .  .     .                       ..

"""
TITLE = "                      ▂▃▅▇█▓▒░𝙷𝙰𝙲𝙺𝙴𝚁_𝚃𝙲𝙷𝙰𝙳_𝙰𝙳𝚅𝙰𝙽𝙲𝙴𝙳_𝙽𝙴𝚃𝚆𝙾𝚁𝙺_𝚃𝙾𝙾𝙻𝙺𝙸𝚃░▒▓█▇▅▃▂"


def get_terminal_width():
    try: return os.get_terminal_size().columns
    except: return 80


def print_g(text, bold=False, center=False):
    style = BOLD if bold else ""
    width = get_terminal_width()
    if center:
        for line in text.split('\n'):
            print(f"{GREEN}{style}{line.center(width)}{END}")
    else:
        print(f"{GREEN}{style}{text}{END}")


def print_result_boxed(text):
    """Affiche le résultat en JAUNE à l'intérieur d'un cadre"""
    width = get_terminal_width()
    lines = str(text).split('\n')
    border = f"{YELLOW}+{'-' * (width - 2)}+{END}"
    print(border)
    for line in lines:
        content = line[:width - 4]
        print(f"{YELLOW}| {content.ljust(width - 4)} |{END}")
    print(border)


def slow_logo_print(logo_text):
    """Affiche le logo ligne par ligne sur environ 2 secondes"""
    lines = logo_text.split('\n')
    total_lines = len(lines)
    delay = 2.0 / total_lines if total_lines > 0 else 0
    for line in lines:
        print_g(line, center=True)
        time.sleep(delay)


def train_animation():
    """Animation d'un train qui avance jusqu'à 100%"""
    print()
    for i in range(0, 101, 2):
        time.sleep(0.02)
        bar = "▬" * (i // 4)
        spaces = " " * (25 - (i // 4))
        sys.stdout.write(f"\r{GREEN} [SCAN] {bar} {BOLD}{i}%{END}")
        sys.stdout.flush()
    print("\n")


class AdvancedNetworkTool:
    def __init__(self, target):
        self.target = target
        try: self.ip = socket.gethostbyname(target)
        except: self.ip = None

    def ping_test(self):
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        res = subprocess.run(['ping', param, '3', self.target], capture_output=True, text=True)
        return res.stdout

    def traceroute(self):
        cmd = 'tracert' if platform.system().lower() == 'windows' else 'traceroute'
        res = subprocess.run([cmd, self.target], capture_output=True, text=True)
        return res.stdout

    def dns_lookup(self, rtype='A'):
        try:
            ans = dns.resolver.resolve(self.target, rtype)
            return "\n".join([str(r) for r in ans])
        except: return "Aucun enregistrement."

    def reverse_dns(self):
        try:
            name = dns.reversename.from_address(self.ip)
            return str(dns.resolver.resolve(name, "PTR")[0])
        except: return "Non trouvé."

    def geo_lookup(self):
        try:
            r = requests.get(f"http://ip-api.com/json/{self.ip}").json()
            return json.dumps(r, indent=4)
        except: return "Erreur API."

    def asn_lookup(self):
        try:
            r = requests.get(f"https://ipapi.co/{self.ip}/json/").json()
            return f"ASN: {r.get('asn')} | Org: {r.get('org')}"
        except: return "Indisponible."

    def port_scan(self):
        open_p = []
        ports = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 8080]
        for p in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((self.ip, p)) == 0: open_p.append(p)
            s.close()
        return f"Ports ouverts: {open_p}"

    def http_headers(self):
        try:
            r = requests.get(f"http://{self.target}", timeout=5)
            return "\n".join([f"{k}: {v}" for k, v in r.headers.items()])
        except: return "Erreur HTTP."

    def extract_links(self):
        try:
            r = requests.get(f"http://{self.target}", timeout=5)
            soup = BeautifulSoup(r.text, 'html.parser')
            return "\n".join([a.get('href') for a in soup.find_all('a', href=True)][:15])
        except: return "Erreur d'extraction."

    def reverse_analytics(self):
        try:
            r = requests.get(f"http://{self.target}", timeout=5)
            ua = re.findall(r'UA-\d+-\d+', r.text)
            gas = re.findall(r'G-[A-Z0-9]+', r.text)
            return f"IDs trouvés: {list(set(ua + gas))}"
        except: return "Aucun ID trouvé."

    def zone_transfer(self):
        """Tente un transfert de zone AXFR"""
        try:
            ns_records = dns.resolver.resolve(self.target, 'NS')
            results = []
            for ns in ns_records:
                server = str(ns.target)
                try:
                    zone = dns.zone.from_xfr(dns.query.xfr(server, self.target))
                    results.append(f"AXFR Succès sur {server}")
                    for name, node in zone.nodes.items():
                        results.append(node.to_text(name))
                except:
                    results.append(f"AXFR Échec sur {server}")
            return "\n".join(results)
        except: return "Erreur lors de la récupération des NS ou AXFR impossible."


def menu():
    os.system('cls' if platform.system().lower() == 'windows' else 'clear')
    slow_logo_print(LOGO)
    print_g(TITLE, bold=True, center=True)
    print("\n")
    target = input(f"{GREEN} [>] ENTRER CIBLE : {END}").strip()
    if not target: return
    tool = AdvancedNetworkTool(target)

    options = {
        "1": tool.ping_test, "2": tool.traceroute, "3": lambda: tool.dns_lookup('A'),
        "4": lambda: f"MX:\n{tool.dns_lookup('MX')}\nNS:\n{tool.dns_lookup('NS')}\nTXT:\n{tool.dns_lookup('TXT')}",
        "5": tool.reverse_dns, "6": lambda: str(whois.whois(target)), "7": tool.geo_lookup,
        "8": tool.asn_lookup, "9": tool.port_scan, "10": tool.http_headers,
        "11": tool.extract_links, "12": tool.reverse_analytics, "13": tool.zone_transfer, "0": None
    }

    menu_text = [
        "1. Test Ping", "2. Traceroute", "3. DNS Lookup (A)", "4. Records MX/NS/TXT",
        "5. Reverse DNS", "6. Whois Lookup", "7. IP Geolocation", "8. ASN Lookup",
        "9. TCP Port Scan", "10. HTTP Headers", "11. Extract Links", "12. Analytics Search",
        "13. Zone Transfer (AXFR)", "0. Quitter"
    ]

    while True:
        print_g("\n--- MENU DES OUTILS ---", bold=True)
        for line in menu_text: print_g(line)
        choice = input(f"\n{GREEN} [?] CHOISIR UN NUMÉRO : {END}")
        if choice == '0': break
        if choice in options:
            train_animation()
            print_result_boxed(options[choice]())
        else:
            print_g("Choix invalide.")


if __name__ == "__main__":
    menu()