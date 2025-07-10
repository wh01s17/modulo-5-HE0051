# libreria para interactuar con el so
import os

ips = ["8.8.8.8", "1.1.1.1", "192.168.1.223"]

for ip in ips:
    respuesta = os.system(f"ping -c 1 {ip} &>/dev/null")

    # operador ternario: verdadero condicion falso
    estado = "[+] Activa" if respuesta == 0 else "[!] Inactiva"
    print(f"{ip}: {estado}")
