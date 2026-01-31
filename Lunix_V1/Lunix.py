import os
import sys
import time
import subprocess

# Couleurs
RED = '\033[91m'
RESET = '\033[0m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_red(text):
    print(f"{RED}{text}{RESET}")

def ascii_art():
    art = """
 ██▓     █    ██  ███▄    █  ██▓▒██   ██▒
▓██▒     ██  ▓██▒ ██ ▀█   █ ▓██▒▒▒ █ █ ▒░
▒██░    ▓██  ▒██░▓██  ▀█ ██▒▒██▒░░  █   ░
▒██░    ▓▓█  ░██░▓██▒  ▐▌██▒░██░ ░ █ █ ▒ 
░██████▒▒▒█████▓ ▒██░   ▓██░░██░▒██▒ ▒██▒
░ ▒░▓  ░░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒ ░▓  ▒▒ ░ ░▓ ░
░ ░ ▒  ░░░▒░ ░ ░ ░ ░░   ░ ▒░ ▒ ░░░   ░▒ ░
  ░ ░    ░░░ ░ ░    ░   ░ ░  ▒ ░ ░    ░  
    ░  ░   ░              ░  ░   ░    ░  
                                         
                                       
    Multi-Tool OSINT By [HYDRA]
    https://github.com/Hydra356
    """
    return art

def display_menu():
    clear()
    print_red(ascii_art())
    print_red("\n" + "="*60)
    print_red("                    [Menu Principal]")
    print_red("="*60)
    print_red("\n[01] -> Username Tracker (OSINT)")
    print_red("[02] -> Email Tracker (OSINT)")
    print_red("[03] -> Phone Number Info")
    print_red("[04] -> IP Info (Lookup)")
    print_red("[05] -> Domain Info")
    print_red("[06] -> Social Media Finder")
    print_red("[07] -> Password Leak Checker")
    print_red("[08] -> Breach Database Search")
    print_red("[09] -> Image Reverse Search")
    print_red("[10] -> Dox Create")
    print_red("[11] -> SQL Vulnerability Scanner")
    print_red("[12] -> Webhook Info")
    print_red("[13] -> Nitro Generator")
    print_red("[14] -> Image to ASCII")
    print_red("[15] -> Webhook Spammer")
    print_red("\n[00] -> Quitter")
    print_red("\n" + "="*60 + "\n")

def run_tool(tool_name):
    config_path = os.path.join("config", f"{tool_name}.py")
    
    if not os.path.exists(config_path):
        print_red(f"\n[!] Erreur: Le module {tool_name} n'existe pas!")
        time.sleep(2)
        return
    
    try:
        print_red(f"\n[*] Lancement de {tool_name}...\n")
        time.sleep(0.5)
        subprocess.run([sys.executable, config_path])
    except Exception as e:
        print_red(f"\n[!] Erreur lors de l'exécution: {str(e)}")
    
    input(f"\n{RED}[*] Appuyez sur Entrée pour retourner au menu...{RESET}")

def main():
    while True:
        display_menu()
        
        choice = input(f"{RED}[Lunix]~$ {RESET}").strip()
        
        if choice == "01" or choice == "1":
            run_tool("username_tracker")
        elif choice == "02" or choice == "2":
            run_tool("email_tracker")
        elif choice == "03" or choice == "3":
            run_tool("phone_info")
        elif choice == "04" or choice == "4":
            run_tool("ip_lookup")
        elif choice == "05" or choice == "5":
            run_tool("domain_info")
        elif choice == "06" or choice == "6":
            run_tool("social_finder")
        elif choice == "07" or choice == "7":
            run_tool("password_checker")
        elif choice == "08" or choice == "8":
            run_tool("breach_search")
        elif choice == "09" or choice == "9":
            run_tool("image_search")
        elif choice == "10":
            run_tool("dox_create")
        elif choice == "11":
            run_tool("sql_scanner")
        elif choice == "12":
            run_tool("webhook_info")
        elif choice == "13":
            run_tool("nitro_generator")
        elif choice == "14":
            run_tool("image_to_ascii")
        elif choice == "15":
            run_tool("webhook_spammer")
        elif choice == "00" or choice == "0":
            print_red("\n[*] Merci d'avoir utilisé Lunix!")
            print_red("[*] Au revoir!\n")
            time.sleep(1)
            break
        else:
            print_red("\n[!] Choix invalide! Veuillez réessayer.")
            time.sleep(1.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_red("\n\n[!] Programme interrompu par l'utilisateur.")
        print_red("[*] Au revoir!\n")
        sys.exit(0)
