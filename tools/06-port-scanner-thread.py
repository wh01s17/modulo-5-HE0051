import socket
import sys 
from concurrent.futures import ThreadPoolExecutor

PUERTOS_COMUNES = {
    20: "FTP-DATA",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    67: "DHCP (Server)",
    68: "DHCP (Client)",
    69: "TFTP",
    80: "HTTP",
    110: "POP3",
    111: "RPCBind",
    119: "NNTP",
    123: "NTP",
    135: "Microsoft RPC",
    137: "NetBIOS Name",
    138: "NetBIOS Datagram",
    139: "NetBIOS Session",
    143: "IMAP",
    161: "SNMP",
    179: "BGP",
    389: "LDAP",
    443: "HTTPS",
    445: "SMB",
    465: "SMTPS",
    514: "Syslog",
    515: "LPD (Line Printer Daemon)",
    587: "SMTP (TLS)",
    631: "IPP (Impresión)",
    993: "IMAPS",
    995: "POP3S",
    1080: "SOCKS Proxy",
    1433: "Microsoft SQL Server",
    1521: "Oracle DB",
    1723: "PPTP VPN",
    2049: "NFS",
    2181: "Zookeeper",
    2375: "Docker API (sin TLS)",
    2376: "Docker API (con TLS)",
    2483: "Oracle DB (TCP)",
    2484: "Oracle DB (SSL)",
    3306: "MySQL",
    3389: "RDP (Remote Desktop)",
    3690: "Subversion",
    4000: "Desarrollo/Custom",
    40105: "Random High Port (Ej.)",
    4444: "Metasploit Handler",
    5000: "Flask / UPnP",
    5060: "SIP",
    5432: "PostgreSQL",
    5672: "RabbitMQ",
    5900: "VNC",
    5985: "WinRM (HTTP)",
    5986: "WinRM (HTTPS)",
    6379: "Redis",
    7001: "WebLogic",
    8000: "HTTP-alt / Dev",
    8008: "HTTP-alt",
    8080: "HTTP-alt / Proxy",
    8081: "HTTP-alt",
    8443: "HTTPS-alt",
    8888: "Dev Tools / Proxy",
    9000: "PHP-FPM / Sentry",
    9200: "Elasticsearch",
    9443: "HTTPS-alt",
    9999: "Demo / Exploits",
    10000: "Webmin / Backup Exec",
    27017: "MongoDB",
    50000: "SAP / Sybase",
    55000: "OSSEC",
    5601: "Kibana",
    6379: "Redis",
    8086: "InfluxDB",
    3000: "Node js, OWASP Juice shop, etc"
}

def port_scanner(ip, port):
    try:
        # Crear un socket TCP
        s = socket.socket()
        s.settimeout(0.5)
        s.connect((ip, port))

        s.close()

        servicio = PUERTOS_COMUNES.get(port, "Servicio desconocido")

        print(f"[+] Puerto abierto: {port} ({servicio})")
    except:
        pass

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <IP>")
        sys.exit(1)
    
    ip = sys.argv[1]

    with ThreadPoolExecutor(max_workers=100) as executer:
        for port in range(1, 65536):
            executer.submit(port_scanner, ip, port)
