import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import sys

# Codes de couleurs ANSI manuels
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def display_banner():
    # Grand titre en ASCII Art manuel
    banner = f"""
{CYAN}{BOLD}
  ██████╗ ██╗  ██╗ ██████╗ ███╗   ██╗███████╗
  ██╔══██╗██║  ██║██╔═══██╗████╗  ██║██╔════╝
  ██████╔╝███████║██║   ██║██╔██╗ ██║█████╗  
  ██╔═══╝ ██╔══██║██║   ██║██║╚██╗██║██╔══╝  
  ██║     ██║  ██║╚██████╔╝██║ ╚████║███████╗
  ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
           {YELLOW}SCANNER DE NUMÉRO AVANCÉ{CYAN}
{RESET}"""
    print(banner)
    print(f"{BLUE}{'=' * 55}{RESET}")


def scan_expert(phone_input):
    try:
        # Analyse du numéro
        obj = phonenumbers.parse(phone_input)

        if not phonenumbers.is_valid_number(obj):
            print(f"{RED}[!] ERREUR : Le numéro n'est pas valide ou inexistant.{RESET}")
            return

        print(f"\n{GREEN}{BOLD}>>> RÉSULTATS DE L'EXTRACTION <<<{RESET}\n")

        # Tableau de bord des résultats
        data = [
            ("Format International", phonenumbers.format_number(obj, phonenumbers.PhoneNumberFormat.INTERNATIONAL)),
            ("Localisation", geocoder.description_for_number(obj, "fr")),
            ("Opérateur (Carrier)", carrier.name_for_number(obj, "fr") or "Non identifié"),
            ("Fuseau Horaire", ", ".join(timezone.time_zones_for_number(obj))),
            ("Code Pays", f"+{obj.country_code}"),
            ("Numéro National", obj.national_number),
            ("Type de ligne", "Mobile" if phonenumbers.number_type(obj) == 1 else "Fixe / Autre")
        ]

        for label, value in data:
            print(f"{CYAN}{label.ljust(22)} : {RESET}{WHITE_BOLD}{value}{RESET}")

    except Exception as e:
        print(f"{RED}[!] Erreur système : {e}{RESET}")


# Variable pour le blanc gras
WHITE_BOLD = "\033[1;37m"


def main():
    display_banner()

    print(f"{YELLOW}Format requis : + [CodePays] [Numéro] (ex: +33612345678){RESET}")
    num = input(f"{BOLD}ENTREZ LE NUMÉRO > {RESET}").strip()

    if not num:
        print(f"{RED}Entrée vide.{RESET}")
        return

    print(f"\n{BLUE}{'-' * 55}{RESET}")
    scan_expert(num)
    print(f"{BLUE}{'-' * 55}{RESET}")
    print(f"\n{GREEN}Scan terminé avec succès.{RESET}")


if __name__ == "__main__":
    main()