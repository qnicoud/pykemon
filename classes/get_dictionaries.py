import json
from pathlib import Path

####################################################################################################################
# Get dictionnaries containing all data for the game

def get_types () :
    with open(Path.cwd() / "pokemon_json\pokemon_types.json", 'r') as json_types :
        return json.load(json_types)

def get_attacks () :
    with open(Path.cwd() / "pokemon_json\pokemon_attacks.json", 'r') as json_attacks :
        return json.load(json_attacks)

def get_pokemons () :
    with open(Path.cwd() / "pokemon_json\pokemon_pokemons.json", 'r') as json_pokemons :
        return json.load(json_pokemons)
