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
╔═╗╔═╗╔═╗╦╔═╗╦    ╔═╗╦╔╗╔╔╦╗╔═╗╦═╗
╚═╗║ ║║  ║╠═╣║    ╠╣ ║║║║ ║║║╣ ╠╦╝
╚═╝╚═╝╚═╝╩╩ ╩╩═╝  ╚  ╩╝╚╝═╩╝╚═╝╩╚═
  Recherche Avancée de Profils Sociaux
    """
    return banner

# Liste étendue de plateformes sociales
SOCIAL_PLATFORMS = {
    # Réseaux sociaux principaux
    "Facebook": "https://www.facebook.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "Twitter/X": "https://twitter.com/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "LinkedIn": "https://www.linkedin.com/in/{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "Pinterest": "https://www.pinterest.com/{}",
    
    # Plateformes de contenu
    "YouTube": "https://www.youtube.com/@{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Vimeo": "https://vimeo.com/{}",
    "Dailymotion": "https://www.dailymotion.com/{}",
    
    # Plateformes professionnelles
    "GitHub": "https://github.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "Bitbucket": "https://bitbucket.org/{}",
    "Stack Overflow": "https://stackoverflow.com/users/{}",
    "Dev.to": "https://dev.to/{}",
    
    # Forums et communautés
    "Reddit": "https://www.reddit.com/user/{}",
    "Quora": "https://www.quora.com/profile/{}",
    "Medium": "https://medium.com/@{}",
    "Substack": "https://{}.substack.com",
    
    # Gaming
    "Steam": "https://steamcommunity.com/id/{}",
    "Xbox": "https://account.xbox.com/profile?gamertag={}",
    "PlayStation": "https://psnprofiles.com/{}",
    "Discord": "https://discord.com/users/{}",
    "Roblox": "https://www.roblox.com/users/{}",
    
    # Musique
    "Spotify": "https://open.spotify.com/user/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Bandcamp": "https://{}.bandcamp.com",
    "Apple Music": "https://music.apple.com/profile/{}",
    
    # Art et Design
    "DeviantArt": "https://{}.deviantart.com",
    "Behance": "https://www.behance.net/{}",
    "Dribbble": "https://dribbble.com/{}",
    "ArtStation": "https://www.artstation.com/{}",
    
    # Messagerie
    "Telegram": "https://t.me/{}",
    "WhatsApp": "https://wa.me/{}",
    "Signal": "signal://user/{}",
    
    # Autres
    "Patreon": "https://www.patreon.com/{}",
    "OnlyFans": "https://onlyfans.com/{}",
    "Linktree": "https://linktr.ee/{}",
    "Tumblr": "https://{}.tumblr.com",
    "Flickr": "https://www.flickr.com/people/{}",
    "500px": "https://500px.com/p/{}",
    "Goodreads": "https://www.goodreads.com/{}",
    "Letterboxd": "https://letterboxd.com/{}",
    "IMDb": "https://www.imdb.com/user/{}",
}

def search_social_media(identifier):
    """Recherche l'identifiant sur toutes les plateformes"""
    
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70)
    print_red(f"  Identifiant recherché: {identifier}")
    print_red(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print_red("="*70 + "\n")
    
    print_red(f"[*] Recherche en cours sur {len(SOCIAL_PLATFORMS)} plateformes...\n")
    time.sleep(0.5)
    
    found_profiles = []
    not_found = []
    
    for platform, url_template in SOCIAL_PLATFORMS.items():
        url = url_template.format(identifier)
        
        try:
            print_yellow(f"[~] {platform:25} ", end="")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
            
            # Analyse de la réponse
            if response.status_code == 200:
                print_green("✓ TROUVÉ")
                found_profiles.append((platform, url))
            else:
                print_red("✗ Non trouvé")
                not_found.append(platform)
                
            time.sleep(0.2)  # Délai pour éviter le rate limiting
            
        except requests.exceptions.Timeout:
            print_red("✗ Timeout")
            not_found.append(platform)
        except requests.exceptions.RequestException:
            print_red("✗ Erreur")
            not_found.append(platform)
    
    # Résumé
    print_red("\n" + "="*70)
    print_red("                         RÉSUMÉ DE LA RECHERCHE")
    print_red("="*70)
    print_green(f"\n[+] Profils trouvés: {len(found_profiles)}/{len(SOCIAL_PLATFORMS)}")
    print_red(f"[-] Profils non trouvés: {len(not_found)}/{len(SOCIAL_PLATFORMS)}")
    
    percentage = (len(found_profiles) / len(SOCIAL_PLATFORMS)) * 100
    print_cyan(f"[*] Taux de présence: {percentage:.1f}%")
    
    if found_profiles:
        print_red("\n" + "="*70)
        print_red("                     PROFILS TROUVÉS")
        print_red("="*70 + "\n")
        
        # Grouper par catégorie
        categories = {
            'Réseaux Sociaux': ['Facebook', 'Instagram', 'Twitter/X', 'TikTok', 'LinkedIn', 'Snapchat', 'Pinterest'],
            'Plateformes de Contenu': ['YouTube', 'Twitch', 'Vimeo', 'Dailymotion'],
            'Développement': ['GitHub', 'GitLab', 'Bitbucket', 'Stack Overflow', 'Dev.to'],
            'Forums': ['Reddit', 'Quora', 'Medium', 'Substack'],
            'Gaming': ['Steam', 'Xbox', 'PlayStation', 'Discord', 'Roblox'],
            'Musique': ['Spotify', 'SoundCloud', 'Bandcamp', 'Apple Music'],
            'Art & Design': ['DeviantArt', 'Behance', 'Dribbble', 'ArtStation'],
            'Autres': []
        }
        
        for category, platforms in categories.items():
            category_profiles = [(p, u) for p, u in found_profiles if p in platforms]
            
            if category_profiles:
                print_yellow(f"\n  [{category}]")
                for platform, url in category_profiles:
                    print_green(f"    ✓ {platform}: {url}")
        
        # Profils non catégorisés
        categorized = [p for cat in categories.values() for p in cat]
        other_profiles = [(p, u) for p, u in found_profiles if p not in categorized]
        
        if other_profiles:
            print_yellow("\n  [Autres Plateformes]")
            for platform, url in other_profiles:
                print_green(f"    ✓ {platform}: {url}")
    
    # Sauvegarde
    save_results(identifier, found_profiles)
    
    print_red("\n" + "="*70 + "\n")

def save_results(identifier, found_profiles):
    """Sauvegarde les résultats dans un fichier"""
    try:
        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        filename = f"{results_dir}/social_{identifier}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("  LUNIX - SOCIAL MEDIA FINDER RESULTS\n")
            f.write(f"  Identifiant: {identifier}\n")
            f.write(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Profils trouvés: {len(found_profiles)}\n\n")
            
            for platform, url in found_profiles:
                f.write(f"[{platform}]\n{url}\n\n")
        
        print_green(f"[+] Résultats sauvegardés dans: {filename}")
        
    except Exception as e:
        print_red(f"[!] Erreur lors de la sauvegarde: {str(e)}")

def main():
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70 + "\n")
    
    identifier = input(f"{RED}[*] Entrez le username/identifiant à rechercher: {RESET}").strip()
    
    if not identifier:
        print_red("\n[!] Erreur: Veuillez entrer un identifiant valide!")
        time.sleep(2)
        return
    
    print_red(f"\n[*] Démarrage de la recherche pour: {identifier}\n")
    time.sleep(1)
    
    search_social_media(identifier)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_red("\n\n[!] Recherche interrompue par l'utilisateur.")
        sys.exit(0)
