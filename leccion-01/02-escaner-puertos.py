import socket

host = "127.0.0.1"
puertos = [21, 22, 80, 443, 3306]

for puerto in puertos:
    s = socket.socket()
    s.settimeout(1)
    if s.connect_ex((host, puerto)) == 0:
        print(f"[+] Puerto {puerto} abierto")
    s.close()
