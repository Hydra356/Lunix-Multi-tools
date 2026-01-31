import os
import sys
import time
import re
import requests
import socket
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
╔╦╗╔═╗╔╦╗╔═╗╦╔╗╔  ╦╔╗╔╔═╗╔═╗
 ║║║ ║║║║╠═╣║║║║  ║║║║╠╣ ║ ║
═╩╝╚═╝╩ ╩╩ ╩╩╝╚╝  ╩╝╚╝╚  ╚═╝
   Informations sur les Domaines
    """
    return banner

def validate_domain(domain):
    """Valide le format du domaine"""
    # Supprime http:// ou https://
    domain = re.sub(r'^https?://', '', domain)
    # Supprime les slashes finaux
    domain = domain.rstrip('/')
    
    # Pattern basique de validation de domaine
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$'
    
    return re.match(pattern, domain) is not None, domain

def get_ip_from_domain(domain):
    """Récupère l'IP associée au domaine"""
    try:
        print_yellow("[~] Résolution DNS...", end="\r")
        ip = socket.gethostbyname(domain)
        print_green(f"[+] IP trouvée: {ip}")
        return ip
    except socket.gaierror:
        print_red("[!] Impossible de résoudre le domaine")
        return None
    except Exception as e:
        print_red(f"[!] Erreur: {str(e)}")
        return None

def check_website_status(domain):
    """Vérifie si le site web est accessible"""
    try:
        print_yellow("[~] Vérification du statut...", end="\r")
        
        urls = [f'https://{domain}', f'http://{domain}']
        
        for url in urls:
            try:
                response = requests.get(url, timeout=5, allow_redirects=True)
                print_green(f"[+] Site accessible ({response.status_code})")
                return {
                    'accessible': True,
                    'status_code': response.status_code,
                    'url': url,
                    'final_url': response.url,
                    'server': response.headers.get('Server', 'N/A')
                }
            except:
                continue
        
        print_red("[!] Site non accessible")
        return {'accessible': False}
        
    except Exception as e:
        print_red(f"[!] Erreur: {str(e)}")
        return {'accessible': False, 'error': str(e)}

def extract_domain_parts(domain):
    """Extrait les différentes parties du domaine"""
    parts = domain.split('.')
    
    if len(parts) >= 2:
        tld = parts[-1]  # Top Level Domain
        sld = parts[-2]  # Second Level Domain
        subdomain = '.'.join(parts[:-2]) if len(parts) > 2 else None
        
        return {
            'full': domain,
            'tld': tld,
            'sld': sld,
            'subdomain': subdomain,
            'root': f"{sld}.{tld}"
        }
    
    return None

def get_common_subdomains(domain):
    """Liste des sous-domaines courants à vérifier"""
    common = ['www', 'mail', 'ftp', 'smtp', 'pop', 'ns1', 'ns2', 'admin', 'blog', 'shop', 'api']
    
    return [f"{sub}.{domain}" for sub in common]

def domain_info(domain):
    """Fonction principale d'analyse de domaine"""
    
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70)
    print_red(f"  Domaine analysé: {domain}")
    print_red(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print_red("="*70 + "\n")
    
    # Validation et nettoyage
    is_valid, clean_domain = validate_domain(domain)
    
    if not is_valid:
        print_red("[!] Format de domaine invalide!")
        print_yellow("\n[*] Format attendu: example.com ou subdomain.example.com")
        return
    
    print_green(f"[+] Format valide: {clean_domain}")
    domain = clean_domain
    
    # Extraction des parties du domaine
    parts = extract_domain_parts(domain)
    
    if parts:
        print_red("\n" + "="*70)
        print_red("                    STRUCTURE DU DOMAINE")
        print_red("="*70)
        print_cyan(f"\n  Domaine complet: {parts['full']}")
        print_cyan(f"  Domaine racine: {parts['root']}")
        print_cyan(f"  TLD (extension): .{parts['tld']}")
        print_cyan(f"  SLD: {parts['sld']}")
        if parts['subdomain']:
            print_cyan(f"  Sous-domaine: {parts['subdomain']}")
        else:
            print_cyan("  Sous-domaine: Aucun")
    
    # Résolution DNS
    print_red("\n" + "="*70)
    print_red("                    RÉSOLUTION DNS")
    print_red("="*70 + "\n")
    ip = get_ip_from_domain(domain)
    
    if ip:
        print_cyan(f"  Adresse IP: {ip}")
    
    # Statut du site web
    print_red("\n" + "="*70)
    print_red("                    STATUT DU SITE WEB")
    print_red("="*70 + "\n")
    status = check_website_status(domain)
    
    if status['accessible']:
        print_cyan(f"  Statut: Accessible")
        print_cyan(f"  Code HTTP: {status['status_code']}")
        print_cyan(f"  URL testée: {status['url']}")
        if status['url'] != status['final_url']:
            print_cyan(f"  Redirige vers: {status['final_url']}")
        print_cyan(f"  Serveur: {status['server']}")
    else:
        print_cyan("  Statut: Non accessible ou hors ligne")
    
    # Sous-domaines courants
    print_red("\n" + "="*70)
    print_red("                    SOUS-DOMAINES COURANTS")
    print_red("="*70)
    print_yellow("\n[*] Sous-domaines à vérifier manuellement:")
    
    subdomains = get_common_subdomains(parts['root'] if parts else domain)
    for sub in subdomains[:5]:  # Affiche les 5 premiers
        print_cyan(f"  • {sub}")
    print_cyan("  • ...")
    
    # Sauvegarde
    save_results(domain, parts, ip, status)
    
    print_red("\n" + "="*70 + "\n")

def save_results(domain, parts, ip, status):
    """Sauvegarde les résultats dans un fichier"""
    try:
        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        safe_domain = domain.replace('.', '_')
        filename = f"{results_dir}/domain_{safe_domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("  LUNIX - DOMAIN INFO RESULTS\n")
            f.write(f"  Domaine: {domain}\n")
            f.write(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")
            
            if parts:
                f.write("STRUCTURE DU DOMAINE\n")
                f.write("-" * 70 + "\n")
                f.write(f"Domaine complet: {parts['full']}\n")
                f.write(f"Domaine racine: {parts['root']}\n")
                f.write(f"TLD: .{parts['tld']}\n")
                f.write(f"SLD: {parts['sld']}\n")
                f.write(f"Sous-domaine: {parts['subdomain'] or 'Aucun'}\n\n")
            
            f.write("RÉSOLUTION DNS\n")
            f.write("-" * 70 + "\n")
            f.write(f"Adresse IP: {ip or 'Non résolu'}\n\n")
            
            f.write("STATUT DU SITE WEB\n")
            f.write("-" * 70 + "\n")
            if status['accessible']:
                f.write(f"Statut: Accessible\n")
                f.write(f"Code HTTP: {status['status_code']}\n")
                f.write(f"URL: {status['url']}\n")
                f.write(f"Serveur: {status['server']}\n")
            else:
                f.write("Statut: Non accessible\n")
        
        print_green(f"[+] Résultats sauvegardés dans: {filename}")
        
    except Exception as e:
        print_red(f"[!] Erreur lors de la sauvegarde: {str(e)}")

def main():
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70 + "\n")
    
    domain = input(f"{RED}[*] Entrez le domaine à analyser: {RESET}").strip()
    
    if not domain:
        print_red("\n[!] Erreur: Veuillez entrer un domaine valide!")
        time.sleep(2)
        return
    
    print_red(f"\n[*] Démarrage de l'analyse...\n")
    time.sleep(1)
    
    domain_info(domain)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_red("\n\n[!] Analyse interrompue par l'utilisateur.")
        sys.exit(0)
