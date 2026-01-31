import os
import sys
import time
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

def print_yellow(text):
    print(f"{YELLOW}{text}{RESET}")

def print_cyan(text):
    print(f"{CYAN}{text}{RESET}")

def print_magenta(text):
    print(f"{MAGENTA}{text}{RESET}")

def ascii_banner():
    banner = """
╔╦╗╔═╗═╗ ╦  ╔═╗╦═╗╔═╗╔═╗╔╦╗╔═╗
 ║║║ ║╔╩╦╝  ║  ╠╦╝║╣ ╠═╣ ║ ║╣ 
═╩╝╚═╝╩ ╚═  ╚═╝╩╚═╚═╝╩ ╩ ╩ ╚═╝
    Création de Documents Dox
    """
    return banner

def get_input(prompt, required=True):
    """Demande une entrée utilisateur"""
    while True:
        value = input(f"{CYAN}{prompt}{RESET}").strip()
        if value or not required:
            return value if value else "N/A"
        print_red("[!] Ce champ est requis!")

def create_dox():
    """Fonction principale de création de dox"""
    
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70)
    print_red("                    CRÉATION D'UN DOX")
    print_red("="*70 + "\n")
    
    print_yellow("[*] Remplissez les informations ci-dessous")
    print_yellow("[*] Laissez vide pour 'N/A' (sauf nom)\n")
    time.sleep(1)
    
    # Collection des données
    dox_data = {}
    
    print_magenta("\n┌─ INFORMATIONS PERSONNELLES")
    dox_data['nom_complet'] = get_input("│ Nom complet: ", required=True)
    dox_data['surnom'] = get_input("│ Surnom/Alias: ", required=False)
    dox_data['age'] = get_input("│ Âge: ", required=False)
    dox_data['date_naissance'] = get_input("│ Date de naissance (JJ/MM/AAAA): ", required=False)
    dox_data['sexe'] = get_input("│ Sexe: ", required=False)
    dox_data['nationalite'] = get_input("│ Nationalité: ", required=False)
    
    print_magenta("\n┌─ ADRESSE & LOCALISATION")
    dox_data['adresse'] = get_input("│ Adresse complète: ", required=False)
    dox_data['ville'] = get_input("│ Ville: ", required=False)
    dox_data['code_postal'] = get_input("│ Code postal: ", required=False)
    dox_data['pays'] = get_input("│ Pays: ", required=False)
    dox_data['coordonnees'] = get_input("│ Coordonnées GPS (lat, lon): ", required=False)
    
    print_magenta("\n┌─ CONTACTS")
    dox_data['telephone'] = get_input("│ Numéro de téléphone: ", required=False)
    dox_data['email'] = get_input("│ Email principal: ", required=False)
    dox_data['email_secondaire'] = get_input("│ Email secondaire: ", required=False)
    
    print_magenta("\n┌─ RÉSEAUX SOCIAUX")
    dox_data['facebook'] = get_input("│ Facebook: ", required=False)
    dox_data['instagram'] = get_input("│ Instagram: ", required=False)
    dox_data['twitter'] = get_input("│ Twitter/X: ", required=False)
    dox_data['tiktok'] = get_input("│ TikTok: ", required=False)
    dox_data['snapchat'] = get_input("│ Snapchat: ", required=False)
    dox_data['discord'] = get_input("│ Discord: ", required=False)
    dox_data['autres_reseaux'] = get_input("│ Autres réseaux: ", required=False)
    
    print_magenta("\n┌─ INFORMATIONS PROFESSIONNELLES")
    dox_data['profession'] = get_input("│ Profession/Occupation: ", required=False)
    dox_data['entreprise'] = get_input("│ Entreprise/École: ", required=False)
    dox_data['lieu_travail'] = get_input("│ Lieu de travail: ", required=False)
    
    print_magenta("\n┌─ INFORMATIONS FAMILIALES")
    dox_data['famille'] = get_input("│ Membres de la famille: ", required=False)
    dox_data['relations'] = get_input("│ Relations importantes: ", required=False)
    
    print_magenta("\n┌─ INFORMATIONS TECHNIQUES")
    dox_data['ip_address'] = get_input("│ Adresse IP: ", required=False)
    dox_data['isp'] = get_input("│ Fournisseur Internet (ISP): ", required=False)
    dox_data['user_agent'] = get_input("│ User Agent: ", required=False)
    
    print_magenta("\n┌─ INFORMATIONS ADDITIONNELLES")
    dox_data['loisirs'] = get_input("│ Loisirs/Centres d'intérêt: ", required=False)
    dox_data['vehicule'] = get_input("│ Véhicule (marque, modèle, plaque): ", required=False)
    dox_data['notes'] = get_input("│ Notes supplémentaires: ", required=False)
    
    # Affichage du résumé
    print_red("\n\n" + "="*70)
    print_red("                    APERÇU DU DOX")
    print_red("="*70 + "\n")
    time.sleep(0.5)
    
    display_dox(dox_data)
    
    # Sauvegarde
    print_red("\n" + "="*70 + "\n")
    save_choice = input(f"{YELLOW}[*] Sauvegarder ce dox? (o/n): {RESET}").strip().lower()
    
    if save_choice == 'o' or save_choice == 'oui':
        save_dox(dox_data)
    else:
        print_yellow("\n[*] Dox non sauvegardé")
    
    print_red("\n" + "="*70 + "\n")

def display_dox(data):
    """Affiche le dox de manière formatée"""
    
    print_magenta("╔══════════════════════════════════════════════════════════════════════╗")
    print_magenta("║                          DOX REPORT                                  ║")
    print_magenta("╚══════════════════════════════════════════════════════════════════════╝\n")
    
    sections = [
        ("INFORMATIONS PERSONNELLES", [
            ('Nom complet', 'nom_complet'),
            ('Surnom/Alias', 'surnom'),
            ('Âge', 'age'),
            ('Date de naissance', 'date_naissance'),
            ('Sexe', 'sexe'),
            ('Nationalité', 'nationalite'),
        ]),
        ("ADRESSE & LOCALISATION", [
            ('Adresse', 'adresse'),
            ('Ville', 'ville'),
            ('Code postal', 'code_postal'),
            ('Pays', 'pays'),
            ('Coordonnées GPS', 'coordonnees'),
        ]),
        ("CONTACTS", [
            ('Téléphone', 'telephone'),
            ('Email principal', 'email'),
            ('Email secondaire', 'email_secondaire'),
        ]),
        ("RÉSEAUX SOCIAUX", [
            ('Facebook', 'facebook'),
            ('Instagram', 'instagram'),
            ('Twitter/X', 'twitter'),
            ('TikTok', 'tiktok'),
            ('Snapchat', 'snapchat'),
            ('Discord', 'discord'),
            ('Autres', 'autres_reseaux'),
        ]),
        ("INFORMATIONS PROFESSIONNELLES", [
            ('Profession', 'profession'),
            ('Entreprise/École', 'entreprise'),
            ('Lieu de travail', 'lieu_travail'),
        ]),
        ("INFORMATIONS FAMILIALES", [
            ('Famille', 'famille'),
            ('Relations', 'relations'),
        ]),
        ("INFORMATIONS TECHNIQUES", [
            ('Adresse IP', 'ip_address'),
            ('ISP', 'isp'),
            ('User Agent', 'user_agent'),
        ]),
        ("INFORMATIONS ADDITIONNELLES", [
            ('Loisirs', 'loisirs'),
            ('Véhicule', 'vehicule'),
            ('Notes', 'notes'),
        ]),
    ]
    
    for section_name, fields in sections:
        print_red(f"┌─ {section_name}")
        for label, key in fields:
            value = data.get(key, 'N/A')
            if value and value != 'N/A':
                print_cyan(f"│ {label}: {value}")
        print_red("│")

def save_dox(data):
    """Sauvegarde le dox dans un fichier"""
    try:
        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        safe_name = data['nom_complet'].replace(' ', '_').replace('/', '_')
        filename = f"{results_dir}/dox_{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("                          LUNIX - DOX REPORT\n")
            f.write(f"  Cible: {data['nom_complet']}\n")
            f.write(f"  Date de création: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")
            
            sections = [
                ("INFORMATIONS PERSONNELLES", [
                    ('Nom complet', 'nom_complet'),
                    ('Surnom/Alias', 'surnom'),
                    ('Âge', 'age'),
                    ('Date de naissance', 'date_naissance'),
                    ('Sexe', 'sexe'),
                    ('Nationalité', 'nationalite'),
                ]),
                ("ADRESSE & LOCALISATION", [
                    ('Adresse', 'adresse'),
                    ('Ville', 'ville'),
                    ('Code postal', 'code_postal'),
                    ('Pays', 'pays'),
                    ('Coordonnées GPS', 'coordonnees'),
                ]),
                ("CONTACTS", [
                    ('Téléphone', 'telephone'),
                    ('Email principal', 'email'),
                    ('Email secondaire', 'email_secondaire'),
                ]),
                ("RÉSEAUX SOCIAUX", [
                    ('Facebook', 'facebook'),
                    ('Instagram', 'instagram'),
                    ('Twitter/X', 'twitter'),
                    ('TikTok', 'tiktok'),
                    ('Snapchat', 'snapchat'),
                    ('Discord', 'discord'),
                    ('Autres', 'autres_reseaux'),
                ]),
                ("INFORMATIONS PROFESSIONNELLES", [
                    ('Profession', 'profession'),
                    ('Entreprise/École', 'entreprise'),
                    ('Lieu de travail', 'lieu_travail'),
                ]),
                ("INFORMATIONS FAMILIALES", [
                    ('Famille', 'famille'),
                    ('Relations', 'relations'),
                ]),
                ("INFORMATIONS TECHNIQUES", [
                    ('Adresse IP', 'ip_address'),
                    ('ISP', 'isp'),
                    ('User Agent', 'user_agent'),
                ]),
                ("INFORMATIONS ADDITIONNELLES", [
                    ('Loisirs', 'loisirs'),
                    ('Véhicule', 'vehicule'),
                    ('Notes', 'notes'),
                ]),
            ]
            
            for section_name, fields in sections:
                f.write(f"\n{section_name}\n")
                f.write("-" * 70 + "\n")
                for label, key in fields:
                    value = data.get(key, 'N/A')
                    f.write(f"{label}: {value}\n")
            
            f.write("\n" + "="*70 + "\n")
            f.write("                    AVERTISSEMENT\n")
            f.write("="*70 + "\n")
            f.write("Ce document est fourni à des fins éducatives uniquement.\n")
            f.write("L'utilisation de ces informations à des fins malveillantes\n")
            f.write("est illégale et contraire à l'éthique.\n")
        
        print_green(f"\n[+] Dox sauvegardé dans: {filename}")
        
    except Exception as e:
        print_red(f"\n[!] Erreur lors de la sauvegarde: {str(e)}")

def main():
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70 + "\n")
    
    print_yellow("[!] AVERTISSEMENT IMPORTANT")
    print_red("─" * 70)
    print_cyan("Ce module est conçu à des fins ÉDUCATIVES uniquement.")
    print_cyan("Le doxing est ILLÉGAL dans de nombreux pays.")
    print_cyan("N'utilisez jamais ces informations pour:")
    print_cyan("  • Harcèlement")
    print_cyan("  • Menaces")
    print_cyan("  • Chantage")
    print_cyan("  • Toute activité malveillante")
    print_red("─" * 70)
    
    choice = input(f"\n{YELLOW}[*] Acceptez-vous ces conditions? (o/n): {RESET}").strip().lower()
    
    if choice != 'o' and choice != 'oui':
        print_red("\n[!] Accès refusé. Retour au menu principal.")
        time.sleep(2)
        return
    
    print_red(f"\n[*] Démarrage du créateur de dox...\n")
    time.sleep(1)
    
    create_dox()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_red("\n\n[!] Création interrompue par l'utilisateur.")
        sys.exit(0)
