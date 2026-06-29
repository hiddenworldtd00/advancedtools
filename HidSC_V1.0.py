import os
import sys
import psutil
import platform
import subprocess
from colorama import Fore, Style, init

# Initialisation
init(autoreset=True)

class HidSC_V1:
    def __init__(self):
        self.yellow = Fore.YELLOW
        self.cyan = Fore.CYAN
        self.green = Fore.GREEN
        self.red = Fore.RED
        self.white = Fore.WHITE
        self.bold = Style.BRIGHT

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def banner(self):
        self.clear()
        print(f"{self.cyan}{self.bold}")
        print(r"  ██╗  ██╗██╗██████╗ ███████╗ ██████╗    ██╗   ██╗ ██╗      ██████╗ ")
        print(r"  ██║  ██║██║██╔══██╗██╔════╝██╔════╝    ██║   ██║███║     ██╔═████╗")
        print(r"  ███████║██║██║  ██║███████╗██║         ██║   ██║╚██║     ██║██╔██║")
        print(r"  ██╔══██║██║██║  ██║╚════██║██║         ╚██╗ ██╔╝ ██║     ████╔╝██║")
        print(r"  ██║  ██║██║██████╔╝███████║╚██████╗     ╚████╔╝  ██║     ╚██████╔╝")
        print(r"  ╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝ ╚═════╝ ████ ╚═══╝   ╚═╝  ██  ╚═════╝ ")
        print(f"\n{self.yellow}{' ' * 25}[HidSC_V1.0]{self.white}")
        print(f"{self.cyan}{'=' * 70}\n")

    def draw_box(self, lines):
        """Encadre le résultat en jaune"""
        if not lines: return
        max_l = max(len(str(line)) for line in lines)
        width = max_l + 4
        print(f"{self.yellow}╔{'═' * width}╗")
        for line in lines:
            print(f"{self.yellow}║  {self.white}{line:<{max_l}}  {self.yellow}║")
        print(f"{self.yellow}╚{'═' * width}╝")

    def get_drives(self):
        """Détecte tous les disques durs du PC"""
        drives = [d.device for d in psutil.disk_partitions() if 'fixed' in d.opts or 'cdrom' not in d.opts]
        return drives

    def progress(self, current, total, text="Scan"):
        length = 40
        percent = int((current / total) * 100)
        filled = int(length * current // total)
        bar = '█' * filled + '-' * (length - filled)
        sys.stdout.write(f'\r{self.white}{text}: {self.yellow}[{self.cyan}{bar}{self.yellow}] {percent}%')
        sys.stdout.flush()

    # --- OPTION 1 : SCAN COMPLET DU PC ---
    def full_system_scan(self):
        self.banner()
        print(f"{self.cyan}[*] Initialisation du scan complet de l'ordinateur...")
        drives = self.get_drives()
        print(f"{self.cyan}[*] Disques détectés : {', '.join(drives)}")

        suspicious_files = []

        for drive in drives:
            try:
                subdirs = [os.path.join(drive, d) for d in os.listdir(drive) if os.path.isdir(os.path.join(drive, d))]
            except:
                continue

            for i, path in enumerate(subdirs):
                self.progress(i + 1, len(subdirs), f"Scan {drive}")
                try:
                    for root, _, files in os.walk(path):
                        for f in files:
                            if f.lower().endswith(('.exe', '.apk', '.bat', '.vbs')):
                                if f.count('.') > 1:
                                    suspicious_files.append(f"MENACE : {f} | LIEU : {root}")
                except:
                    continue

        print("\n")
        if suspicious_files:
            self.draw_box(["OBJETS SUSPECTS DÉTECTÉS :"] + suspicious_files[:10])
        else:
            self.draw_box(["SCAN TERMINÉ : AUCUNE MENACE DÉTECTÉE SUR LE SYSTÈME"])

    # --- OPTION 2 : RECHERCHE DE FICHIER ---
    def find_file(self):
        self.banner()
        print(f"{self.yellow}>>> Entrez le nom du fichier ou l'extension à localiser :")
        query = input(f"{self.cyan}Input > {self.white}").strip().lower()

        if not query: return

        print(f"{self.cyan}[*] Recherche de '{query}' sur tous les disques...")
        matches = []
        drives = self.get_drives()

        for drive in drives:
            try:
                items = os.listdir(drive)
                for i, item in enumerate(items):
                    self.progress(i + 1, len(items), f"Recherche {drive}")
                    p = os.path.join(drive, item)
                    if os.path.isdir(p):
                        for root, _, files in os.walk(p):
                            for f in files:
                                if query in f.lower():
                                    matches.append(os.path.join(root, f))
                                    if len(matches) > 10: break
            except:
                continue

        print("\n")
        if matches:
            self.draw_box([f"FICHIERS TROUVÉS ({len(matches)}) :"] + matches[:8])
            print(f"\n{self.green}[✓] Voulez-vous ouvrir le premier emplacement ? (y/n)")
            ans = input("> ")
            if ans.lower() == 'y':
                subprocess.run(['explorer', '/select,', os.path.normpath(matches[0])])
        else:
            self.draw_box(["AUCUN FICHIER CORRESPONDANT TROUVÉ"])

    def menu(self):
        while True:
            self.banner()
            print(f"{self.white}1. SCAN COMPLET DU PC (Sécurité)")
            print(f"{self.white}2. LOCALISER UN FICHIER (Recherche)")
            print(f"{self.white}3. QUITTER")

            choice = input(f"\n{self.cyan}[HidSC_V1.0] #> {self.white}")

            if choice == '1':
                self.full_system_scan()
                input("\nAppuyez sur Entrée pour revenir...")
            elif choice == '2':
                self.find_file()
                input("\nAppuyez sur Entrée pour revenir...")
            elif choice == '3':
                print(f"{self.red}Fermeture de la session...")
                break

if __name__ == "__main__":
    app = HidSC_V1()
    app.menu()