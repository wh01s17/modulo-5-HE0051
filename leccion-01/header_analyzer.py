# header_analyzer.py
# Script para analizar cabeceras HTTP y guardar el resultado en un archivo de texto

import requests

def analyze_headers(url):
    # Verifica que la URL tenga el esquema http:// o https://
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    print("\nAnalizando cabeceras para:", url, "\n")

    try:
        # Envía una petición GET al servidor
        response = requests.get(url, timeout=5)
        print("Estado de respuesta:", response.status_code, response.reason, "\n")

        headers = response.headers

        # Construimos un texto para guardar en el archivo
        report_lines = []
        report_lines.append(f"Análisis de cabeceras para: {url}")
        report_lines.append(f"Estado de respuesta: {response.status_code} {response.reason}\n")

        report_lines.append("Cabeceras encontradas:\n")
        for key, value in headers.items():
            print(" -", key + ":", value)  # Mostramos en consola
            report_lines.append(f" - {key}: {value}")

        # Destacamos cabeceras importantes
        report_lines.append("\nCabeceras destacadas:")
        report_lines.append(f"Server: {headers.get('Server', 'No presente')}")
        report_lines.append(f"X-Powered-By: {headers.get('X-Powered-By', 'No presente')}")
        report_lines.append(f"Content-Type: {headers.get('Content-Type', 'No presente')}")
        report_lines.append(f"Set-Cookie: {headers.get('Set-Cookie', 'No presente')}")
        report_lines.append(f"Strict-Transport-Security: {headers.get('Strict-Transport-Security', 'No presente')}")

        # Guardamos el resultado en un archivo de texto
        with open("header_report.txt", "w", encoding="utf-8") as f:
            for line in report_lines:
                f.write(line + "\n")

        print("\nAnálisis finalizado. El reporte se guardó en 'header_report.txt'.")

    except requests.exceptions.MissingSchema:
        print("Error: La URL ingresada no es válida.")
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo establecer conexión con el servidor.")
    except requests.exceptions.Timeout:
        print("Error: El servidor tardó demasiado en responder.")
    except Exception as e:
        print("Error inesperado:", e)

# Programa principal
if __name__ == "__main__":
    print("Analizador de Cabeceras HTTP - Python y Ciberseguridad")
    target_url = input("Ingresa la URL a analizar (ej: scanme.nmap.org): ")
    analyze_headers(target_url)
