import os
import time
import subprocess
import platform
from colorama import Fore, Style, init

# Initialisation des couleurs
init(autoreset=True)


def print_banner():
    """Affiche un titre géant en style hacker"""
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
 ██████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗
██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║
╚█████╗ ███████║███████║██║  ██║██║   ██║██║ █╗ ██║
 ╚═══██╗██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║
██████╔╝██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ 
    {Fore.RED}RECONNAISSANCE & INFORMATION GATHERING ARCHIVER
{Fore.CYAN}{'=' * 60}
    """
    print(banner)


def progress_bar(status="Génération"):
    """Simule une barre de progression de 0 à 100%"""
    length = 50
    for i in range(101):
        time.sleep(0.02)  # Vitesse de progression
        filled = int(length * i // 100)
        bar = '█' * filled + '-' * (length - filled)
        print(f'\r{Fore.WHITE}{status} : |{Fore.GREEN}{bar}{Fore.WHITE}| {i}%', end='\r')
    print("\n")


def open_file(filename):
    """Ouvre le fichier texte directement sur l'ordinateur"""
    try:
        if platform.system() == "Windows":
            os.startfile(filename)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", filename])
        else:  # Linux
            subprocess.run(["xdg-open", filename])
    except Exception as e:
        print(f"{Fore.RED}Erreur lors de l'ouverture : {e}")


def create_recon_file():
    print_banner()

    # Input pour le nom du fichier
    file_name = input(f"{Fore.YELLOW}Entrez le nom du rapport (ex: cible_recon) : {Fore.WHITE}").strip()
    if not file_name.endswith(".txt"):
        file_name += ".txt"

    print(f"\n{Fore.BLUE}[*] Initialisation du protocole de stockage...")

    # Contenu du rapport (Template d'Information Gathering)
    content = f"""============================================================
           SHADOW RECONNAISSANCE REPORT
============================================================
DATE: {time.strftime('%Y-%m-%d %H:%M:%S')}
CIBLE: {file_name.replace('.txt', '')}
------------------------------------------------------------

[1] RECONNAISSANCE RÉSEAU (Network)
-----------------------------------
- IP Publique: 
- Ports Ouverts: 
- Services Détectés:
- DNS / Sous-domaines:

[2] EMPREINTE NUMÉRIQUE (OSINT)
-------------------------------
- Emails trouvés:
- Profils Sociaux:
- Noms de domaine associés:
- Technologies Web:

[3] ANALYSE DE VULNÉRABILITÉ (Leaks)
------------------------------------
- Mots de passe fugués:
- Anciennes versions logicielles:

[4] NOTES ADDITIONNELLES
------------------------
> 

============================================================
        END OF ARCHIVE - ENCRYPTED STORAGE READY
============================================================
"""

    # Simulation de la progression
    progress_bar("Cryptage des données")

    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"{Fore.GREEN}{Style.BRIGHT}[✓] Rapport créé avec succès : {file_name}")
        print(f"{Fore.CYAN}[*] Ouverture du fichier en cours...")

        time.sleep(1)
        open_file(file_name)

    except Exception as e:
        print(f"{Fore.RED}[!] Erreur fatale : {e}")


if __name__ == "__main__":
    create_recon_file()