from .get_dictionaries import get_attacks, get_pokemons, get_types

####################################################################################################################
# Game elements classes

class Type :
    def __init__ (self, name = "Normal") :
        types           = get_types()
        self.long       = types[name]["Long"]
        self.short      = types[name]["Short"]
        self.strength   = types[name]["Strength"]

    def get_Str (self, type) :
        return self.strength[type]



class Attack :
    def __init__ (self, name = "Attack", type = "Type", power = "Power", precision = "precision", max_pp = "PP") :
        attack = get_attacks ()
        # Following to be removed -> is juste her to prevent warning
        attack = attack

        self.name       = name
        self.type       = type
        self.power      = power
        self.precision  = precision
        self.PP         = max_pp
        self.max_PP     = max_pp

    def is_used (self) :
        self.PP = (self.PP - 1) if self.PP >= 0 else 0
    
    def is_refilled (self, gain) :
        self.PP = (self.PP + gain) if (self.PP + gain) <= self.max_PP else self.max_PP

    

class Pokemon :
    def __init__(self, name) :
            pokemon         = get_pokemons ()

            self.name       = pokemon[name]["Name"]
            self.id         = pokemon[name]["Id"]
            self.type       = Type(pokemon[name]["Type"])

            self.lvl        = pokemon[name]["Level"]
            self.HP         = pokemon[name]["HP"]

            self.atkN       = pokemon[name]["Attack"]
            self.defN       = pokemon[name]["Defence"]
            self.atkS       = pokemon[name]["AttackSpe"]
            self.atkS       = pokemon[name]["DefenceSpe"]
            self.speed      = pokemon[name]["Speed"]

            self.atk_list   = pokemon[name]["AttackList"]

            self.sprite     = pokemon[name]["Sprite"]
 
            self.status     = None
    
    def attack (self, name_atk) :
        if name_atk in self.atk :
            pass
        else :
            print("Unknown attack...")

    def got_hurt () :
        pass

    def use_object () :
        pass

    def update_status () :
        pass

    def display_health () :
        pass

    def display_sprite () :
        pass



class Object :
    def __init__ (self, qty = 0) :
        self.qty = qty
        self.type = "type"
        self.name = "Object"
        pass



class Void :
    def __init__ (self) :
        self.type = "Void"



class Action :
    def __init__ (self, type) :
        self.type = type

        if self.type == "Pokemon" :
            self.name = "Change actual Pokemon"

        elif self.type == "Object" :
            self.name = "Use object"
        
        elif self.type == "Attack" :
            self.name = "Choose attack !"
        
        elif self.type == "Game" :
            self.name = "Play the game ! "

        elif self.type == "PVP" :
            self.name = "PVP : fight to death !"