#!/usr/bin/env python3
#==================================================================================#
"""
Pykemon
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"    
#==================================================================================#

# Import required modules
from time import sleep

# Import my files
from classes.window_display_management import Input, MainFrame, Window


class App :
    def __init__ (self) :
        self.window = Window()
        self.input = Input()

    def start (self) :

        # Display splash screen
        self.window.clear_window()
        for pokemon in MainFrame("startup").content :
            print (pokemon)
            sleep(0.05)
        sleep(2)

        # Infinite loop used to record inputs util game is exited
        while True :
            # Check input
            self.input.check(self.window, refresh = 0.3)

            # If window was updated, refresh it
            if self.window.state_changed :
                self.window.refresh_window()


##########################################################################################################
## TESTS

# poke = get_pokemons()
# a = poke["Bulbasaur"]["Type"]
# print(a)

app = App()

app.start()

