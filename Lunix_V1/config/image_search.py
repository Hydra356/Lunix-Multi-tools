import os
import sys
import time
import webbrowser
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
╦╔╦╗╔═╗╔═╗╔═╗  ╔═╗╔═╗╔═╗╦═╗╔═╗╦ ╦
║║║║╠═╣║ ╦║╣   ╚═╗║╣ ╠═╣╠╦╝║  ╠═╣
╩╩ ╩╩ ╩╚═╝╚═╝  ╚═╝╚═╝╩ ╩╩╚═╚═╝╩ ╩
    Recherche Inversée d'Images
    """
    return banner

# Plateformes de recherche d'images
IMAGE_SEARCH_ENGINES = {
    'Google Images': 'https://www.google.com/searchbyimage?image_url={}',
    'Yandex Images': 'https://yandex.com/images/search?url={}&rpt=imageview',
    'TinEye': 'https://www.tineye.com/search?url={}',
    'Bing Visual Search': 'https://www.bing.com/images/search?q=imgurl:{}',
}

# Outils d'analyse d'images
IMAGE_TOOLS = {
    'FotoForensics': 'https://fotoforensics.com/',
    'Forensically': 'https://29a.ch/photo-forensics/',
    'Jeffrey\'s Image Metadata Viewer': 'http://exif.regex.info/exif.cgi',
    'Get-IPTC': 'http://www.get-iptc.org/',
}

# Sites de reconnaissance faciale (pour info uniquement)
FACE_RECOGNITION_INFO = [
    'PimEyes: https://pimeyes.com/',
    'FaceCheck.ID: https://facecheck.id/',
    'Clearview AI (Law Enforcement)',
]

def validate_url(url):
    """Valide qu'une URL d'image est correcte"""
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    url_lower = url.lower()
    
    if not url.startswith(('http://', 'https://')):
        return False
    
    # Vérifie si c'est une URL d'image
    return any(url_lower.endswith(ext) for ext in valid_extensions) or '?' in url

def open_search_engines(image_url):
    """Ouvre les moteurs de recherche dans le navigateur"""
    print_red("\n" + "="*70)
    print_red("                  OUVERTURE DES MOTEURS DE RECHERCHE")
    print_red("="*70 + "\n")
    
    print_yellow("[*] Ouverture dans votre navigateur par défaut...\n")
    time.sleep(1)
    
    opened = 0
    for engine, url_template in IMAGE_SEARCH_ENGINES.items():
        try:
            search_url = url_template.format(image_url)
            print_cyan(f"[~] Ouverture de {engine}...")
            webbrowser.open(search_url)
            opened += 1
            time.sleep(1)  # Délai entre les ouvertures
        except Exception as e:
            print_red(f"[!] Erreur avec {engine}: {str(e)}")
    
    print_green(f"\n[+] {opened} moteurs de recherche ouverts!")

def image_search(image_url):
    """Fonction principale de recherche d'image"""
    
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70)
    print_red(f"  URL de l'image: {image_url}")
    print_red(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print_red("="*70 + "\n")
    
    # Validation
    if not validate_url(image_url):
        print_red("[!] URL d'image invalide!")
        print_yellow("\n[*] L'URL doit:")
        print_cyan("  • Commencer par http:// ou https://")
        print_cyan("  • Se terminer par .jpg, .jpeg, .png, .gif, etc.")
        print_cyan("  • Exemple: https://example.com/image.jpg")
        return
    
    print_green("[+] URL valide détectée")
    
    # Informations sur la recherche inversée
    print_red("\n" + "="*70)
    print_red("                  RECHERCHE INVERSÉE D'IMAGE")
    print_red("="*70)
    print_yellow("\n[*] La recherche inversée permet de:")
    print_cyan("  • Trouver la source originale d'une image")
    print_cyan("  • Détecter les images modifiées ou manipulées")
    print_cyan("  • Trouver des images similaires")
    print_cyan("  • Vérifier l'authenticité d'une image")
    print_cyan("  • Identifier des personnes, lieux ou objets")
    
    # URLs de recherche
    print_red("\n" + "="*70)
    print_red("                  LIENS DE RECHERCHE")
    print_red("="*70 + "\n")
    
    for engine, url_template in IMAGE_SEARCH_ENGINES.items():
        search_url = url_template.format(image_url)
        print_green(f"[{engine}]")
        print_cyan(f"  {search_url}\n")
    
    # Métadonnées EXIF
    print_red("\n" + "="*70)
    print_red("                  EXTRACTION DE MÉTADONNÉES")
    print_red("="*70)
    print_yellow("\n[*] Les images contiennent souvent des métadonnées (EXIF):")
    print_cyan("  • Date et heure de prise de vue")
    print_cyan("  • Modèle d'appareil photo / smartphone")
    print_cyan("  • Coordonnées GPS (localisation)")
    print_cyan("  • Paramètres de l'appareil (ISO, ouverture, etc.)")
    print_cyan("  • Logiciel d'édition utilisé")
    
    # Proposition d'ouverture automatique
    print_red("\n" + "="*70 + "\n")
    choice = input(f"{RED}[*] Ouvrir automatiquement les moteurs de recherche? (o/n): {RESET}").strip().lower()
    
    if choice == 'o' or choice == 'oui':
        open_search_engines(image_url)
    else:
        print_yellow("\n[*] Vous pouvez copier les liens ci-dessus manuellement")
    
    # Sauvegarde
    save_results(image_url)
    
    print_red("\n" + "="*70 + "\n")

def save_results(image_url):
    """Sauvegarde les résultats dans un fichier"""
    try:
        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        filename = f"{results_dir}/image_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("  LUNIX - IMAGE REVERSE SEARCH RESULTS\n")
            f.write(f"  URL de l'image: {image_url}\n")
            f.write(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")
            
            f.write("LIENS DE RECHERCHE\n")
            f.write("-" * 70 + "\n\n")
            
            for engine, url_template in IMAGE_SEARCH_ENGINES.items():
                search_url = url_template.format(image_url)
                f.write(f"[{engine}]\n{search_url}\n\n")
            
            f.write("\nOUTILS D'ANALYSE\n")
            f.write("-" * 70 + "\n\n")
            
            for tool, url in IMAGE_TOOLS.items():
                f.write(f"{tool}\n{url}\n\n")
        
        print_green(f"[+] Résultats sauvegardés dans: {filename}")
        
    except Exception as e:
        print_red(f"[!] Erreur lors de la sauvegarde: {str(e)}")

def main():
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70 + "\n")
    
    print_yellow("[*] Entrez l'URL d'une image à rechercher")
    print_cyan("[*] Exemple: https://example.com/photo.jpg\n")
    
    image_url = input(f"{RED}[*] URL de l'image: {RESET}").strip()
    
    if not image_url:
        print_red("\n[!] Erreur: Veuillez entrer une URL valide!")
        time.sleep(2)
        return
    
    print_red(f"\n[*] Préparation de la recherche...\n")
    time.sleep(1)
    
    image_search(image_url)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_red("\n\n[!] Recherche interrompue par l'utilisateur.")
        sys.exit(0)
