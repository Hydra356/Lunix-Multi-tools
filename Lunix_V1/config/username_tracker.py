import os
import sys
import time
import requests
from datetime import datetime

# Couleurs
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_red(text):
    print(f"{RED}{text}{RESET}")

def print_green(text):
    print(f"{GREEN}{text}{RESET}")

def print_yellow(text, end='\n'):
    print(f"{YELLOW}{text}{RESET}", end=end)

def ascii_banner():
    banner = """
╦ ╦╔═╗╔═╗╦═╗╔╗╔╔═╗╔╦╗╔═╗  ╔╦╗╦═╗╔═╗╔═╗╦╔═╔═╗╦═╗
║ ║╚═╗║╣ ╠╦╝║║║╠═╣║║║║╣    ║ ╠╦╝╠═╣║  ╠╩╗║╣ ╠╦╝
╚═╝╚═╝╚═╝╩╚═╝╚╝╩ ╩╩ ╩╚═╝   ╩ ╩╚═╩ ╩╚═╝╩ ╩╚═╝╩╚═
    Recherche de Username sur Réseaux Sociaux
    """
    return banner

# Liste des plateformes à vérifier
PLATFORMS = {
    "GitHub": "https://github.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "Twitter": "https://twitter.com/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Facebook": "https://www.facebook.com/{}",
    "LinkedIn": "https://www.linkedin.com/in/{}",
    "Pinterest": "https://www.pinterest.com/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "Discord": "https://discord.com/users/{}",
    "Telegram": "https://t.me/{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "Medium": "https://medium.com/@{}",
    "DeviantArt": "https://{}.deviantart.com",
    "Behance": "https://www.behance.net/{}",
    "Dribbble": "https://dribbble.com/{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "SoundCloud": "https://soundcloud.com/{}",
}

def check_username(username):
    """Vérifie la présence du username sur différentes plateformes"""
    
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70)
    print_red(f"  Username recherché: {username}")
    print_red(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print_red("="*70 + "\n")
    
    print_red("[*] Recherche en cours sur les réseaux sociaux...\n")
    time.sleep(0.5)
    
    found_platforms = []
    not_found_platforms = []
    
    for platform, url_template in PLATFORMS.items():
        url = url_template.format(username)
        
        try:
            print_yellow(f"[~] Vérification de {platform}...", end="\r")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
            
            # Analyse de la réponse
            if response.status_code == 200:
                print_green(f"[+] {platform:20} -> TROUVÉ! {url}")
                found_platforms.append((platform, url))
            else:
                print_red(f"[-] {platform:20} -> Non trouvé")
                not_found_platforms.append(platform)
                
            time.sleep(0.3)  # Délai pour éviter le rate limiting
            
        except requests.exceptions.Timeout:
            print_red(f"[!] {platform:20} -> Timeout")
            not_found_platforms.append(platform)
        except requests.exceptions.RequestException:
            print_red(f"[!] {platform:20} -> Erreur de connexion")
            not_found_platforms.append(platform)
    
    # Résumé
    print_red("\n" + "="*70)
    print_red("                         RÉSUMÉ DE LA RECHERCHE")
    print_red("="*70)
    print_green(f"\n[+] Profils trouvés: {len(found_platforms)}")
    print_red(f"[-] Profils non trouvés: {len(not_found_platforms)}")
    
    if found_platforms:
        print_red("\n" + "="*70)
        print_red("                     LIENS DES PROFILS TROUVÉS")
        print_red("="*70 + "\n")
        for platform, url in found_platforms:
            print_green(f"  [{platform}] {url}")
    
    # Sauvegarde des résultats
    save_results(username, found_platforms)
    
    print_red("\n" + "="*70 + "\n")

def save_results(username, found_platforms):
    """Sauvegarde les résultats dans un fichier"""
    try:
        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        filename = f"{results_dir}/username_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write(f"  LUNIX - USERNAME TRACKER RESULTS\n")
            f.write(f"  Username: {username}\n")
            f.write(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Profils trouvés: {len(found_platforms)}\n\n")
            
            for platform, url in found_platforms:
                f.write(f"[{platform}]\n{url}\n\n")
        
        print_green(f"[+] Résultats sauvegardés dans: {filename}")
        
    except Exception as e:
        print_red(f"[!] Erreur lors de la sauvegarde: {str(e)}")

def main():
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70 + "\n")
    
    username = input(f"{RED}[*] Entrez le username à rechercher: {RESET}").strip()
    
    if not username:
        print_red("\n[!] Erreur: Veuillez entrer un username valide!")
        time.sleep(2)
        return
    
    print_red(f"\n[*] Démarrage de la recherche pour: {username}\n")
    time.sleep(1)
    
    check_username(username)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_red("\n\n[!] Recherche interrompue par l'utilisateur.")
        sys.exit(0)
