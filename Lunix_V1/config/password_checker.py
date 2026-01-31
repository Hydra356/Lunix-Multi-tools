import os
import sys
import time
import hashlib
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
╔═╗╔═╗╔═╗╔═╗╦ ╦╔═╗╦═╗╔╦╗  ╔═╗╦ ╦╔═╗╔═╗╦╔═
╠═╝╠═╣╚═╗╚═╗║║║║ ║╠╦╝ ║║  ║  ╠═╣║╣ ║  ╠╩╗
╩  ╩ ╩╚═╝╚═╝╚╩╝╚═╝╩╚══╩╝  ╚═╝╩ ╩╚═╝╚═╝╩ ╩
   Vérification de Fuites de Mots de Passe
    """
    return banner

def check_password_strength(password):
    """Analyse la force du mot de passe"""
    score = 0
    feedback = []
    
    # Longueur
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Trop court (minimum 8 caractères)")
    
    if len(password) >= 12:
        score += 1
    
    # Complexité
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Manque de minuscules")
    
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Manque de majuscules")
    
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Manque de chiffres")
    
    if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
        score += 1
    else:
        feedback.append("Manque de caractères spéciaux")
    
    # Évaluation
    if score <= 2:
        strength = "Très Faible"
        color = RED
    elif score <= 3:
        strength = "Faible"
        color = RED
    elif score <= 4:
        strength = "Moyen"
        color = YELLOW
    elif score <= 5:
        strength = "Bon"
        color = GREEN
    else:
        strength = "Excellent"
        color = GREEN
    
    return {
        'score': score,
        'max_score': 6,
        'strength': strength,
        'color': color,
        'feedback': feedback
    }

def check_haveibeenpwned(password):
    """Vérifie si le mot de passe apparaît dans HaveIBeenPwned (k-anonymity)"""
    print_yellow("\n[~] Vérification dans la base HaveIBeenPwned...", end="\r")
    
    try:
        # Hash SHA-1 du mot de passe
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        
        # On n'envoie que les 5 premiers caractères (k-anonymity)
        prefix = sha1_hash[:5]
        suffix = sha1_hash[5:]
        
        # Requête à l'API HIBP
        url = f'https://api.pwnedpasswords.com/range/{prefix}'
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            # Cherche le suffixe dans les résultats
            hashes = response.text.split('\r\n')
            
            for h in hashes:
                hash_suffix, count = h.split(':')
                if hash_suffix == suffix:
                    print_red(f"[!] Mot de passe COMPROMIS! Trouvé {count} fois")
                    return {
                        'pwned': True,
                        'count': int(count)
                    }
            
            print_green("[+] Mot de passe NON trouvé dans les fuites")
            return {
                'pwned': False,
                'count': 0
            }
        else:
            print_red("[!] Erreur lors de la vérification")
            return {'error': True}
            
    except Exception as e:
        print_red(f"[!] Erreur: {str(e)}")
        return {'error': True, 'message': str(e)}

def generate_hash_info(password):
    """Génère différents hashes du mot de passe"""
    hashes = {
        'MD5': hashlib.md5(password.encode()).hexdigest(),
        'SHA1': hashlib.sha1(password.encode()).hexdigest(),
        'SHA256': hashlib.sha256(password.encode()).hexdigest(),
        'SHA512': hashlib.sha512(password.encode()).hexdigest()
    }
    return hashes

def password_check(password):
    """Fonction principale de vérification de mot de passe"""
    
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70)
    print_red(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print_red("="*70 + "\n")
    
    print_yellow("[*] ATTENTION: Votre mot de passe ne sera PAS sauvegardé")
    print_yellow("[*] La vérification utilise k-anonymity (sécurisé)\n")
    time.sleep(1)
    
    # Analyse de la force
    print_red("="*70)
    print_red("                    ANALYSE DE LA FORCE")
    print_red("="*70)
    
    strength = check_password_strength(password)
    
    print_cyan(f"\n  Longueur: {len(password)} caractères")
    print_cyan(f"  Score: {strength['score']}/{strength['max_score']}")
    print(f"  Force: {strength['color']}{strength['strength']}{RESET}")
    
    if strength['feedback']:
        print_yellow("\n  Recommandations:")
        for fb in strength['feedback']:
            print_cyan(f"    • {fb}")
    
    # Vérification des fuites
    print_red("\n" + "="*70)
    print_red("                  VÉRIFICATION DES FUITES")
    print_red("="*70)
    
    hibp_result = check_haveibeenpwned(password)
    
    if not hibp_result.get('error'):
        if hibp_result['pwned']:
            print_red(f"\n  ⚠️  ALERTE SÉCURITÉ ⚠️")
            print_red(f"  Ce mot de passe a été compromis!")
            print_red(f"  Trouvé {hibp_result['count']} fois dans des fuites de données")
            print_yellow("\n  ➜ CHANGEZ IMMÉDIATEMENT CE MOT DE PASSE")
        else:
            print_green("\n  ✓ Mot de passe non trouvé dans les fuites connues")
            print_cyan("  Cela ne garantit pas qu'il est sûr à 100%")
    
    # Informations de hash
    print_red("\n" + "="*70)
    print_red("                    HASHES DU MOT DE PASSE")
    print_red("="*70)
    print_yellow("\n[*] Hashes cryptographiques (à ne PAS partager):\n")
    
    hashes = generate_hash_info(password)
    for algo, hash_value in hashes.items():
        print_cyan(f"  {algo:8}: {hash_value}")
    
    # Conseils de sécurité
    print_red("\n" + "="*70)
    print_red("                    CONSEILS DE SÉCURITÉ")
    print_red("="*70)
    print_yellow("\n[*] Bonnes pratiques:")
    print_cyan("  • Utilisez un mot de passe unique pour chaque compte")
    print_cyan("  • Minimum 12 caractères avec majuscules, minuscules, chiffres et symboles")
    print_cyan("  • Utilisez un gestionnaire de mots de passe (Bitwarden, 1Password, etc.)")
    print_cyan("  • Activez l'authentification à deux facteurs (2FA)")
    print_cyan("  • Ne réutilisez JAMAIS un mot de passe compromis")
    print_cyan("  • Changez vos mots de passe régulièrement")
    
    print_red("\n" + "="*70 + "\n")

def main():
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70 + "\n")
    
    print_yellow("[*] Ce mot de passe ne sera PAS stocké sur le disque")
    print_yellow("[*] La vérification est effectuée de manière sécurisée\n")
    
    # Masquer le mot de passe pendant la saisie (ne fonctionne pas partout)
    import getpass
    try:
        password = getpass.getpass(f"{RED}[*] Entrez le mot de passe à vérifier: {RESET}")
    except:
        password = input(f"{RED}[*] Entrez le mot de passe à vérifier: {RESET}").strip()
    
    if not password:
        print_red("\n[!] Erreur: Veuillez entrer un mot de passe!")
        time.sleep(2)
        return
    
    print_red(f"\n[*] Démarrage de l'analyse...\n")
    time.sleep(1)
    
    password_check(password)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_red("\n\n[!] Analyse interrompue par l'utilisateur.")
        sys.exit(0)
