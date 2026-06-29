import os
import psutil
import socket

# Liste de mots-clés ou noms souvent associés à des malwares (exemples)
SUSPICIOUS_NAMES = ["miner.exe", "keylogger", "spyware", "trojan"]
DANGEROUS_CODE = ["os.remove", "subprocess.Popen", "base64.b64decode", "requests.post"]


def scan_processes():
    print("--- Analyse des processus en cours ---")
    found = False
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            name = proc.info['name'].lower()
            for suspicious in SUSPICIOUS_NAMES:
                if suspicious in name:
                    print(f"[!] Alerte : Processus suspect trouvé : {name} (PID: {proc.info['pid']})")
                    found = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    if not found:
        print("[+] Aucun processus suspect détecté.")


def scan_startup():
    print("\n--- Analyse des dossiers de démarrage ---")
    # Chemin typique sous Windows pour le démarrage automatique
    startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    if os.path.exists(startup_path):
        files = os.listdir(startup_path)
        if files:
            print(f"[!] Fichiers trouvés au démarrage : {files}")
        else:
            print("[+] Le dossier de démarrage est propre.")
    else:
        print("[?] Dossier de démarrage introuvable (système non-Windows ?)")


def scan_directory(path):
    print(f"\n--- Analyse des scripts dans : {path} ---")
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(('.py', '.js', '.bat', '.ps1')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        for trigger in DANGEROUS_CODE:
                            if trigger in content:
                                print(f"[!] Script potentiellement malveillant : {file_path} (contient '{trigger}')")
                except Exception as e:
                    continue


def main():
    print("=== SCAN DE SÉCURITÉ PYTHON ===\n")
    scan_processes()
    scan_startup()

    # Scanner un dossier spécifique (ex: Téléchargements)
    target_folder = input("\nEntrez le chemin d'un dossier à scanner (ex: C:/Users/Nom/Downloads) : ")
    if os.path.exists(target_folder):
        scan_directory(target_folder)
    else:
        print("Chemin invalide.")


if __name__ == "__main__":
    main()