import hashlib
import os

# Cartella da controllare
DIR = "ready pdfs/"

hash_map = {}

def sha256(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

for filename in os.listdir(DIR):
    file_path = os.path.join(DIR, filename)
    if os.path.isfile(file_path):
        file_hash = sha256(file_path)
        print(f"File: {file_path}, SHA-256: {file_hash}")
        if file_hash in hash_map:
            print(f"CANCELLO il Duplicato trovato: {file_path} (uguale a {hash_map[file_hash]})")
            os.remove(file_path)
        else:
            hash_map[file_hash] = file_path
