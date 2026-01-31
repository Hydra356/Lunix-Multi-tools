import os
import sys
import time
import re
import requests
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
╔═╗╔╦╗╔═╗╦╦    ╔╦╗╦═╗╔═╗╔═╗╦╔═╔═╗╦═╗
║╣ ║║║╠═╣║║     ║ ╠╦╝╠═╣║  ╠╩╗║╣ ╠╦╝
╚═╝╩ ╩╩ ╩╩╩═╝   ╩ ╩╚═╩ ╩╚═╝╩ ╩╚═╝╩╚═
    Analyse OSINT d'Adresses Email
    """
    return banner

def validate_email(email):
    """Valide le format de l'email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def extract_info(email):
    """Extrait les informations de base de l'email"""
    try:
        username, domain = email.split('@')
        return {
            'username': username,
            'domain': domain,
            'full_email': email
        }
    except:
        return None

def check_email_breach(email):
    """Vérifie si l'email apparaît dans des fuites de données"""
    print_yellow("\n[~] Vérification des fuites de données...", end="\r")
    time.sleep(0.5)
    
    # Note: Pour une vraie vérification, utilisez l'API HaveIBeenPwned
    # Ceci est une démonstration
    print_red("[!] Vérification manuelle recommandée sur: https://haveibeenpwned.com/")
    return None

def check_social_media(email):
    """Recherche l'email sur les réseaux sociaux"""
    info = extract_info(email)
    if not info:
        return []
    
    username = info['username']
    
    print_yellow("\n[~] Recherche sur les réseaux sociaux...", end="\r")
    time.sleep(0.5)
    
    platforms = {
        'Gravatar': f'https://en.gravatar.com/{email}',
        'GitHub (username)': f'https://github.com/{username}',
        'Twitter (username)': f'https://twitter.com/{username}',
    }
    
    results = []
    for platform, url in platforms.items():
        results.append((platform, url))
    
    print_green(f"[+] {len(results)} plateformes à vérifier manuellement")
    return results

def analyze_domain(domain):
    """Analyse le domaine de l'email"""
    print_yellow("\n[~] Analyse du domaine...", end="\r")
    time.sleep(0.5)
    
    common_providers = {
        'gmail.com': 'Google Gmail',
        'yahoo.com': 'Yahoo Mail',
        'hotmail.com': 'Microsoft Hotmail',
        'outlook.com': 'Microsoft Outlook',
        'icloud.com': 'Apple iCloud',
        'protonmail.com': 'ProtonMail (Sécurisé)',
        'proton.me': 'ProtonMail (Sécurisé)',
        'aol.com': 'AOL Mail',
        'mail.com': 'Mail.com',
        'zoho.com': 'Zoho Mail',
    }
    
    provider = common_providers.get(domain, 'Domaine personnalisé ou inconnu')
    
    return {
        'domain': domain,
        'provider': provider,
        'is_common': domain in common_providers
    }

def email_tracker(email):
    """Fonction principale de tracking d'email"""
    
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70)
    print_red(f"  Email analysé: {email}")
    print_red(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print_red("="*70 + "\n")
    
    # Validation
    if not validate_email(email):
        print_red("[!] Format d'email invalide!")
        return
    
    print_green("[+] Format d'email valide")
    
    # Extraction des informations
    info = extract_info(email)
    if info:
        print_red("\n" + "="*70)
        print_red("                    INFORMATIONS DE BASE")
        print_red("="*70)
        print_cyan(f"\n  Username: {info['username']}")
        print_cyan(f"  Domaine: {info['domain']}")
        print_cyan(f"  Email complet: {info['full_email']}")
    
    # Analyse du domaine
    domain_info = analyze_domain(info['domain'])
    print_red("\n" + "="*70)
    print_red("                    ANALYSE DU DOMAINE")
    print_red("="*70)
    print_cyan(f"\n  Domaine: {domain_info['domain']}")
    print_cyan(f"  Fournisseur: {domain_info['provider']}")
    print_cyan(f"  Type: {'Fournisseur populaire' if domain_info['is_common'] else 'Domaine personnalisé'}")
    
    # Vérification des fuites
    print_red("\n" + "="*70)
    print_red("                  VÉRIFICATION DES FUITES")
    print_red("="*70)
    check_email_breach(email)
    
    # Recherche sur les réseaux sociaux
    print_red("\n" + "="*70)
    print_red("                  PRÉSENCE SUR LES RÉSEAUX")
    print_red("="*70)
    social_results = check_social_media(email)
    
    if social_results:
        print_green(f"\n[+] Plateformes à vérifier manuellement:")
        for platform, url in social_results:
            print_cyan(f"  [{platform}] {url}")
    
    # Sauvegarde
    save_results(email, info, domain_info, social_results)
    
    print_red("\n" + "="*70 + "\n")

def save_results(email, info, domain_info, social_results):
    """Sauvegarde les résultats dans un fichier"""
    try:
        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        filename = f"{results_dir}/email_{info['username']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("  LUNIX - EMAIL TRACKER RESULTS\n")
            f.write(f"  Email: {email}\n")
            f.write(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")
            
            f.write("INFORMATIONS DE BASE\n")
            f.write("-" * 70 + "\n")
            f.write(f"Username: {info['username']}\n")
            f.write(f"Domaine: {info['domain']}\n")
            f.write(f"Email complet: {info['full_email']}\n\n")
            
            f.write("ANALYSE DU DOMAINE\n")
            f.write("-" * 70 + "\n")
            f.write(f"Domaine: {domain_info['domain']}\n")
            f.write(f"Fournisseur: {domain_info['provider']}\n")
            f.write(f"Type: {'Fournisseur populaire' if domain_info['is_common'] else 'Domaine personnalisé'}\n\n")
            
            f.write("PLATEFORMES À VÉRIFIER\n")
            f.write("-" * 70 + "\n")
            for platform, url in social_results:
                f.write(f"[{platform}]\n{url}\n\n")
        
        print_green(f"[+] Résultats sauvegardés dans: {filename}")
        
    except Exception as e:
        print_red(f"[!] Erreur lors de la sauvegarde: {str(e)}")

def main():
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70 + "\n")
    
    email = input(f"{RED}[*] Entrez l'adresse email à analyser: {RESET}").strip()
    
    if not email:
        print_red("\n[!] Erreur: Veuillez entrer une adresse email valide!")
        time.sleep(2)
        return
    
    print_red(f"\n[*] Démarrage de l'analyse pour: {email}\n")
    time.sleep(1)
    
    email_tracker(email)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_red("\n\n[!] Analyse interrompue par l'utilisateur.")
        sys.exit(0)
