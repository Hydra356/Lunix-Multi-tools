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
╦ ╦╔═╗╔╗ ╦ ╦╔═╗╔═╗╦╔═  ╦╔╗╔╔═╗╔═╗
║║║║╣ ╠╩╗╠═╣║ ║║ ║╠╩╗  ║║║║╠╣ ║ ║
╚╩╝╚═╝╚═╝╩ ╩╚═╝╚═╝╩ ╩  ╩╝╚╝╚  ╚═╝
    Informations sur Webhook Discord
    """
    return banner

def validate_webhook(webhook_url):
    """Valide l'URL du webhook Discord"""
    if not webhook_url.startswith('https://discord.com/api/webhooks/'):
        return False
    return True

def get_webhook_info(webhook_url):
    """Récupère les informations du webhook"""
    print_yellow("\n[~] Récupération des informations...", end="\r")
    
    try:
        response = requests.get(webhook_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print_green("[+] Webhook trouvé!")
            return {
                'success': True,
                'id': data.get('id', 'N/A'),
                'token': data.get('token', 'N/A'),
                'name': data.get('name', 'N/A'),
                'avatar': data.get('avatar', 'N/A'),
                'channel_id': data.get('channel_id', 'N/A'),
                'guild_id': data.get('guild_id', 'N/A'),
                'type': data.get('type', 'N/A'),
                'url': data.get('url', webhook_url),
            }
        elif response.status_code == 404:
            print_red("[!] Webhook introuvable ou supprimé")
            return {'success': False, 'error': 'Webhook not found'}
        else:
            print_red(f"[!] Erreur {response.status_code}")
            return {'success': False, 'error': f'HTTP {response.status_code}'}
            
    except Exception as e:
        print_red(f"[!] Erreur: {str(e)}")
        return {'success': False, 'error': str(e)}

def test_webhook(webhook_url):
    """Teste si le webhook est fonctionnel"""
    print_yellow("\n[~] Test du webhook...", end="\r")
    
    try:
        payload = {
            'content': '🔴 Test depuis Lunix OSINT Tool',
            'username': 'Lunix'
        }
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        if response.status_code == 204:
            print_green("[+] Webhook fonctionnel! Message envoyé")
            return True
        else:
            print_red(f"[!] Échec du test (Code: {response.status_code})")
            return False
            
    except Exception as e:
        print_red(f"[!] Erreur lors du test: {str(e)}")
        return False

def delete_webhook(webhook_url):
    """Supprime le webhook"""
    print_red("\n[!] ATTENTION: Cette action est IRRÉVERSIBLE!")
    confirm = input(f"{YELLOW}[*] Êtes-vous sûr de vouloir SUPPRIMER ce webhook? (oui/non): {RESET}").strip().lower()
    
    if confirm != 'oui':
        print_yellow("\n[*] Suppression annulée")
        return False
    
    print_yellow("\n[~] Suppression du webhook...", end="\r")
    
    try:
        response = requests.delete(webhook_url, timeout=10)
        
        if response.status_code == 204:
            print_green("[+] Webhook supprimé avec succès!")
            return True
        else:
            print_red(f"[!] Échec de la suppression (Code: {response.status_code})")
            return False
            
    except Exception as e:
        print_red(f"[!] Erreur: {str(e)}")
        return False

def webhook_info(webhook_url):
    """Fonction principale d'analyse de webhook"""
    
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70)
    print_red(f"  Webhook: {webhook_url[:50]}...")
    print_red(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print_red("="*70 + "\n")
    
    # Validation
    if not validate_webhook(webhook_url):
        print_red("[!] URL de webhook invalide!")
        print_yellow("\n[*] Format attendu: https://discord.com/api/webhooks/...")
        return
    
    print_green("[+] Format de webhook valide")
    
    # Récupération des informations
    info = get_webhook_info(webhook_url)
    
    if not info['success']:
        print_red(f"\n[!] Impossible de récupérer les informations: {info.get('error', 'Unknown')}")
        return
    
    # Affichage des informations
    print_red("\n" + "="*70)
    print_red("                    INFORMATIONS DU WEBHOOK")
    print_red("="*70)
    
    print_magenta("\n┌─ IDENTIFIANTS")
    print_cyan(f"│ ID: {info['id']}")
    print_cyan(f"│ Token: {info['token'][:20]}..." if len(info['token']) > 20 else f"│ Token: {info['token']}")
    print_cyan(f"│ Type: {info['type']}")
    
    print_magenta("\n┌─ CONFIGURATION")
    print_cyan(f"│ Nom: {info['name']}")
    print_cyan(f"│ Avatar: {info['avatar'] or 'Aucun'}")
    
    print_magenta("\n┌─ LOCALISATION")
    print_cyan(f"│ ID du serveur: {info['guild_id']}")
    print_cyan(f"│ ID du salon: {info['channel_id']}")
    
    print_magenta("\n┌─ URL")
    print_cyan(f"│ {info['url']}")
    
    # Menu d'actions
    print_red("\n" + "="*70)
    print_red("                        ACTIONS")
    print_red("="*70)
    print_yellow("\n[*] Actions disponibles:")
    print_cyan("  [1] Tester le webhook (envoyer un message)")
    print_cyan("  [2] Supprimer le webhook")
    print_cyan("  [3] Sauvegarder les informations")
    print_cyan("  [0] Retour")
    
    while True:
        print_red("\n" + "="*70)
        action = input(f"{RED}[Action]~$ {RESET}").strip()
        
        if action == "1":
            test_webhook(webhook_url)
        elif action == "2":
            if delete_webhook(webhook_url):
                print_yellow("\n[*] Le webhook a été supprimé. Retour au menu...")
                time.sleep(2)
                break
        elif action == "3":
            save_results(webhook_url, info)
        elif action == "0":
            break
        else:
            print_red("[!] Action invalide!")
    
    print_red("\n" + "="*70 + "\n")

def save_results(webhook_url, info):
    """Sauvegarde les informations dans un fichier"""
    try:
        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        webhook_id = info['id']
        filename = f"{results_dir}/webhook_{webhook_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("  LUNIX - WEBHOOK INFO RESULTS\n")
            f.write(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")
            
            f.write("IDENTIFIANTS\n")
            f.write("-" * 70 + "\n")
            f.write(f"ID: {info['id']}\n")
            f.write(f"Token: {info['token']}\n")
            f.write(f"Type: {info['type']}\n\n")
            
            f.write("CONFIGURATION\n")
            f.write("-" * 70 + "\n")
            f.write(f"Nom: {info['name']}\n")
            f.write(f"Avatar: {info['avatar'] or 'Aucun'}\n\n")
            
            f.write("LOCALISATION\n")
            f.write("-" * 70 + "\n")
            f.write(f"ID du serveur: {info['guild_id']}\n")
            f.write(f"ID du salon: {info['channel_id']}\n\n")
            
            f.write("URL\n")
            f.write("-" * 70 + "\n")
            f.write(f"{info['url']}\n")
        
        print_green(f"\n[+] Informations sauvegardées dans: {filename}")
        
    except Exception as e:
        print_red(f"\n[!] Erreur lors de la sauvegarde: {str(e)}")

def main():
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70 + "\n")
    
    print_yellow("[*] Collez l'URL du webhook Discord à analyser\n")
    
    webhook_url = input(f"{RED}[*] URL du webhook: {RESET}").strip()
    
    if not webhook_url:
        print_red("\n[!] Erreur: Veuillez entrer une URL valide!")
        time.sleep(2)
        return
    
    print_red(f"\n[*] Analyse du webhook...\n")
    time.sleep(1)
    
    webhook_info(webhook_url)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_red("\n\n[!] Analyse interrompue par l'utilisateur.")
        sys.exit(0)
