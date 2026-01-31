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
╦╔═╗  ╦  ╔═╗╔═╗╦╔═╦ ╦╔═╗
║╠═╝  ║  ║ ║║ ║╠╩╗║ ║╠═╝
╩╩    ╩═╝╚═╝╚═╝╩ ╩╚═╝╩  
  Localisation et Informations IP
    """
    return banner

def validate_ip(ip):
    """Valide le format de l'adresse IP"""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    
    # Vérifie que chaque octet est entre 0 et 255
    octets = ip.split('.')
    for octet in octets:
        if int(octet) > 255:
            return False
    
    return True

def is_private_ip(ip):
    """Vérifie si l'IP est privée"""
    octets = list(map(int, ip.split('.')))
    
    # 10.0.0.0 - 10.255.255.255
    if octets[0] == 10:
        return True
    
    # 172.16.0.0 - 172.31.255.255
    if octets[0] == 172 and 16 <= octets[1] <= 31:
        return True
    
    # 192.168.0.0 - 192.168.255.255
    if octets[0] == 192 and octets[1] == 168:
        return True
    
    # 127.0.0.0 - 127.255.255.255 (localhost)
    if octets[0] == 127:
        return True
    
    return False

def get_ip_info(ip):
    """Récupère les informations de l'IP via une API gratuite"""
    print_yellow("\n[~] Récupération des informations...", end="\r")
    
    try:
        # Utilisation de l'API ip-api.com (gratuite, limite: 45 req/min)
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data['status'] == 'success':
                print_green("[+] Informations récupérées avec succès!")
                return {
                    'success': True,
                    'country': data.get('country', 'N/A'),
                    'country_code': data.get('countryCode', 'N/A'),
                    'region': data.get('regionName', 'N/A'),
                    'city': data.get('city', 'N/A'),
                    'zip': data.get('zip', 'N/A'),
                    'lat': data.get('lat', 'N/A'),
                    'lon': data.get('lon', 'N/A'),
                    'timezone': data.get('timezone', 'N/A'),
                    'isp': data.get('isp', 'N/A'),
                    'org': data.get('org', 'N/A'),
                    'as': data.get('as', 'N/A'),
                }
            else:
                print_red("[!] Impossible de récupérer les informations")
                return {'success': False, 'error': data.get('message', 'Unknown error')}
        else:
            print_red("[!] Erreur lors de la requête API")
            return {'success': False, 'error': 'API request failed'}
            
    except requests.exceptions.Timeout:
        print_red("[!] Timeout lors de la requête")
        return {'success': False, 'error': 'Request timeout'}
    except Exception as e:
        print_red(f"[!] Erreur: {str(e)}")
        return {'success': False, 'error': str(e)}

def ip_lookup(ip):
    """Fonction principale de lookup IP"""
    
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70)
    print_red(f"  Adresse IP analysée: {ip}")
    print_red(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print_red("="*70 + "\n")
    
    # Validation
    if not validate_ip(ip):
        print_red("[!] Format d'adresse IP invalide!")
        print_yellow("\n[*] Format attendu: xxx.xxx.xxx.xxx (ex: 8.8.8.8)")
        return
    
    print_green("[+] Format d'adresse IP valide")
    
    # Vérification IP privée
    if is_private_ip(ip):
        print_red("\n" + "="*70)
        print_red("                    TYPE D'ADRESSE")
        print_red("="*70)
        print_yellow("\n[!] Cette adresse IP est PRIVÉE (réseau local)")
        print_cyan("\n  Plages d'IP privées:")
        print_cyan("  • 10.0.0.0 - 10.255.255.255")
        print_cyan("  • 172.16.0.0 - 172.31.255.255")
        print_cyan("  • 192.168.0.0 - 192.168.255.255")
        print_cyan("  • 127.0.0.0 - 127.255.255.255 (localhost)")
        print_yellow("\n[*] Les IPs privées ne peuvent pas être géolocalisées")
        print_red("\n" + "="*70 + "\n")
        return
    
    print_cyan("\n[+] Adresse IP publique détectée")
    
    # Récupération des informations
    info = get_ip_info(ip)
    
    if not info['success']:
        print_red(f"\n[!] Erreur: {info.get('error', 'Unknown error')}")
        return
    
    # Affichage des résultats
    print_red("\n" + "="*70)
    print_red("                    LOCALISATION")
    print_red("="*70)
    print_cyan(f"\n  Pays: {info['country']} ({info['country_code']})")
    print_cyan(f"  Région: {info['region']}")
    print_cyan(f"  Ville: {info['city']}")
    print_cyan(f"  Code postal: {info['zip']}")
    print_cyan(f"  Fuseau horaire: {info['timezone']}")
    
    print_red("\n" + "="*70)
    print_red("                    COORDONNÉES GPS")
    print_red("="*70)
    print_cyan(f"\n  Latitude: {info['lat']}")
    print_cyan(f"  Longitude: {info['lon']}")
    print_cyan(f"  Google Maps: https://www.google.com/maps?q={info['lat']},{info['lon']}")
    
    print_red("\n" + "="*70)
    print_red("                    FOURNISSEUR D'ACCÈS")
    print_red("="*70)
    print_cyan(f"\n  ISP: {info['isp']}")
    print_cyan(f"  Organisation: {info['org']}")
    print_cyan(f"  AS: {info['as']}")
    
    # Sauvegarde
    save_results(ip, info)
    
    print_red("\n" + "="*70 + "\n")

def save_results(ip, info):
    """Sauvegarde les résultats dans un fichier"""
    try:
        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        safe_ip = ip.replace('.', '_')
        filename = f"{results_dir}/ip_{safe_ip}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("  LUNIX - IP LOOKUP RESULTS\n")
            f.write(f"  IP: {ip}\n")
            f.write(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")
            
            f.write("LOCALISATION\n")
            f.write("-" * 70 + "\n")
            f.write(f"Pays: {info['country']} ({info['country_code']})\n")
            f.write(f"Région: {info['region']}\n")
            f.write(f"Ville: {info['city']}\n")
            f.write(f"Code postal: {info['zip']}\n")
            f.write(f"Fuseau horaire: {info['timezone']}\n\n")
            
            f.write("COORDONNÉES GPS\n")
            f.write("-" * 70 + "\n")
            f.write(f"Latitude: {info['lat']}\n")
            f.write(f"Longitude: {info['lon']}\n")
            f.write(f"Google Maps: https://www.google.com/maps?q={info['lat']},{info['lon']}\n\n")
            
            f.write("FOURNISSEUR D'ACCÈS\n")
            f.write("-" * 70 + "\n")
            f.write(f"ISP: {info['isp']}\n")
            f.write(f"Organisation: {info['org']}\n")
            f.write(f"AS: {info['as']}\n")
        
        print_green(f"[+] Résultats sauvegardés dans: {filename}")
        
    except Exception as e:
        print_red(f"[!] Erreur lors de la sauvegarde: {str(e)}")

def main():
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70 + "\n")
    
    ip = input(f"{RED}[*] Entrez l'adresse IP à analyser: {RESET}").strip()
    
    if not ip:
        print_red("\n[!] Erreur: Veuillez entrer une adresse IP valide!")
        time.sleep(2)
        return
    
    print_red(f"\n[*] Démarrage de l'analyse...\n")
    time.sleep(1)
    
    ip_lookup(ip)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_red("\n\n[!] Analyse interrompue par l'utilisateur.")
        sys.exit(0)
