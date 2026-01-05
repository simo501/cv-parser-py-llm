import argparse
import os 
import re
import json
from models_database import *


def get_filenames(input_folder):
    try:
        elementi = os.listdir(input_folder)
        files = []
        for f in elementi:
            # se non sono sotto cartelle ne file dot 
            if os.path.isfile(os.path.join(input_folder,f)) and f[0] != ".":
                files.append(f)
        return tuple(files)
    except FileNotFoundError:
        print(f"Errore: la input_folder '{input_folder}' non esiste")
        return ()
    except PermissionError:
        print(f"Errore: permessi insufficienti per accedere a '{input_folder}'")
        return ()

def parse_filename(filename):
    if (filename[0] == "."):
        return None
    sub = re.sub(r'\d', '', filename)
    sub = sub.strip("_")
    sub = sub.strip(".txt")
    sub = sub[:-2]
    sub = sub.strip("_")
    return sub.replace("_", " ").title()


def word_with_context(testo, keywords, n_parole_prima=6, n_parole_dopo=12):
    # Divide il testo in parole
    parole = re.findall(r'\b\w+\b', testo.lower())
    
    occurences_list = []
    
    for parola in keywords:
        for i, p in enumerate(parole):
            if p == parola.lower():
                # Prendi n parole prima
                inizio = max(0, i - n_parole_prima)
                prima = parole[inizio:i] # nella forma di list
                
                # Prendi n parole dopo
                fine = min(len(parole), i + n_parole_dopo + 1)
                dopo = parole[i+1:fine] # nella forma di list
                
                # rendiamo prima e dopo (che sono 2 list) string uniche
                prima_joined = " ".join(prima)
                dopo_joined  = " ".join(dopo)
                text = " ".join([prima_joined, parola, dopo_joined]) 
                try:
                    occurences_list.append(Occorrenza(parola=parola, testo=text))
                except ValidationError as err:
                    print(f"There's some problem with one occurence\n{err}")
    
    return occurences_list


def dump_by_keywords(input_folder, keywords, output_file=False):
    cnt_analyzed_files = 0
    
    user_list = []
    files= get_filenames(input_folder)
    files_number = len(files)

    for filename in files:
        with open("".join([input_folder, filename]), 
                  "r", 
                  encoding="utf-8", 
                  errors="ignore") as file:
            person_name = parse_filename(filename)
            testo = file.read().lower()
            occurrences = word_with_context(testo, keywords)            
            try:
                utente = UtenteOccorrenze(nome=person_name, occorrenze=occurrences)
            except ValidationError as err:
                print(f"There's ({filename}) causing problems\n{err}")
            user_list.append(utente)
            cnt_analyzed_files += 1
            print("\r" + str(cnt_analyzed_files) + "/" + str(files_number), end="", flush=True)

    if (output_file):
        body = BodyUtenti(utenti=user_list)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(body.model_dump(), f, indent=4, ensure_ascii=False)
        
    print(f"\n{cnt_analyzed_files} files analyzed.\n")


    

def main():
    parser = argparse.ArgumentParser(description="QUESTO SCRIPT ANALIZZA SOLO I TESTI")
    parser.add_argument("--input-folder", "-i", help="FOLDER con i FILE da analizare", required=True)
    parser.add_argument("--output-json", "-ojson", help="NOME file output JSON", required=True)
    
    args = parser.parse_args()
    
    # "universit" 
    # ha lo scopo di evitare problemi di encoding di sorta che possono nascera a causa 
    # della a accentata in università 
    dump_by_keywords(args.input_folder, ["universit", "liceo", "diploma"], args.output_json)


if __name__ == "__main__":
    main()