from ollama import chat 
import json
from models_database import *

def load_database(path):
    with open(path, 'r') as file:
        json_text = file.read()
    return json_text

def ollama_subroutine(message):
    response = chat (model='universities-finder', 
    messages=[
    {
        'role': 'user', 
        'content': message
    }
    ],
    think=False,
    stream=False
    )
    
    time_elapsed = ("time elapsed: " + str(response.total_duration / 1000000000) + " sec")
    return response.message.content, time_elapsed

cnt_laureati = 0
database_path = "db.json"
json_text = load_database(database_path)

json_parsed = Body.model_validate_json(json_text)

for utente in json_parsed.utenti:
    if len(utente.occorrenze) != 0:
        for occorrenza in utente.occorrenze:
            if (occorrenza.parola == 'universit'):
                # print(occorrenza)
                res_ollama, time_elapsed = ollama_subroutine(occorrenza.testo)
                print(utente.nome + "\n" + res_ollama + "\n" + time_elapsed)
                