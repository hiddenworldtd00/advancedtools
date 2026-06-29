import os
import time
import math
import psutil
import platform
import subprocess
from colorama import Fore, Style, init

# Initialisation des couleurs
init(autoreset=True)


class SentinelPro:
    def __init__(self):
        self.title = "🛡️ SENTINEL ADVANCED SECURITY PRO 🛡️"

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw_header(self):
        self.clear_screen()
        print(Fore.CYAN + "=" * 60)
        print(Fore.GREEN + Style.BRIGHT + self.title.center(60))
        print(Fore.CYAN + "=" * 60 + "\n")

    def progress_bar(self, current, total, status='Analyse en cours'):
        """Affiche une barre de progression de 1 à 100%"""
        length = 40
        percent = float(current) / total
        filled_length = int(length * percent)
        bar = '█' * filled_length + '-' * (length - filled_length)

        # Calcul du pourcentage
        p_val = int(percent * 100)

        # Affichage (le \r permet de rester sur la même ligne)
        print(f'\r{Fore.WHITE}{status} : |{Fore.BLUE}{bar}{Fore.WHITE}| {p_val}%', end='\r')
        if current == total:
            print()

    def calculate_entropy(self, path):
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

    def open_location(self, path):
        """Ouvre le dossier contenant le fichier suspect et le sélectionne"""
        try:
            folder = os.path.dirname(path)
            if platform.system() == "Windows":
                # Ouvre l'explorateur et sélectionne le fichier
                subprocess.run(['explorer', '/select,', os.path.normpath(path)])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(['open', '-R', path])
            else:  # Linux
                subprocess.run(['xdg-open', folder])
        except Exception as e:
            print(f"{Fore.RED}Erreur ouverture dossier : {e}")

    def analyze_file(self, file_path):
        score = 0
        details = []

        # 1. Analyse extension
        if file_path.lower().endswith(('.exe', '.bat', '.cmd', '.scr', '.vbs')):
            score += 10

        # 2. Analyse entropie (Code packé/crypté)
        entropy = self.calculate_entropy(file_path)
        if entropy > 7.4:
            score += 50
            details.append(f"Fichier crypté/obfusqué (Entropie: {entropy:.2f})")

        # 3. Double extension
        if file_path.count('.') > 1:
            score += 20
            details.append("Double extension suspecte")

        return score, details

    def scan_directory(self, folder_path):
        all_files = []
        for root, _, files in os.walk(folder_path):
            for f in files:
                all_files.append(os.path.join(root, f))

        total = len(all_files)
        if total == 0:
            print(Fore.YELLOW + "Dossier vide.")
            return

        print(f"{Fore.CYAN}Démarrage du scan de {total} fichiers...\n")

        for i, file_path in enumerate(all_files):
            # Mise à jour de la barre 1-100%
            self.progress_bar(i + 1, total)

            score, details = self.analyze_file(file_path)

            if score >= 50:
                print(f"\n{Fore.RED}{Style.BRIGHT}[!!!] MENACE DÉTECTÉE : {os.path.basename(file_path)}")
                print(f"{Fore.RED}Score de risque : {score}/100")
                for d in details:
                    print(f"  -> {d}")

                print(f"{Fore.YELLOW}Ouverture automatique de l'emplacement...")
                self.open_location(file_path)
                time.sleep(1)  # Pause pour laisser l'utilisateur voir
                print("\n" + "-" * 30)

        print(f"\n{Fore.GREEN}--- Scan terminé ---")

    def scan_memory(self):
        print(f"{Fore.CYAN}Analyse des processus en mémoire...")
        procs = list(psutil.process_iter())
        total = len(procs)

        for i, proc in enumerate(procs):
            self.progress_bar(i + 1, total, status='Scan RAM')
            try:
                p_info = proc.as_dict(attrs=['pid', 'name', 'exe'])
                if p_info['exe'] and ("Temp" in p_info['exe'] or "AppData" in p_info['exe']):
                    print(f"\n{Fore.RED}[!] PROCESSUS SUSPECT : {p_info['name']} (PID: {p_info['pid']})")
                    print(f"Chemin : {p_info['exe']}")
                    self.open_location(p_info['exe'])
            except:
                continue
        print(f"\n{Fore.GREEN}--- Analyse RAM terminée ---")


def main():
    scanner = SentinelPro()

    while True:
        scanner.draw_header()
        print(f"{Fore.WHITE}{Style.BRIGHT}MENU DES OUTILS :")
        print(f"1. {Fore.YELLOW}Scanner un Dossier (avec barre %)")
        print(f"2. {Fore.YELLOW}Scanner un Fichier unique")
        print(f"3. {Fore.YELLOW}Scanner la Mémoire vive (RAM)")
        print(f"4. {Fore.RED}Quitter")

        choice = input(f"\n{Fore.CYAN}Choisissez un outil (1-4) : ")

        if choice == '1':
            path = input("Chemin du dossier : ").strip('"')
            if os.path.isdir(path):
                scanner.scan_directory(path)
            else:
                print(Fore.RED + "Dossier invalide.")
            input("\nAppuyez sur Entrée...")

        elif choice == '2':
            path = input("Chemin du fichier : ").strip('"')
            if os.path.isfile(path):
                score, details = scanner.analyze_file(path)
                if score >= 50:
                    print(f"{Fore.RED}RÉSULTAT : MALVEILLANT ({score}/100)")
                    scanner.open_location(path)
                else:
                    print(f"{Fore.GREEN}RÉSULTAT : SAIN")
            input("\nAppuyez sur Entrée...")

        elif choice == '3':
            scanner.scan_memory()
            input("\nAppuyez sur Entrée...")

        elif choice == '4':
            break


if __name__ == "__main__":
    main()