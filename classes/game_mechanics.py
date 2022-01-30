####################################################################################################################
# Game mechanics classes

class CombatManager :
    def __init__ (self, pokemon1, pokemon2) :
        self.p1 = pokemon1
        self.p2 = pokemon2

        self.winner = None


class Player :
    def __init__ (self) :
        self.pokemons   = []
        self.objects    = []
        
    def add_pokemon (self, pokemon) :
        self.pokemons.append(pokemon)

    def remove_pokemon (self, pokemon_name) :
        for id in range(len(self.pokemons)) :
            if self.pokemons[id].name == pokemon_name :
                self.pokemons[id].pop()

    def set_current_pokemon (self, pokemon_name) :
        for poke in self.pokemons :
            if poke.name == pokemon_name :
                self.current_pokemon = poke