import os
import sys
import time
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

def print_yellow(text, end='\n'):
    print(f"{YELLOW}{text}{RESET}", end=end)

def print_cyan(text):
    print(f"{CYAN}{text}{RESET}")

def print_magenta(text):
    print(f"{MAGENTA}{text}{RESET}")

def ascii_banner():
    banner = """
╔╗ ╦═╗╔═╗╔═╗╔═╗╦ ╦  ╔═╗╔═╗╔═╗╦═╗╔═╗╦ ╦
╠╩╗╠╦╝║╣ ╠═╣║  ╠═╣  ╚═╗║╣ ╠═╣╠╦╝║  ╠═╣
╚═╝╩╚═╚═╝╩ ╩╚═╝╩ ╩  ╚═╝╚═╝╩ ╩╩╚═╚═╝╩ ╩
   Recherche dans les Bases de Fuites
    """
    return banner

# Fuites de données célèbres (exemples historiques)
FAMOUS_BREACHES = [
    {
        'name': 'LinkedIn (2012)',
        'records': '165 millions',
        'type': 'Email, Mots de passe',
        'description': 'Fuite massive de données utilisateurs LinkedIn'
    },
    {
        'name': 'Yahoo (2013-2014)',
        'records': '3 milliards',
        'type': 'Noms, emails, mots de passe, numéros',
        'description': 'La plus grande fuite de données de l\'histoire'
    },
    {
        'name': 'Facebook (2019)',
        'records': '533 millions',
        'type': 'Téléphones, noms, IDs',
        'description': 'Données scraped de profils publics'
    },
    {
        'name': 'Adobe (2013)',
        'records': '153 millions',
        'type': 'Emails, mots de passe, indices',
        'description': 'Fuite de la base utilisateurs Adobe'
    },
    {
        'name': 'MySpace (2016)',
        'records': '360 millions',
        'type': 'Emails, usernames, mots de passe',
        'description': 'Ancienne base de données MySpace'
    },
    {
        'name': 'Dropbox (2012)',
        'records': '68 millions',
        'type': 'Emails, mots de passe hachés',
        'description': 'Fuite de comptes Dropbox'
    },
    {
        'name': 'Tumblr (2013)',
        'records': '65 millions',
        'type': 'Emails, mots de passe',
        'description': 'Base de données Tumblr compromise'
    },
    {
        'name': 'Marriott/Starwood (2018)',
        'records': '500 millions',
        'type': 'Noms, adresses, passeports, cartes',
        'description': 'Données clients hôtels'
    },
]

def check_haveibeenpwned_email(email):
    """Vérifie si l'email apparaît dans HaveIBeenPwned"""
    print_yellow("\n[~] Vérification sur HaveIBeenPwned...", end="\r")
    
    try:
        url = f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}'
        headers = {
            'User-Agent': 'Lunix-OSINT-Tool'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            breaches = response.json()
            print_red(f"[!] {len(breaches)} fuites trouvées!")
            return breaches
        elif response.status_code == 404:
            print_green("[+] Aucune fuite trouvée")
            return []
        else:
            print_red(f"[!] Erreur {response.status_code}")
            return None
            
    except Exception as e:
        print_red(f"[!] Erreur: {str(e)}")
        print_yellow("[*] Vérification manuelle recommandée sur: https://haveibeenpwned.com/")
        return None

def display_breach_info(breach):
    """Affiche les détails d'une fuite"""
    print_magenta(f"\n  ┌─ {breach.get('Name', 'Unknown')}")
    print_cyan(f"  │ Date: {breach.get('BreachDate', 'N/A')}")
    print_cyan(f"  │ Comptes compromis: {breach.get('PwnCount', 'N/A'):,}")
    print_cyan(f"  │ Données exposées: {', '.join(breach.get('DataClasses', []))}")
    print_cyan(f"  │ Description: {breach.get('Description', 'N/A')[:80]}...")
    print_cyan(f"  └─ Vérifié: {'Oui' if breach.get('IsVerified') else 'Non'}")

def breach_search(query):
    """Fonction principale de recherche de fuites"""
    
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70)
    print_red(f"  Recherche: {query}")
    print_red(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print_red("="*70 + "\n")
    
    # Détection du type de recherche
    if '@' in query:
        search_type = "email"
        print_cyan("[*] Type de recherche: Email")
    else:
        search_type = "general"
        print_cyan("[*] Type de recherche: Général")
    
    # Recherche HaveIBeenPwned pour emails
    if search_type == "email":
        print_red("\n" + "="*70)
        print_red("                  VÉRIFICATION HAVEIBEENPWNED")
        print_red("="*70)
        
        breaches = check_haveibeenpwned_email(query)
        
        if breaches and len(breaches) > 0:
            print_red(f"\n[!] ALERTE: {len(breaches)} fuites trouvées pour cet email!\n")
            
            for breach in breaches[:10]:  # Limite à 10 pour l'affichage
                display_breach_info(breach)
            
            if len(breaches) > 10:
                print_yellow(f"\n[*] ... et {len(breaches) - 10} autres fuites")
            
            save_breach_results(query, breaches)
        elif breaches is not None and len(breaches) == 0:
            print_green("\n[✓] Bonne nouvelle! Cet email n'apparaît dans aucune fuite connue")
            print_cyan("[*] Continuez à surveiller régulièrement")
    
    # Affichage des fuites célèbres
    print_red("\n" + "="*70)
    print_red("                  FUITES CÉLÈBRES (HISTORIQUE)")
    print_red("="*70)
    print_yellow("\n[*] Quelques-unes des plus grandes fuites de l'histoire:\n")
    
    for breach in FAMOUS_BREACHES[:5]:
        print_magenta(f"  • {breach['name']}")
        print_cyan(f"    └─ {breach['records']} comptes | {breach['type']}")
    
    # Conseils
    print_red("\n" + "="*70)
    print_red("                     QUE FAIRE EN CAS DE FUITE?")
    print_red("="*70)
    print_yellow("\n[*] Actions recommandées:")
    print_cyan("  1. Changez IMMÉDIATEMENT votre mot de passe")
    print_cyan("  2. Activez l'authentification à 2 facteurs (2FA)")
    print_cyan("  3. Vérifiez l'activité suspecte sur vos comptes")
    print_cyan("  4. Surveillez vos relevés bancaires")
    print_cyan("  5. Utilisez des mots de passe uniques pour chaque service")
    print_cyan("  6. Envisagez un gestionnaire de mots de passe")
    
    print_red("\n" + "="*70 + "\n")

def save_breach_results(email, breaches):
    """Sauvegarde les résultats dans un fichier"""
    try:
        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        safe_email = email.replace('@', '_at_').replace('.', '_')
        filename = f"{results_dir}/breach_{safe_email}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("  LUNIX - BREACH SEARCH RESULTS\n")
            f.write(f"  Email: {email}\n")
            f.write(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"NOMBRE DE FUITES TROUVÉES: {len(breaches)}\n\n")
            
            for breach in breaches:
                f.write(f"[{breach.get('Name', 'Unknown')}]\n")
                f.write(f"Date: {breach.get('BreachDate', 'N/A')}\n")
                f.write(f"Comptes compromis: {breach.get('PwnCount', 'N/A'):,}\n")
                f.write(f"Données exposées: {', '.join(breach.get('DataClasses', []))}\n")
                f.write(f"Description: {breach.get('Description', 'N/A')}\n")
                f.write("\n")
        
        print_green(f"[+] Résultats sauvegardés dans: {filename}")
        
    except Exception as e:
        print_red(f"[!] Erreur lors de la sauvegarde: {str(e)}")

def main():
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70 + "\n")
    
    query = input(f"{RED}[*] Entrez un email ou terme à rechercher: {RESET}").strip()
    
    if not query:
        print_red("\n[!] Erreur: Veuillez entrer une valeur valide!")
        time.sleep(2)
        return
    
    print_red(f"\n[*] Démarrage de la recherche...\n")
    time.sleep(1)
    
    breach_search(query)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_red("\n\n[!] Recherche interrompue par l'utilisateur.")
        sys.exit(0)
