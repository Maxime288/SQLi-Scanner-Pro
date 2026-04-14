#!/usr/bin/env python3
"""
🌐 SQLi Scanner Pro
Détecteur de vulnérabilités SQL Injection basique.
"""

import requests
import argparse
import sys
import time
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# ──────────────────────────────────────────────────────────────
# Couleurs ANSI & Style
# ──────────────────────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    RED     = "\033[38;5;196m"
    GREEN   = "\033[38;5;82m"
    YELLOW  = "\033[38;5;226m"
    BLUE    = "\033[38;5;45m"
    MAGENTA = "\033[38;5;171m"
    CYAN    = "\033[38;5;51m"
    GRAY    = "\033[38;5;244m"

BANNER = fr"""
{C.MAGENTA}   _____  ____  _      _ {C.CYAN}  _____  {C.RESET}
{C.MAGENTA}  / ____|/ __ \| |    (_) {C.CYAN}/ ____| {C.RESET}
{C.MAGENTA} | (___ | |  | | |     _ {C.CYAN}| (___   {C.RESET}
{C.MAGENTA}  \___ \| |  | | |    | |{C.CYAN} \___ \  {C.RESET}
{C.MAGENTA}  ____) | |__| | |____| |{C.CYAN} ____) | {C.RESET}
{C.MAGENTA} |_____/ \___\_\______|_|{C.CYAN}|_____/  {C.RESET}
{C.GRAY}        SQL Injection Detector v1.0{C.RESET}
"""

# Signatures d'erreurs SQL communes
SQL_ERRORS = {
    "MySQL": ["you have an error in your sql syntax", "warning: mysql"],
    "PostgreSQL": ["viva postgresql", "invalid input syntax for type", "postgresql query failed"],
    "Microsoft SQL Server": ["unclosed quotation mark after the character string", "driver: sql server"],
    "Oracle": ["ora-00933", "oracle error", "quoted string not properly terminated"]
}

PAYLOADS = ["'", "\"", "';", "\")", "'))"]

# ──────────────────────────────────────────────────────────────
# Logique de détection
# ──────────────────────────────────────────────────────────────

def scan_sqli(url):
    print(f" {C.BOLD}[*]{C.RESET} Analyse de l'URL : {C.CYAN}{url}{C.RESET}")
    
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    
    if not params:
        print(f" {C.RED}[!] Erreur : Aucun paramètre GET trouvé dans l'URL.{C.RESET}")
        return

    vulnerable = False

    for param in params:
        print(f" {C.BOLD}[*]{C.RESET} Test du paramètre : {C.YELLOW}{param}{C.RESET}")
        
        for payload in PAYLOADS:
            # Création de l'URL modifiée avec le payload
            temp_params = params.copy()
            temp_params[param] = [payload]
            new_query = urlencode(temp_params, doseq=True)
            target_url = urlunparse(parsed_url._replace(query=new_query))
            
            try:
                response = requests.get(target_url, timeout=5)
                content = response.text.lower()
                
                for db, errors in SQL_ERRORS.items():
                    for error in errors:
                        if error in content:
                            print(f"\n{C.RED}{C.BOLD}[VULNÉRABLE]{C.RESET} Injection possible !")
                            print(f"  {C.BOLD}Paramètre : {C.RESET}{param}")
                            print(f"  {C.BOLD}Payload   : {C.RESET}{payload}")
                            print(f"  {C.BOLD}Type DB   : {C.RESET}{db}")
                            vulnerable = True
                            return # On s'arrête à la première vuln trouvé
            except Exception as e:
                print(f" {C.GRAY}[!] Erreur de connexion sur {payload}{C.RESET}")

    if not vulnerable:
        print(f"\n {C.GREEN}[-]{C.RESET} Aucune vulnérabilité SQLi évidente détectée.")

def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="Détecteur de SQL Injection basique")
    parser.add_argument("-u", "--url", required=True, help="URL cible (ex: http://site.com/page.php?id=1)")
    args = parser.parse_args()

    start_time = time.time()
    scan_sqli(args.url)
    print(f"\n{C.GRAY}Terminé en {time.time()-start_time:.2f}s{C.RESET}")

if __name__ == "__main__":
    main()
