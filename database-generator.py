import argparse
import os 
import re
import json


def get_filenames(input_folder):
    try:
        # Ottiene tutti gli elementi nella cartella
        elementi = os.listdir(input_folder)
        # Filtra solo i file (esclude le sottocartelle)
        files = [f for f in elementi if os.path.isfile(os.path.join(input_folder, f))]
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

    # leviamo i numeri che non sono prevedibili
    sub = re.sub(r'\d', '', filename)
    # leviamo gli underscores
    sub = sub.strip("_")
    # estensione
    sub = sub.strip(".txt")
    # rimuoviamo cv eliminando gli ultimi 2 caratteri
    sub = sub[:-2]
    # leviamo ulteriori under scores fastidiosi
    sub = sub.strip("_")
    # sub = sub.replace("_", " ")
    return sub


def word_with_context(testo, keywords, n_parole_prima=3, n_parole_dopo=15):
    # Divide il testo in parole
    parole = re.findall(r'\b\w+\b', testo.lower())
    risultati = {}
    
    for parola in keywords:
        
        contatore_occorrenze = 0
        dizionario_occorrenze = {}
        
        for i, p in enumerate(parole):
            if p == parola.lower():
                # Prendi n parole prima
                inizio = max(0, i - n_parole_prima)
                prima = parole[inizio:i] # nella forma di list
                
                # Prendi n parole dopo
                fine = min(len(parole), i + n_parole_dopo + 1)
                dopo = parole[i+1:fine] # nella forma di list
                
                contatore_occorrenze += 1

                # rendiamo prima e dopo string uniche
                prima_joined = " ".join(prima)
                dopo_joined  = " ".join(dopo)

                # destrutturazione in prima e dopo
                # dizionario_occorrenze[contatore_occorrenze] = {"prima": prima_joined, "dopo": dopo_joined}
                text = " ".join([prima_joined, parola, dopo_joined]) 
                dizionario_occorrenze[contatore_occorrenze] = {"text" : text}

                # risultati.append((prima, p, dopo))

        risultati[parola] = dizionario_occorrenze
    
    # ritorna ad un json con oggetto la persona ed oggetto annidato le parole
    # e le occorrenze
    return risultati


def analyze_for_keywords(input_folder, keywords, output_file=False):
    index_file_analyzed = 0
    
    ret_dict = {}

    for filename in get_filenames(input_folder):
        index_file_analyzed += 1
        with open("".join([input_folder, filename]), 
                  "r", 
                  encoding="utf-8", 
                  errors="ignore") as file:
            nome = parse_filename(filename)
            print(f"sto analizzando {nome}")

            # leggiamo tutto il testo per SENZA case sensitive
            testo = file.read().lower()
            
            ret_analysis = word_with_context(testo, keywords)
            
            # oggetto json padre con nome persona
            ret_dict[nome] = ret_analysis

    print(json.dumps(ret_dict, indent=4))

    if (output_file):
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(ret_dict, f, indent=4, ensure_ascii=False)
        
    print(f"analizzati {index_file_analyzed} files.\n")


    

def main():
    parser = argparse.ArgumentParser(description="QUESTO SCRIPT ANALIZZA SOLO I TESTI")
    parser.add_argument("--input-folder", "-i", help="FOLDER con i FILE da analizare", required=True)
    parser.add_argument("--output-json", "-ojson", help="NOME file output JSON", required=True)
    
    args = parser.parse_args()
    
    # "universit" 
    # ha lo scopo di evitare problemi di encoding di sorta che possono nascera a causa 
    # della a accentata in università 
    analyze_for_keywords(args.input_folder, ["universit", "liceo", "laurea", "diploma"], args.output_json)


if __name__ == "__main__":
    main()