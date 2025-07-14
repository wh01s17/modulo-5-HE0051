import hashlib

wordlist = r"/home/wh01s17/Documentos/wordlists/rockyou.txt"
hash_input = "0192023a7bbd73250516f069df18b500"

def crack_md5():
    try:
        with open(wordlist, 'rt', encoding='latin-1') as dic:
            for word in dic:
                word = word.strip()
                hash_md5 = hashlib.md5(word.encode()).hexdigest()

                if hash_md5 == hash_input:
                    print(f"[+] Hash crackeado: {word}")
                    return
    except FileNotFoundError:
        print(f"[!] Archivo no encontrado: {wordlist}")
        return

if __name__ == "__main__":
    crack_md5()
