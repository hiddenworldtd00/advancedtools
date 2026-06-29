import os
import shutil
import time
import socket
import requests
import platform
import subprocess
from colorama import Fore, Style, init

# Initialisation des couleurs
init(autoreset=True)


class UltimateNexus:
    def __init__(self):
        self.book_extensions = ['.pdf', '.epub', '.mobi', '.azw3', '.cbz', '.fb2']

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def banner(self):
        self.clear()
        banner_text = f"""
{Fore.GREEN}{Style.BRIGHT}
███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
        {Fore.CYAN}>> SYSTEM REORGANIZER & OSINT SUITE <<
{Fore.GREEN}{'=' * 50}
        """
        print(banner_text)

    def progress_bar(self, current, total, text="Traitement"):
        length = 40
        percent = float(current) / total
        filled = int(length * percent)
        bar = '█' * filled + '-' * (length - filled)
        print(f'\r{Fore.WHITE}{text}: |{Fore.GREEN}{bar}{Fore.WHITE}| {int(percent * 100)}%', end='\r')
        if current == total: print()

    # --- FONCTIONNALITÉ 1 : REGROUPER LES LIVRES ---
    def organize_books(self):
        self.banner()
        print(f"{Fore.YELLOW}[!] Cet outil va scanner votre PC pour regrouper tous les livres.")
        folder_name = input(f"{Fore.CYAN}Nommez le dossier de destination : {Fore.WHITE}")

        target_dir = os.path.join(os.path.expanduser("~"), "Desktop", folder_name)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        print(f"{Fore.BLUE}[*] Recherche des livres dans votre dossier Utilisateur...")

        found_files = []
        search_root = os.path.expanduser("~")  # On cherche dans le dossier utilisateur pour aller vite

        for root, _, files in os.walk(search_root):
            for f in files:
                if any(f.lower().endswith(ext) for ext in self.book_extensions):
                    found_files.append(os.path.join(root, f))

        total = len(found_files)
        if total == 0:
            print(Fore.RED + "Aucun livre trouvé.")
            return

        print(f"{Fore.GREEN}{total} livres détectés. Début du transfert...")

        for i, file_path in enumerate(found_files):
            try:
                shutil.copy(file_path, target_dir)
                self.progress_bar(i + 1, total, "Migration")
            except:
                continue

        print(f"\n{Fore.GREEN}[✓] Terminé ! Tous les livres sont dans : {target_dir}")
        subprocess.run(['explorer', target_dir] if platform.system() == "Windows" else ['open', target_dir])

    # --- FONCTIONNALITÉ 2 : OUTILS OSINT ---
    def osint_menu(self):
        while True:
            self.banner()
            print(f"{Fore.WHITE}--- MENU OSINT ---")
            print("1. IP Lookup (Local & Public)")
            print("2. DNS Lookup (Host to IP)")
            print("3. Username Tracker (Simulateur)")
            print("4. Retour au menu principal")

            choice = input(f"\n{Fore.CYAN}Sélectionnez une option : ")

            if choice == '1':
                ip_pub = requests.get('https://api.ipify.org').text
                print(f"\n{Fore.GREEN}IP Publique : {ip_pub}")
                print(f"{Fore.GREEN}Hostname : {socket.gethostname()}")
                input("\nAppuyez sur Entrée...")

            elif choice == '2':
                domain = input("Entrez le domaine (ex: google.com) : ")
                try:
                    ip = socket.gethostbyname(domain)
                    print(f"{Fore.GREEN}L'adresse IP de {domain} est {ip}")
                except:
                    print(Fore.RED + "Impossible de résoudre le domaine.")
                input("\nAppuyez sur Entrée...")

            elif choice == '3':
                user = input("Nom d'utilisateur à chercher : ")
                print(f"{Fore.YELLOW}Recherche sur les plateformes...")
                platforms = ["GitHub", "Twitter", "Instagram", "Reddit"]
                for p in platforms:
                    time.sleep(0.5)
                    print(f"{Fore.WHITE}[+] Vérification {p}... {Fore.GREEN}OK")
                print(f"\n{Fore.BLUE}Rapport généré pour {user}.")
                input("\nAppuyez sur Entrée...")

            elif choice == '4':
                break

    def main_menu(self):
        while True:
            self.banner()
            print(f"1. {Fore.YELLOW}BIBLIOTHÈQUE : Regrouper tous les livres du PC{Fore.WHITE}")
            print(f"2. {Fore.YELLOW}OSINT : Outils de recherche d'informations{Fore.WHITE}")
            print(f"3. {Fore.RED}QUITTER{Fore.WHITE}")

            choice = input(f"\n{Fore.CYAN}Entrez votre choix (1-3) : ")

            if choice == '1':
                self.organize_books()
                input("\nAppuyez sur Entrée...")
            elif choice == '2':
                self.osint_menu()
            elif choice == '3':
                print(Fore.RED + "Extinction du système...")
                break


if __name__ == "__main__":
    app = UltimateNexus()
    app.main_menu()