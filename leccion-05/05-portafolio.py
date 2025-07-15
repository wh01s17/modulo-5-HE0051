# Detectar formularios

import requests
from bs4 import BeautifulSoup

# URL de prueba con formularios públicos
url = "https://httpbin.org/forms/post"

# Realizar solicitud HTTP GET
respuesta = requests.get(url)

# Analizar el HTML con BeautifulSoup
soup = BeautifulSoup(respuesta.text, 'html.parser')

# Buscar todos los formularios
formularios = soup.find_all('form')

print(f"Formularios encontrados: {len(formularios)}\n")

# Analizar cada formulario
for idx, form in enumerate(formularios, start=1):
    metodo = form.get('method', 'GET').upper()
    accion = form.get('action', 'N/A')

    print(f"Formulario #{idx}:")
    print(f"- Método: {metodo}")
    print(f"- Acción: {accion}")

    # Buscar todos los campos de entrada
    campos = form.find_all(['input', 'textarea', 'select'])
    print("- Campos:")
    for campo in campos:
        nombre = campo.get('name', '[sin nombre]')
        tipo = campo.get('type', 'text') if campo.name == 'input' else campo.name
        print(f" * name: {nombre} | type: {tipo}")
    print("-" * 40)
