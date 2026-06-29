import os
import sys
import platform
import subprocess
import time

# Couleurs et Styles ANSI
C = "\033[96m"  # Cyan
G = "\033[92m"  # Vert
Y = "\033[93m"  # Jaune
R = "\033[91m"  # Rouge
B = "\033[1m"  # Gras
RESET = "\033[0m"


def display_title():
    # Grand titre en ASCII Art Manuel
    title = f"""
{C}{B}
  ███████╗███████╗ █████╗ ██████╗  ██████╗██╗  ██╗
  ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║
  ███████╗█████╗  ███████║██████╔╝██║     ███████║
  ╚════██║██╔══╝  ██╔══██║██╔══██╗██║     ██╔══██║
  ███████║███████╗██║  ██║██║  ██║╚██████╗██║  ██║
  ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
           {Y}SYSTEME DE RECHERCHE ULTRA-RAPIDE{C}
{RESET}"""
    print(title)


def open_location(path):
    """Ouvre le dossier et sélectionne le fichier"""
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(['explorer', '/select,', os.path.normpath(path)])
        elif system == "Darwin":  # Mac
            subprocess.run(['open', '-R', path])
        else:  # Linux
            subprocess.run(['xdg-open', os.path.dirname(path)])
    except Exception as e:
        print(f"\n{R}Erreur d'ouverture : {e}{RESET}")


def search_with_progress(target_name, root_folder):
    matches = []
    # On récupère les dossiers du premier niveau pour calculer le pourcentage
    try:
        top_level_items = [os.path.join(root_folder, d) for d in os.listdir(root_folder)]
    except PermissionError:
        print(f"{R}Erreur : Permission refusée sur {root_folder}{RESET}")
        return []

    total_items = len(top_level_items)
    if total_items == 0: return []

    print(f"{Y}Initialisation du scan...{RESET}")

    for index, current_path in enumerate(top_level_items):
        # Calcul du pourcentage
        percent = int(((index + 1) / total_items) * 100)

        # Affichage de la barre de progression
        sys.stdout.write(f"\r{B}{C}[{percent}%]{RESET} Analyse : {current_path[:50].ljust(50)}...")
        sys.stdout.flush()

        # Recherche récursive dans le dossier actuel
        if os.path.isdir(current_path):
            for root, dirs, files in os.walk(current_path):
                for item in dirs + files:
                    if target_name.lower() in item.lower():
                        matches.append(os.path.join(root, item))
        else:
            if target_name.lower() in os.path.basename(current_path).lower():
                matches.append(current_path)

    # Forcer 100% à la fin
    sys.stdout.write(f"\r{B}{G}[100%]{RESET} Recherche terminée !{' ' * 60}\n")
    return matches


def main():
    display_title()

    search_query = input(f"{B}Entrez le nom (ou l'extension comme .apk) : {RESET}").strip()
    if not search_query:
        print(f"{R}Recherche annulée.{RESET}")
        return

    # Dossier de départ (Scan du dossier utilisateur pour la rapidité)
    start_dir = os.path.expanduser("~")

    print(f"\n{Y}Recherche de : {B}{search_query}{RESET} dans {B}{start_dir}{RESET}\n")

    results = search_with_progress(search_query, start_dir)

    if not results:
        print(f"\n{R}Aucun fichier ou dossier trouvé.{RESET}")
    else:
        print(f"\n{G}{B}{len(results)} RÉSULTAT(S) TROUVÉ(S) :{RESET}")
        for i, path in enumerate(results[:20]):  # Limite à 20 résultats affichés
            print(f"{C}[{i}]{RESET} {path}")

        if len(results) > 20:
            print(f"... et {len(results) - 20} autres.")

        choice = input(f"\n{B}Entrez le numéro pour l'ouvrir (ou n'importe quoi pour quitter) : {RESET}")

        if choice.isdigit() and int(choice) < len(results):
            selected = results[int(choice)]
            print(f"{G}Ouverture de l'emplacement : {selected}{RESET}")
            open_location(selected)


if __name__ == "__main__":
    main()