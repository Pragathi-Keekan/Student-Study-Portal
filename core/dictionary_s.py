import requests

def get_dictionary_definition(word):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        definitions = [meaning['definitions'][0]['definition'] for meaning in data[0]['meanings']]
        return definitions
    else:
        return f"Error: Unable to retrieve definition. Status code: {response.status_code}"

word = 'beast'
definitions = get_dictionary_definition(word)
if definitions:
    print(f"Definitions of '{word}':")
    for index, definition in enumerate(definitions, start=1):
        print(f"{index}. {definition}")
else:
    print("An error occurred while fetching the definition.")
