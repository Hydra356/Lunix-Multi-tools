import os
import sys
import time
import random
import string
import requests
from datetime import datetime

# Couleurs
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RESET = '\033[0m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_red(text):
    print(f"{RED}{text}{RESET}")

def print_green(text):
    print(f"{GREEN}{text}{RESET}")

def print_yellow(text):
    print(f"{YELLOW}{text}{RESET}")

def print_cyan(text, end='\n'):
    print(f"{CYAN}{text}{RESET}", end=end)

def print_magenta(text):
    print(f"{MAGENTA}{text}{RESET}")

def ascii_banner():
    banner = """
╔╗╔╦╔╦╗╦═╗╔═╗  ╔═╗╔═╗╔╗╔╔═╗╦═╗╔═╗╔╦╗╔═╗╦═╗
║║║║ ║ ╠╦╝║ ║  ║ ╦║╣ ║║║║╣ ╠╦╝╠═╣ ║ ║ ║╠╦╝
╝╚╝╩ ╩ ╩╚═╚═╝  ╚═╝╚═╝╝╚╝╚═╝╩╚═╩ ╩ ╩ ╚═╝╩╚═
    Générateur de Codes Discord Nitro
    """
    return banner

def generate_nitro_code():
    """Génère un code Nitro Discord aléatoire"""
    # Format: https://discord.gift/XXXXXXXXXXXXXXXX (16 caractères)
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(16))
    return code

def check_nitro_code(code):
    """Vérifie si un code Nitro est valide"""
    try:
        url = f"https://discord.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
        
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            return {'valid': True, 'status': 'Valide'}
        elif response.status_code == 404:
            return {'valid': False, 'status': 'Invalide'}
        elif response.status_code == 429:
            return {'valid': False, 'status': 'Rate Limited'}
        else:
            return {'valid': False, 'status': f'Erreur {response.status_code}'}
            
    except requests.exceptions.Timeout:
        return {'valid': False, 'status': 'Timeout'}
    except Exception as e:
        return {'valid': False, 'status': 'Erreur'}

def nitro_generator(amount, check_codes=False):
    """Génère et optionnellement vérifie des codes Nitro"""
    
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70)
    print_red(f"  Génération de {amount} codes")
    print_red(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print_red("="*70 + "\n")
    
    print_yellow(f"[*] Génération de {amount} codes Discord Nitro...\n")
    time.sleep(1)
    
    valid_codes = []
    invalid_codes = []
    
    for i in range(amount):
        code = generate_nitro_code()
        full_url = f"https://discord.gift/{code}"
        
        if check_codes:
            print_cyan(f"[~] Vérification {i+1}/{amount}: {code}", end="\r")
            result = check_nitro_code(code)
            
            if result['valid']:
                print_green(f"[+] VALIDE! {full_url}")
                valid_codes.append(full_url)
            else:
                print_red(f"[-] Invalide: {code} ({result['status']})")
                invalid_codes.append(full_url)
            
            # Délai pour éviter le rate limiting
            time.sleep(0.5)
        else:
            print_cyan(f"[+] Code {i+1}/{amount}: {full_url}")
            valid_codes.append(full_url)
    
    # Résumé
    print_red("\n\n" + "="*70)
    print_red("                    RÉSUMÉ DE LA GÉNÉRATION")
    print_red("="*70 + "\n")
    
    if check_codes:
        print_green(f"[+] Codes valides trouvés: {len(valid_codes)}")
        print_red(f"[-] Codes invalides: {len(invalid_codes)}")
        
        if valid_codes:
            print_magenta("\n┌─ CODES VALIDES:")
            for code in valid_codes:
                print_green(f"│ {code}")
    else:
        print_cyan(f"[*] {len(valid_codes)} codes générés (non vérifiés)")
        print_yellow("\n[!] Note: Ces codes sont générés aléatoirement")
        print_yellow("[!] La probabilité qu'un code soit valide est extrêmement faible")
    
    # Sauvegarde
    print_red("\n" + "="*70)
    save_choice = input(f"\n{YELLOW}[*] Sauvegarder les codes? (o/n): {RESET}").strip().lower()
    
    if save_choice == 'o' or save_choice == 'oui':
        save_codes(valid_codes, check_codes)
    
    print_red("\n" + "="*70 + "\n")

def save_codes(codes, checked):
    """Sauvegarde les codes dans un fichier"""
    try:
        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        status = "checked" if checked else "generated"
        filename = f"{results_dir}/nitro_{status}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("  LUNIX - NITRO GENERATOR RESULTS\n")
            f.write(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"  Status: {'Vérifiés' if checked else 'Générés (non vérifiés)'}\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"NOMBRE DE CODES: {len(codes)}\n\n")
            
            for i, code in enumerate(codes, 1):
                f.write(f"{i}. {code}\n")
            
            if not checked:
                f.write("\n" + "="*70 + "\n")
                f.write("AVERTISSEMENT\n")
                f.write("="*70 + "\n")
                f.write("Ces codes ont été générés aléatoirement.\n")
                f.write("La probabilité qu'ils soient valides est extrêmement faible.\n")
                f.write("Discord Nitro utilise des codes cryptographiquement sécurisés.\n")
        
        print_green(f"\n[+] Codes sauvegardés dans: {filename}")
        
    except Exception as e:
        print_red(f"\n[!] Erreur lors de la sauvegarde: {str(e)}")

def main():
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70 + "\n")
    
    print_yellow("[!] AVERTISSEMENT")
    print_red("─" * 70)
    print_cyan("Les codes Discord Nitro sont cryptographiquement sécurisés.")
    print_cyan("La probabilité de générer un code valide est astronomiquement faible.")
    print_cyan("Cet outil est fourni à des fins ÉDUCATIVES uniquement.")
    print_red("─" * 70)
    
    try:
        amount = int(input(f"\n{RED}[*] Nombre de codes à générer: {RESET}").strip())
        
        if amount <= 0:
            print_red("\n[!] Le nombre doit être positif!")
            time.sleep(2)
            return
        
        if amount > 100:
            print_yellow("\n[!] Attention: Générer plus de 100 codes peut prendre du temps")
            confirm = input(f"{YELLOW}[*] Continuer? (o/n): {RESET}").strip().lower()
            if confirm != 'o' and confirm != 'oui':
                print_red("\n[*] Annulé")
                time.sleep(1)
                return
        
        check = input(f"\n{YELLOW}[*] Vérifier les codes (peut être long)? (o/n): {RESET}").strip().lower()
        check_codes = (check == 'o' or check == 'oui')
        
        if check_codes:
            print_yellow("\n[!] La vérification peut déclencher un rate limit Discord")
            confirm = input(f"{YELLOW}[*] Continuer quand même? (o/n): {RESET}").strip().lower()
            if confirm != 'o' and confirm != 'oui':
                check_codes = False
                print_yellow("\n[*] Les codes seront générés sans vérification")
        
        print_red(f"\n[*] Démarrage...\n")
        time.sleep(1)
        
        nitro_generator(amount, check_codes)
        
    except ValueError:
        print_red("\n[!] Veuillez entrer un nombre valide!")
        time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_red("\n\n[!] Génération interrompue par l'utilisateur.")
        sys.exit(0)
