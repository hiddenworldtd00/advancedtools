import socket
import cv2
import os


def scan_network(ip_prefix):
    print(f"Scanning {ip_prefix}.0/24...")
    cameras = []
    # Teste les IPs de .1 à .254 sur le port RTSP standard (554)
    for i in range(1, 255):
        ip = f"{ip_prefix}.{i}"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            if s.connect_ex((ip, 554)) == 0:
                print(f"[+] Caméra potentielle trouvée : {ip}")
                cameras.append(ip)
    return cameras


def main():
    # Détection automatique de l'IP locale (ex: 192.168.1)
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    ip_prefix = ".".join(local_ip.split(".")[:-1])

    cams = scan_network(ip_prefix)

    if not cams:
        print("Aucune caméra trouvée sur le port 554.")
        return

    print("\nCaméras trouvées :")
    for idx, ip in enumerate(cams):
        print(f"{idx}: {ip}")

    choice = int(input("\nChoisissez le numéro de la caméra : "))
    target_ip = cams[choice]

    # Note: L'URL RTSP varie selon la marque (ex: /h264, /live, /Streaming/Channels/101)
    # Si vous connaissez le login/pass, format : rtsp://user:pass@IP:554/path
    user = input("Utilisateur (laisser vide si aucun) : ")
    password = input("Mot de passe (laisser vide si aucun) : ")
    path = input("Chemin du flux (ex: /h264, /live, /ch1) [defaut: /] : ") or "/"

    if user and password:
        url = f"rtsp://{user}:{password}@{target_ip}:554{path}"
    else:
        url = f"rtsp://{target_ip}:554{path}"

    print(f"Ouverture de : {url}")
    cap = cv2.VideoCapture(url)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur de flux ou accès refusé.")
            break

        cv2.imshow(f"Camera {target_ip}", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Appuyez sur 'q' pour quitter
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()