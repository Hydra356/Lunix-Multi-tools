import os
import sys
import time
import re
from datetime import datetime

# Couleurs
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_red(text):
    print(f"{RED}{text}{RESET}")

def print_green(text):
    print(f"{GREEN}{text}{RESET}")

def print_yellow(text, end='\n'):
    print(f"{YELLOW}{text}{RESET}", end=end)

def print_cyan(text):
    print(f"{CYAN}{text}{RESET}")

def ascii_banner():
    banner = """
╔═╗╦ ╦╔═╗╔╗╔╔═╗  ╦╔╗╔╔═╗╔═╗
╠═╝╠═╣║ ║║║║║╣   ║║║║╠╣ ║ ║
╩  ╩ ╩╚═╝╝╚╝╚═╝  ╩╝╚╝╚  ╚═╝
  Informations sur Numéro de Téléphone
    """
    return banner

# Base de données des indicatifs pays
COUNTRY_CODES = {
    '+1': 'États-Unis / Canada',
    '+33': 'France',
    '+32': 'Belgique',
    '+41': 'Suisse',
    '+49': 'Allemagne',
    '+44': 'Royaume-Uni',
    '+34': 'Espagne',
    '+39': 'Italie',
    '+351': 'Portugal',
    '+31': 'Pays-Bas',
    '+46': 'Suède',
    '+47': 'Norvège',
    '+45': 'Danemark',
    '+358': 'Finlande',
    '+7': 'Russie / Kazakhstan',
    '+86': 'Chine',
    '+81': 'Japon',
    '+82': 'Corée du Sud',
    '+91': 'Inde',
    '+61': 'Australie',
    '+64': 'Nouvelle-Zélande',
    '+27': 'Afrique du Sud',
    '+20': 'Égypte',
    '+212': 'Maroc',
    '+213': 'Algérie',
    '+216': 'Tunisie',
    '+234': 'Nigeria',
    '+52': 'Mexique',
    '+54': 'Argentine',
    '+55': 'Brésil',
    '+56': 'Chili',
    '+57': 'Colombie',
}

def normalize_phone(phone):
    """Normalise le numéro de téléphone"""
    # Supprime tous les caractères non numériques sauf le +
    phone = re.sub(r'[^\d+]', '', phone)
    
    # Si le numéro commence par 00, remplace par +
    if phone.startswith('00'):
        phone = '+' + phone[2:]
    
    # Si le numéro ne commence pas par +, ajoute +
    if not phone.startswith('+'):
        phone = '+' + phone
    
    return phone

def identify_country(phone):
    """Identifie le pays à partir de l'indicatif"""
    for code, country in sorted(COUNTRY_CODES.items(), key=lambda x: len(x[0]), reverse=True):
        if phone.startswith(code):
            return {
                'code': code,
                'country': country,
                'number_without_code': phone[len(code):]
            }
    
    return {
        'code': 'Inconnu',
        'country': 'Pays non identifié',
        'number_without_code': phone
    }

def get_phone_type(phone, country_code):
    """Détermine le type de numéro (mobile/fixe) - basique"""
    # Pour la France
    if country_code == '+33':
        number = phone.replace(country_code, '')
        if number.startswith('6') or number.startswith('7'):
            return 'Mobile'
        elif number.startswith(('1', '2', '3', '4', '5', '9')):
            return 'Fixe'
    
    # Pour les autres pays, on ne peut pas déterminer facilement
    return 'Non déterminé'

def format_phone(phone, country_info):
    """Formate le numéro de manière lisible"""
    code = country_info['code']
    number = country_info['number_without_code']
    
    # Formatage par groupes de 2
    formatted = code + ' '
    for i in range(0, len(number), 2):
        formatted += number[i:i+2] + ' '
    
    return formatted.strip()

def phone_info(phone):
    """Fonction principale d'analyse de numéro"""
    
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70)
    print_red(f"  Numéro analysé: {phone}")
    print_red(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print_red("="*70 + "\n")
    
    # Normalisation
    print_yellow("[~] Normalisation du numéro...", end="\r")
    time.sleep(0.5)
    normalized = normalize_phone(phone)
    print_green(f"[+] Numéro normalisé: {normalized}")
    
    # Identification du pays
    print_yellow("[~] Identification du pays...", end="\r")
    time.sleep(0.5)
    country_info = identify_country(normalized)
    
    # Formatage
    formatted = format_phone(normalized, country_info)
    
    # Type de numéro
    phone_type = get_phone_type(normalized, country_info['code'])
    
    # Affichage des résultats
    print_red("\n" + "="*70)
    print_red("                    INFORMATIONS GÉNÉRALES")
    print_red("="*70)
    print_cyan(f"\n  Numéro original: {phone}")
    print_cyan(f"  Numéro normalisé: {normalized}")
    print_cyan(f"  Numéro formaté: {formatted}")
    
    print_red("\n" + "="*70)
    print_red("                    LOCALISATION")
    print_red("="*70)
    print_cyan(f"\n  Indicatif pays: {country_info['code']}")
    print_cyan(f"  Pays: {country_info['country']}")
    print_cyan(f"  Type de ligne: {phone_type}")
    
    # Opérateurs possibles (exemple pour la France)
    if country_info['code'] == '+33':
        print_red("\n" + "="*70)
        print_red("                    OPÉRATEURS POSSIBLES (FR)")
        print_red("="*70)
        print_cyan("\n  Opérateurs principaux:")
        print_cyan("  • Orange")
        print_cyan("  • SFR")
        print_cyan("  • Bouygues Telecom")
        print_cyan("  • Free Mobile")
    
    # Sauvegarde
    save_results(phone, normalized, formatted, country_info, phone_type)
    
    print_red("\n" + "="*70 + "\n")

def save_results(original, normalized, formatted, country_info, phone_type):
    """Sauvegarde les résultats dans un fichier"""
    try:
        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        safe_number = normalized.replace('+', '').replace(' ', '')
        filename = f"{results_dir}/phone_{safe_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("  LUNIX - PHONE INFO RESULTS\n")
            f.write(f"  Numéro: {original}\n")
            f.write(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")
            
            f.write("INFORMATIONS GÉNÉRALES\n")
            f.write("-" * 70 + "\n")
            f.write(f"Numéro original: {original}\n")
            f.write(f"Numéro normalisé: {normalized}\n")
            f.write(f"Numéro formaté: {formatted}\n\n")
            
            f.write("LOCALISATION\n")
            f.write("-" * 70 + "\n")
            f.write(f"Indicatif pays: {country_info['code']}\n")
            f.write(f"Pays: {country_info['country']}\n")
            f.write(f"Type de ligne: {phone_type}\n\n")
        
        print_green(f"[+] Résultats sauvegardés dans: {filename}")
        
    except Exception as e:
        print_red(f"[!] Erreur lors de la sauvegarde: {str(e)}")

def main():
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70 + "\n")
    
    phone = input(f"{RED}[*] Entrez le numéro de téléphone: {RESET}").strip()
    
    if not phone:
        print_red("\n[!] Erreur: Veuillez entrer un numéro valide!")
        time.sleep(2)
        return
    
    print_red(f"\n[*] Démarrage de l'analyse...\n")
    time.sleep(1)
    
    phone_info(phone)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_red("\n\n[!] Analyse interrompue par l'utilisateur.")
        sys.exit(0)
