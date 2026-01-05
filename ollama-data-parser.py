import json
import argparse
from ollama import chat 
from models_database import *

def load_database(path):
    with open(path, 'r') as file:
        json_text = file.read()
    return json_text

def build_user_model_list(username, universities: list):
    universities_model_list = []
    for university in universities:
        try:
            name, course, mark = university
            universities_model_list.append(Universita(nome=name, corso=course, voto=mark))
        except ValidationError as err:
            print(f"While preparing {username} model an error occured\n{err}")

    user_model: UtenteUniversita
    try: 
        user_model = UtenteUniversita(nome=username, universita=universities_model_list)
    except ValidationError as err:
        print(f"the final modeling stage of {username} has failed\n{err}")

    return user_model


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

def ollama_response_parser(response):
    university = str()
    course = str()
    mark = str()
    try:
        university = response.split('\n')[0].split(':')[1].strip()
        course = response.split('\n')[1].split(':')[1].strip()
        mark = response.split('\n')[2].split(':')[1].strip()
    except:
        print(f"ERROR in ollama_response_parser with args: {response}") 
    return university, course, mark 

def build_json(input_json_path, output_json_path):
    print("Loading JSON text..")
    json_text = load_database(input_json_path)
    print("Parsing JSON..")
    json_parsed = BodyUtenti.model_validate_json(json_text)

    users_model_list = []
    for index_user, utente in enumerate(json_parsed.utenti):
        print(f"Extracting data from {utente.nome} - {index_user}/{len(json_parsed.utenti)} --------------")
        user_universities = []
        if len(utente.occorrenze) != 0:
            for occorrenza in utente.occorrenze:
                if (occorrenza.parola == 'universit'):
                    print(occorrenza.testo)
                    ollama_response, time_elapsed = ollama_subroutine(occorrenza.testo)
                    print("\t" + ollama_response.replace("\n", "\n\t") + "\n" + time_elapsed)
                    university, course, mark = ollama_response_parser(ollama_response)
                    user_universities.append([university,course,mark])

        users_model_list.append(build_user_model_list(utente.nome, user_universities))

    final_model = BodyUtenteUniversita(utenti=users_model_list)

    with open(output_json_path, "w", encoding="utf-8") as f:
                json.dump(final_model.model_dump(), f, indent=4, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description="QUESTO SCRIPT ESTRAE LE UNIVERSITÀ DAL JSON")
    parser.add_argument("--input-json", "-i", help="PATH json da ANALIZZARE", required=True)
    parser.add_argument("--output-json", "-ojson", help="NOME file output JSON", required=True)
    
    args = parser.parse_args()

    build_json(args.input_json, args.output_json)

if __name__ == "__main__":
    main()