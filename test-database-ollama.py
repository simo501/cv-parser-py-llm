from ollama import chat 
import json

def load_database(path):
    with open(path, 'r') as file:
        json_content = file.read()

    return json.loads(json_content)

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
database_path = "../database.json"
json_parsed = load_database(database_path)

for persona in json_parsed:
    persona_obj = json_parsed[persona]
    for tipo_occorrenza in persona_obj:
        # print(tipo_occorrenza)
        if (tipo_occorrenza == "universita") and len(persona_obj[tipo_occorrenza]) != 0:
            cnt_laureati += 1
            tipo_occorrenze_obj = persona_obj[tipo_occorrenza]
            for num_occorrenza in tipo_occorrenze_obj:
                if (len(tipo_occorrenze_obj) != 0):
                    testo_occorrenza_num = tipo_occorrenze_obj[num_occorrenza]["text"]
                    res_ollama, time_elapsed = ollama_subroutine(testo_occorrenza_num)
                    # print(testo_occorrenza_num)
                    print(persona + "\n" + res_ollama + "\n" + time_elapsed)
                    