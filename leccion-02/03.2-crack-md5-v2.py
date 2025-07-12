import sys
import hashlib
from tqdm import tqdm

def crack_md5():
    if len(sys.argv) != 3:
        print(f"Uso: {sys.argv[0]} <archivo_wordlist> <hash>")
        sys.exit(1)

    wordlist = sys.argv[1]
    hash_input = sys.argv[2]

    try:
        with open(wordlist, 'rt', encoding='latin-1') as dic:
            barra = tqdm(dic, desc="Crackeando", unit=" palabra")

            for word in dic:
                word = word.strip()
                hash_md5 = hashlib.md5(word.encode()).hexdigest()

                if hash_md5 == hash_input:
                    barra.close()
                    print(f"[+] Hash crackeado: {word}")
                    return
            barra.close()
    except FileNotFoundError:
        print(f"[!] Archivo no encontrado: {wordlist}")
        sys.exit(1)

if __name__ == "__main__":
    crack_md5()
