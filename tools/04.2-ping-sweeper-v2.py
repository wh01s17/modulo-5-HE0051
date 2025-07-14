import subprocess
import signal
import sys 
import platform

def def_handler(sig, frame):
    print("\n[!] Saliendo ...\n")
    sys.exit(1)

# Manejo de ctrl + c
signal.signal(signal.SIGINT, def_handler)

def ping_sweep(red_base):
    sistema = platform.system()

    for i in range(1, 255):
        ip = f"{red_base}.{i}"

        if sistema == "Windows":
            comando = ["ping", "-n", "1", "-w", "1000", ip]
        else:
            comando = ["ping", "-c", "1", "-W", "1", ip]
        
        result = subprocess.run(
            comando,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if result.returncode == 0:
            print(f"[+] {ip} está activa")
        else:
            print(f"[-] {ip} no responde")

if __name__ == "__main__":
    red_base = "192.168.1"
    ping_sweep(red_base)

