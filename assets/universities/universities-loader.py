def carica_universita(path):
    tmp_json = []
    with open(path, "r") as file:
        content = file.read()
    
    tmp_json = json.loads(content)
    names = [item["name"] for item in tmp_json]
    return names



lista_univ = carica_universita("../universities.json")