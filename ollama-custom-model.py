import ollama

ollama.create(model='universities-finder', 
                      from_='qwen3:8b', 
                      system="Sei uno strumento che analizza del testo, non puoi commentare nulla ne fare domande, hai l obbligo di rispondere nella maniera in cui ti specifico io di seguito: Devi estrarre dal testo che ti viene inoltrato solo 3 cose. 1. Università (obbligatoriamente) 2. il corso di laurea (non obbligatorio) 3. il voto di laurea (non obbligatorio)",)

def check_model(model_name):
    # Recupera la lista dei modelli presenti
    response = ollama.list()
    models = [m['model'] for m in response['models']]
    print(models)
    
    if model_name in models:
        print(f"Il modello \t{model_name}\t è disponibile.")
    else:
        print(f"Modello \t{model_name}\t non trovato.")

check_model('universities-finder:latest')