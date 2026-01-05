import ollama

print("Deleting old model")

ollama.delete(model='universities-finder:latest')

print("Creating ollama model...")

ollama.create(model='universities-finder', 
                      from_='qwen3:8b', 
                      system="Sei uno strumento che analizza del testo quindi NON puoi COMMENTARE e NON fare DOMANDE. " \
                      "Devi estrarre dal testo che ti viene fornito solo 3 cose: Università (che può essere scritto come universit), Corso di Laurea e Voto di Laurea" \
                      "Hai l'obbligo di rispondere seguendo questo format della risposta:" \
                      "Università:" \
                      "Corso di Laurea:" \
                      "Voto di Laurea:" \
                      "il primo ed il secondo campo sono obbligatori, devono contenere entrambi al massimo una cosa e devono avere senso, il terzo completalo solo quando lo trovi con certezza",)

def check_model(model_name):
    # Recupera la lista dei modelli presenti
    response = ollama.list()
    models = [m['model'] for m in response['models']]
    print(models)
    
    if model_name in models:
        print(f"The model \t{model_name}\t is available.")
    else:
        print(f"The model \t{model_name}\t is not available.")

check_model('universities-finder:latest')