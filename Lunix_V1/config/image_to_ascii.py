import os
import sys
import time
from PIL import Image
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
╦╔╦╗╔═╗╔═╗╔═╗  ╔╦╗╔═╗  ╔═╗╔═╗╔═╗╦╦
║║║║╠═╣║ ╦║╣    ║ ║ ║  ╠═╣╚═╗║  ║║
╩╩ ╩╩ ╩╚═╝╚═╝   ╩ ╚═╝  ╩ ╩╚═╝╚═╝╩╩
    Convertisseur Image vers ASCII
    """
    return banner

# Caractères ASCII pour la conversion (du plus sombre au plus clair)
ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.', ' ']
# Version détaillée
ASCII_CHARS_DETAILED = ['$', '@', 'B', '%', '8', '&', 'W', 'M', '#', '*', 'o', 'a', 'h', 'k', 'b', 'd', 'p', 'q', 'w', 'm', 'Z', 'O', '0', 'Q', 'L', 'C', 'J', 'U', 'Y', 'X', 'z', 'c', 'v', 'u', 'n', 'x', 'r', 'j', 'f', 't', '/', '\\', '|', '(', ')', '1', '{', '}', '[', ']', '?', '-', '_', '+', '~', '<', '>', 'i', '!', 'l', 'I', ';', ':', ',', '"', '^', '`', "'", '.', ' ']

def resize_image(image, new_width=100):
    """Redimensionne l'image en conservant le ratio"""
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  # 0.55 pour compenser la hauteur des caractères
    return image.resize((new_width, new_height))

def grayscale_image(image):
    """Convertit l'image en niveaux de gris"""
    return image.convert('L')

def pixels_to_ascii(image, detailed=False):
    """Convertit les pixels en caractères ASCII"""
    pixels = image.getdata()
    ascii_chars = ASCII_CHARS_DETAILED if detailed else ASCII_CHARS
    
    ascii_str = ''
    for pixel in pixels:
        # Normalise la valeur du pixel (0-255) à l'index des caractères
        ascii_str += ascii_chars[pixel * len(ascii_chars) // 256]
    
    return ascii_str

def convert_image_to_ascii(image_path, width=100, detailed=False):
    """Convertit une image en art ASCII"""
    try:
        print_yellow("\n[~] Chargement de l'image...", end="\r")
        image = Image.open(image_path)
        print_green("[+] Image chargée!")
        
        print_yellow("[~] Redimensionnement...", end="\r")
        image = resize_image(image, width)
        print_green("[+] Image redimensionnée!")
        
        print_yellow("[~] Conversion en niveaux de gris...", end="\r")
        image = grayscale_image(image)
        print_green("[+] Conversion terminée!")
        
        print_yellow("[~] Génération de l'ASCII art...", end="\r")
        ascii_str = pixels_to_ascii(image, detailed)
        print_green("[+] ASCII art généré!")
        
        # Découpe la chaîne en lignes selon la largeur
        img_width = image.width
        ascii_str_len = len(ascii_str)
        ascii_img = ''
        
        for i in range(0, ascii_str_len, img_width):
            ascii_img += ascii_str[i:i+img_width] + '\n'
        
        return {
            'success': True,
            'ascii_art': ascii_img,
            'width': img_width,
            'height': image.height
        }
        
    except FileNotFoundError:
        return {'success': False, 'error': 'Fichier introuvable'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def image_to_ascii(image_path):
    """Fonction principale de conversion"""
    
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70)
    print_red(f"  Image: {os.path.basename(image_path)}")
    print_red(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print_red("="*70 + "\n")
    
    # Vérification du fichier
    if not os.path.exists(image_path):
        print_red("[!] Fichier introuvable!")
        return
    
    print_green("[+] Fichier détecté")
    
    # Options
    print_red("\n" + "="*70)
    print_red("                        OPTIONS")
    print_red("="*70)
    
    try:
        width = int(input(f"\n{CYAN}[*] Largeur (caractères, défaut 100): {RESET}").strip() or "100")
        if width <= 0:
            width = 100
    except:
        width = 100
    
    detailed = input(f"{CYAN}[*] Mode détaillé (plus de caractères)? (o/n): {RESET}").strip().lower()
    detailed = (detailed == 'o' or detailed == 'oui')
    
    print_red(f"\n[*] Démarrage de la conversion...\n")
    time.sleep(1)
    
    # Conversion
    result = convert_image_to_ascii(image_path, width, detailed)
    
    if not result['success']:
        print_red(f"\n[!] Erreur: {result['error']}")
        return
    
    # Affichage
    print_red("\n" + "="*70)
    print_red("                      RÉSULTAT ASCII ART")
    print_red("="*70 + "\n")
    
    print_cyan(result['ascii_art'])
    
    print_red("\n" + "="*70)
    print_red("                      INFORMATIONS")
    print_red("="*70)
    print_cyan(f"\n  Largeur: {result['width']} caractères")
    print_cyan(f"  Hauteur: {result['height']} lignes")
    print_cyan(f"  Mode: {'Détaillé' if detailed else 'Standard'}")
    
    # Sauvegarde
    print_red("\n" + "="*70)
    save_choice = input(f"\n{YELLOW}[*] Sauvegarder l'ASCII art? (o/n): {RESET}").strip().lower()
    
    if save_choice == 'o' or save_choice == 'oui':
        save_ascii(result['ascii_art'], image_path)
    
    print_red("\n" + "="*70 + "\n")

def save_ascii(ascii_art, original_path):
    """Sauvegarde l'ASCII art dans un fichier"""
    try:
        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        base_name = os.path.splitext(os.path.basename(original_path))[0]
        filename = f"{results_dir}/ascii_{base_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("  LUNIX - IMAGE TO ASCII CONVERTER\n")
            f.write(f"  Image originale: {os.path.basename(original_path)}\n")
            f.write(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")
            
            f.write(ascii_art)
        
        print_green(f"\n[+] ASCII art sauvegardé dans: {filename}")
        
    except Exception as e:
        print_red(f"\n[!] Erreur lors de la sauvegarde: {str(e)}")

def main():
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70 + "\n")
    
    print_yellow("[*] Convertissez vos images en ASCII art!\n")
    print_cyan("[*] Formats supportés: JPG, PNG, BMP, GIF, etc.\n")
    
    image_path = input(f"{RED}[*] Chemin de l'image: {RESET}").strip()
    
    if not image_path:
        print_red("\n[!] Erreur: Veuillez entrer un chemin valide!")
        time.sleep(2)
        return
    
    # Supprime les guillemets si présents
    image_path = image_path.strip('"').strip("'")
    
    image_to_ascii(image_path)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_red("\n\n[!] Conversion interrompue par l'utilisateur.")
        sys.exit(0)
