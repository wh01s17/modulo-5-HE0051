# Escaneo subred

import nmap

# Crear un escáner de Nmap
scanner = nmap.PortScanner()

# Definir la subred objetivo (ajustar a tu entorno)
subred = "192.168.1.0/24"
print(f"Iniciando escaneo sobre la subred {subred}...\n")

# Ejecutar escaneo con detección de versión (-sV) sobre puertos comunes
scanner.scan(hosts=subred, arguments='-p 1-1024 -sV')

hosts_activos = scanner.all_hosts()
print(f"Hosts activos detectados: {len(hosts_activos)}\n")

# Recorrer cada host encontrado
for host in hosts_activos:
    print(f"Host: {host}")
    for proto in scanner[host].all_protocols():
        puertos = scanner[host][proto].keys()
        for puerto in sorted(puertos):
            info = scanner[host][proto][puerto]
            servicio = info.get('name', 'desconocido')
            version = info.get('version', '')
            producto = info.get('product', '')
            extra = f"{producto} {version}".strip()
            descripcion = f"{servicio} ({extra})" if extra else servicio
            print(f" - Puerto {puerto}: {descripcion}")
    print("-" * 40)

print("\nEscaneo finalizado.")
