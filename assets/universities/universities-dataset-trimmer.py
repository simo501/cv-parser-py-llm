import json

content = []

with open("universities-complete.json") as file:
    content = file.read()

json_content = json.loads(content)

# Filtra mantenendo solo gli oggetti con alpha_two_code == 'DE'
filtered_list = []

codes = [
    "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "ES", "FI", 
    "FR", "GR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT", 
    "NL", "PL", "PT", "RO", "SE", "SI", "SK", "US"
]

for item in json_content:
    # Controlla se il valore soddisfa la condizione
    code = item['alpha_two_code']
    if code in codes:
        filtered_list.append(item)

print(filtered_list)

with open("universities-trimmed.json", "w") as f:
    json.dump(filtered_list, f, indent=4, ensure_ascii=False)