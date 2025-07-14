import os

def ping_sweep(red_base):
    for i in range(1, 255):
        ip = f"{red_base}.{i}"

        # -c 1 o -n 1: Envia solo 1 paquete
        # -W 1 o -w 1000: Espera máxima es de 1 segundo
        # respuesta = os.system(f"ping -c 1 -W 1 {ip} &>/dev/null")
        respuesta = os.system(f"ping -n 1 -w 1000 {ip} >nul 2>&1")

        if respuesta == 0:
            print(f"[+] {ip} está activa")
        else:
            print(f"[-] {ip} no responde")

if __name__ == "__main__":
    red_base = "192.168.1"
    ping_sweep(red_base)
