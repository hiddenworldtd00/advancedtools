import os
import platform
import subprocess

# Codes de couleurs ANSI (Sans module externe)
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def display_banner():
    banner = f"""
{CYAN}{BOLD}
  🔍 EXPLORATEUR DE FICHIERS AVANCÉ
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [ RECHERCHE & OUVERTURE DIRECTE ]
{RESET}"""
    print(banner)


def open_file_location(path):
    """Ouvre le dossier et sélectionne le fichier selon l'OS"""
    system = platform.system()
    try:
        if system == "Windows":
            # Ouvre l'explorateur et sélectionne le fichier
            subprocess.run(['explorer', '/select,', os.path.normpath(path)])
        elif system == "Darwin":  # macOS
            subprocess.run(['open', '-R', path])
        else:  # Linux
            # Ouvre le dossier parent
            subprocess.run(['xdg-open', os.path.dirname(path)])
        return True
    except Exception as e:
        print(f"{RED}Erreur lors de l'ouverture : {e}{RESET}")
        return False


def fast_search(name, search_path):
    print(f"\n{YELLOW}Recherche de '{name}' dans {search_path}...{RESET}")
    print(f"{BLUE}(Cela peut prendre du temps selon la taille du disque){RESET}\n")

    matches = []

    # Parcours du système de fichiers
    for root, dirs, files in os.walk(search_path):
        # Vérifier dans les dossiers ET les fichiers
        for item in dirs + files:
            if name.lower() in item.lower():
                full_path = os.path.join(root, item)
                matches.append(full_path)
                # Optionnel : Arrêter à la première correspondance pour aller plus vite
                # return [full_path]

    return matches


def main():
    display_banner()

    target = input(f"{BOLD}Nom du fichier/dossier/APK à chercher : {RESET}").strip()
    if not target:
        print(f"{RED}Nom invalide.{RESET}")
        return

    # Définition du point de départ (Dossier utilisateur par défaut pour la rapidité)
    # Pour scanner TOUT le PC sur Windows, utilisez "C:\\"
    home_dir = os.path.expanduser("~")

    results = fast_search(target, home_dir)

    if not results:
        print(f"{RED}Aucun résultat trouvé pour '{target}'.{RESET}")
    else:
        print(f"{GREEN}{len(results)} résultat(s) trouvé(s) :{RESET}")
        for i, path in enumerate(results):
            print(f"{CYAN}[{i}] {RESET}{path}")

        choice = input(f"\n{BOLD}Entrez le numéro pour l'ouvrir (ou 'q' pour quitter) : {RESET}")

        if choice.isdigit() and int(choice) < len(results):
            selected_path = results[int(choice)]
            print(f"{YELLOW}Ouverture de l'emplacement...{RESET}")
            open_file_location(selected_path)
        else:
            print("Quitter.")


if __name__ == "__main__":
    main()