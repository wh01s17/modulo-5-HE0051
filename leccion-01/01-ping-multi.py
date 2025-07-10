# libreria para interactuar con el so
import os
import platform

ips = ["8.8.8.8", "1.1.1.1", "192.168.1.234"]

# Detectar sistema operativo
if platform.system() == "Windows":
    comando = "ping -n 1 {} > nul"
else:
    comando = "ping -c 1 {} &>/dev/null"

for ip in ips:
    respuesta = os.system(comando.format(ip))
    estado = "[+] Activa" if respuesta == 0 else "[!] Inactiva"
    print(f"{ip}: {estado}")
