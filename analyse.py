import os
import hashlib
import math
import psutil
import time
from datetime import datetime


# Configuration des couleurs pour le terminal
class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Color.CYAN}{'=' * 60}{Color.END}")
    print(f"{Color.BOLD}{Color.BLUE}       🛡️  SENTINEL ADVANCED SECURITY SYSTEM v1.0 🛡️{Color.END}")
    print(f"{Color.CYAN}{'=' * 60}{Color.END}")


class SecurityTools:
    @staticmethod
    def calculate_entropy(path):
        """Détecte si un fichier est crypté/packé (typique des malwares)."""
        try:
            with open(path, "rb") as f:
                data = f.read()
            if not data: return 0
            entropy = 0
            for x in range(256):
                p_x = float(data.count(x)) / len(data)
                if p_x > 0:
                    entropy += - p_x * math.log(p_x, 2)
            return entropy
        except:
            return 0

    def scan_file(self, file_path):
        """Analyse complète d'un fichier spécifique."""
        print(f"\n{Color.BOLD}Analyse de :{Color.END} {file_path}")
        score = 0
        details = []

        # 1. Vérification double extension (ex: photo.jpg.exe)
        if file_path.count('.') > 1:
            score += 30
            details.append("Suspicion : Double extension détectée.")

        # 2. Analyse de l'entropie
        entropy = self.calculate_entropy(file_path)
        if entropy > 7.5:
            score += 40
            details.append(f"Alerte : Entropie très élevée ({entropy:.2f}) - Fichier probablement crypté.")

        # 3. Vérification de la taille
        size = os.path.getsize(file_path) / (1024 * 1024)
        if size < 0.1 and file_path.endswith('.exe'):
            score += 10
            details.append("Note : Fichier exécutable anormalement petit.")

        # Affichage du résultat
        if score >= 50:
            print(f"{Color.RED}[!] VERDICT : DANGEREUX ({score}/100){Color.END}")
            for d in details: print(f"  - {d}")
        elif score >= 20:
            print(f"{Color.YELLOW}[?] VERDICT : SUSPECT ({score}/100){Color.END}")
            for d in details: print(f"  - {d}")
        else:
            print(f"{Color.GREEN}[✓] VERDICT : SAIN (Aucune menace évidente){Color.END}")

    def scan_processes(self):
        """Analyse les programmes qui tournent actuellement en mémoire."""
        print(f"\n{Color.BOLD}--- Analyse des Processus Actifs ---{Color.END}\n")
        suspicious_found = False
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                # On cherche des processus sans chemin d'accès ou dans Temp
                exe_path = proc.info['exe']
                if exe_path:
                    if "Temp" in exe_path or "AppData\\Local" in exe_path:
                        print(
                            f"{Color.RED}[!] Suspect : {proc.info['name']} (PID: {proc.info['pid']}) tourne depuis un dossier temporaire !{Color.END}")
                        print(f"    Chemin : {exe_path}")
                        suspicious_found = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if not suspicious_found:
            print(f"{Color.GREEN}[✓] Aucun processus malveillant détecté en mémoire.{Color.END}")


def main():
    scanner = SecurityTools()

    while True:
        print_header()
        print(f"{Color.BOLD}Choisissez un outil :{Color.END}")
        print(f"1. {Color.YELLOW}Analyse de Dossier / Fichier{Color.END}")
        print(f"2. {Color.YELLOW}Analyse des Processus Système (RAM){Color.END}")
        print(f"3. {Color.YELLOW}Scan Rapide des zones d'infection (Temp/Downloads){Color.END}")
        print(f"4. {Color.RED}Quitter{Color.END}")

        choice = input(f"\n{Color.CYAN}Entrez votre choix (1-4) : {Color.END}")

        if choice == '1':
            path = input(f"\nEntrez le chemin complet : ")
            if os.path.exists(path):
                if os.path.isfile(path):
                    scanner.scan_file(path)
                else:
                    for root, _, files in os.walk(path):
                        for f in files:
                            scanner.scan_file(os.path.join(root, f))
            else:
                print(f"{Color.RED}Chemin invalide.{Color.END}")
            input("\nAppuyez sur Entrée pour revenir au menu...")

        elif choice == '2':
            scanner.scan_processes()
            input("\nAppuyez sur Entrée pour revenir au menu...")

        elif choice == '3':
            paths_to_check = [os.environ.get('TEMP'), os.path.expanduser('~/Downloads')]
            print(f"\n{Color.BOLD}Scan automatique des zones sensibles...{Color.END}")
            for p in paths_to_check:
                if p and os.path.exists(p):
                    print(f"\nScan de : {p}")
                    for f in os.listdir(p):
                        full_p = os.path.join(p, f)
                        if os.path.isfile(full_p) and (f.endswith('.exe') or f.endswith('.zip')):
                            scanner.scan_file(full_p)
            input("\nAppuyez sur Entrée pour revenir au menu...")

        elif choice == '4':
            print(f"{Color.BLUE}Fermeture du système de sécurité. Restez vigilant !{Color.END}")
            break
        else:
            print(f"{Color.RED}Choix invalide.{Color.END}")
            time.sleep(1)


if __name__ == "__main__":
    main()