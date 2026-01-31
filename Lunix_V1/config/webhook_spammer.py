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
╦ ╦╔═╗╔╗ ╦ ╦╔═╗╔═╗╦╔═  ╔═╗╔═╗╔═╗╔╦╗╔╦╗╔═╗╦═╗
║║║║╣ ╠╩╗╠═╣║ ║║ ║╠╩╗  ╚═╗╠═╝╠═╣║║║║║║║╣ ╠╦╝
╚╩╝╚═╝╚═╝╩ ╩╚═╝╚═╝╩ ╩  ╚═╝╩  ╩ ╩╩ ╩╩ ╩╚═╝╩╚═
    Spam de Messages via Webhook Discord
    """
    return banner

def validate_webhook(webhook_url):
    """Valide l'URL du webhook Discord"""
    if not webhook_url.startswith('https://discord.com/api/webhooks/'):
        return False
    return True

def send_message(webhook_url, content, username=None, avatar_url=None):
    """Envoie un message via le webhook"""
    try:
        payload = {'content': content}
        
        if username:
            payload['username'] = username
        if avatar_url:
            payload['avatar_url'] = avatar_url
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        if response.status_code == 204:
            return {'success': True}
        elif response.status_code == 429:
            retry_after = response.json().get('retry_after', 1)
            return {'success': False, 'error': 'Rate Limited', 'retry_after': retry_after}
        else:
            return {'success': False, 'error': f'HTTP {response.status_code}'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

def webhook_spam(webhook_url, message, count, delay, username=None, avatar_url=None):
    """Fonction principale de spam"""
    
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70)
    print_red(f"  Webhook: {webhook_url[:50]}...")
    print_red(f"  Messages: {count}")
    print_red(f"  Délai: {delay}s")
    print_red(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print_red("="*70 + "\n")
    
    # Validation
    if not validate_webhook(webhook_url):
        print_red("[!] URL de webhook invalide!")
        print_yellow("\n[*] Format attendu: https://discord.com/api/webhooks/...")
        return
    
    print_green("[+] Webhook valide")
    
    # Avertissement
    print_red("\n" + "="*70)
    print_red("                        AVERTISSEMENT")
    print_red("="*70)
    print_yellow("\n[!] Le spam de webhooks peut entraîner:")
    print_cyan("  • Suppression automatique du webhook par Discord")
    print_cyan("  • Bannissement du serveur")
    print_cyan("  • Rate limiting (limitation de débit)")
    print_yellow("\n[!] Utilisez cet outil de manière responsable")
    print_red("="*70 + "\n")
    
    confirm = input(f"{YELLOW}[*] Continuer? (oui/non): {RESET}").strip().lower()
    
    if confirm != 'oui':
        print_red("\n[*] Spam annulé")
        time.sleep(1)
        return
    
    # Début du spam
    print_red("\n" + "="*70)
    print_red("                    DÉBUT DU SPAM")
    print_red("="*70 + "\n")
    
    print_yellow(f"[*] Envoi de {count} messages...\n")
    time.sleep(1)
    
    sent = 0
    failed = 0
    rate_limited = 0
    
    for i in range(count):
        result = send_message(webhook_url, message, username, avatar_url)
        
        if result['success']:
            sent += 1
            print_green(f"[+] Message {i+1}/{count} envoyé")
        else:
            failed += 1
            error = result.get('error', 'Unknown')
            
            if error == 'Rate Limited':
                rate_limited += 1
                retry_after = result.get('retry_after', delay)
                print_red(f"[!] Rate limit! Attente de {retry_after}s...")
                time.sleep(retry_after)
                
                # Réessayer
                result = send_message(webhook_url, message, username, avatar_url)
                if result['success']:
                    sent += 1
                    failed -= 1
                    print_green(f"[+] Message {i+1}/{count} envoyé (retry)")
            else:
                print_red(f"[!] Échec {i+1}/{count}: {error}")
        
        # Délai entre les messages
        if i < count - 1:
            time.sleep(delay)
    
    # Résumé
    print_red("\n" + "="*70)
    print_red("                    RÉSUMÉ DU SPAM")
    print_red("="*70 + "\n")
    
    print_green(f"[+] Messages envoyés: {sent}/{count}")
    if failed > 0:
        print_red(f"[-] Messages échoués: {failed}/{count}")
    if rate_limited > 0:
        print_yellow(f"[!] Rate limits rencontrés: {rate_limited}")
    
    success_rate = (sent / count * 100) if count > 0 else 0
    print_cyan(f"\n[*] Taux de succès: {success_rate:.1f}%")
    
    print_red("\n" + "="*70 + "\n")

def main():
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70 + "\n")
    
    print_yellow("[!] AVERTISSEMENT IMPORTANT")
    print_red("─" * 70)
    print_cyan("Le spam est une violation des conditions d'utilisation de Discord.")
    print_cyan("Cet outil est fourni à des fins ÉDUCATIVES uniquement.")
    print_cyan("Vous êtes entièrement responsable de vos actions.")
    print_red("─" * 70)
    
    # Configuration
    print_red("\n" + "="*70)
    print_red("                        CONFIGURATION")
    print_red("="*70 + "\n")
    
    webhook_url = input(f"{CYAN}[*] URL du webhook: {RESET}").strip()
    
    if not webhook_url:
        print_red("\n[!] URL requise!")
        time.sleep(2)
        return
    
    message = input(f"{CYAN}[*] Message à envoyer: {RESET}").strip()
    
    if not message:
        print_red("\n[!] Message requis!")
        time.sleep(2)
        return
    
    try:
        count = int(input(f"{CYAN}[*] Nombre de messages: {RESET}").strip())
        
        if count <= 0:
            print_red("\n[!] Le nombre doit être positif!")
            time.sleep(2)
            return
        
        if count > 1000:
            print_yellow("\n[!] Attention: Plus de 1000 messages peuvent causer un rate limit sévère")
            confirm = input(f"{YELLOW}[*] Continuer? (o/n): {RESET}").strip().lower()
            if confirm != 'o' and confirm != 'oui':
                print_red("\n[*] Annulé")
                time.sleep(1)
                return
        
        delay = float(input(f"{CYAN}[*] Délai entre messages (secondes, min 0.5): {RESET}").strip() or "1")
        
        if delay < 0.5:
            print_yellow("\n[!] Délai minimum: 0.5s (pour éviter le rate limit)")
            delay = 0.5
        
    except ValueError:
        print_red("\n[!] Valeur invalide!")
        time.sleep(2)
        return
    
    # Options avancées
    print_red("\n" + "="*70)
    print_red("                    OPTIONS AVANCÉES")
    print_red("="*70)
    
    advanced = input(f"\n{YELLOW}[*] Configurer username/avatar? (o/n): {RESET}").strip().lower()
    
    username = None
    avatar_url = None
    
    if advanced == 'o' or advanced == 'oui':
        username = input(f"{CYAN}[*] Username (laisser vide pour défaut): {RESET}").strip() or None
        avatar_url = input(f"{CYAN}[*] URL de l'avatar (laisser vide pour défaut): {RESET}").strip() or None
    
    print_red(f"\n[*] Préparation du spam...\n")
    time.sleep(1)
    
    webhook_spam(webhook_url, message, count, delay, username, avatar_url)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_red("\n\n[!] Spam interrompu par l'utilisateur.")
        sys.exit(0)
