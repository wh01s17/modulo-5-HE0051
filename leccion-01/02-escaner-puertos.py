import socket

host = "127.0.0.1"
#             ftp, ssh, http, https, mysql/mariadb
puertos_lista = [21, 22, 80, 443, 3306]

for puerto in puertos:
    s = socket.socket()
    s.settimeout(1)     # 1 segundo
    # s.settimeout(0.5)   # medio segundo (500 milisegundos)
    # s.settimeout(0.1)   # 100 milisegundos

    if s.connect_ex((host, puerto)) == 0:
        print(f"[+] Puerto {puerto} abierto")

    s.close()
