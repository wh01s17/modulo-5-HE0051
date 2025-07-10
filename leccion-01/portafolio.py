import requests

def analyze_headers(url):
    # Verifica que la URL tenga un esquema válido
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    print(f"\nAnalizando cabeceras para: {url}\n")

    try:
        response = requests.get(url, timeout=5)
        print(f"[+] Estado de respuesta: {response.status_code} {response.reason}\n")
        headers = response.headers
        print("Cabeceras encontradas:\n")

        for key, value in headers.items():
            print(f" - {key}: {value}")

        print("\nCabeceras destacadas:")
        print(f"Server: {headers.get('Server', 'No presente')}")
        print(f"X-Powered-By: {headers.get('X-Powered-By', 'No presente')}")
        print(f"Content-Type: {headers.get('Content-Type', 'No presente')}")
        print(f"Set-Cookie: {headers.get('Set-Cookie', 'No presente')}")
        print(f"Strict-Transport-Security: {headers.get('Strict-Transport-Security', 'No presente')}")

    except requests.exceptions.MissingSchema:
        print("Error: La URL ingresada no es válida.")
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo establecer conexión con el servidor.")
    except requests.exceptions.Timeout:
        print("Error: El servidor tardó demasiado en responder.")
    except Exception as e:
        print(f"Error inesperado: {e}")

    print("\nAnálisis finalizado. Usa esta información con fines educativos.")

# Programa principal
if __name__ == "__main__":
    print("🧪 Analizador de Cabeceras HTTP - Python y Ciberseguridad")
    target_url = input("Ingresa la URL a analizar (ej: scanme.nmap.org): ")
    analyze_headers(target_url)
