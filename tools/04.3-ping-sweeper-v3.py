# Ping Sweeper compatible con Linux y Windows (con threading y argumento de red)

# Ejecuta otros procesos del sistema (programas externos)
import subprocess
import signal
import sys
import platform
# Ejecuta varios hilos dentro del mismo proceso Python
import threading

# Manejador de Ctrl+C
def def_handler(sig, frame):
    print("\n[!] Saliendo...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

# Función para hacer ping a una IP específica
def ping_host(ip, sistema):
    if sistema == "Windows":
        comando = ["ping", "-n", "1", "-w", "1000", ip]
    else:
        comando = ["ping", "-c", "1", "-W", "1", ip]

    try:
        result = subprocess.run(
            comando,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if result.returncode == 0:
            print(f"[+] {ip} está activa")
        # else:
        #     print(f"[-] {ip} no responde")
    except KeyboardInterrupt:
        print("\n[!] Interrumpido por el usuario")
        sys.exit(0)

# Barrido de IPs con múltiples hilos
def ping_sweep(red_base):
    sistema = platform.system()
    hilos = []

    for i in range(1, 255):
        ip = f"{red_base}.{i}"
        hilo = threading.Thread(target=ping_host, args=(ip, sistema))
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <base_de_red>")
        print("Ejemplo: python ping_sweeper.py 192.168.1")
        sys.exit(1)

    red_base = sys.argv[1]
    ping_sweep(red_base)
