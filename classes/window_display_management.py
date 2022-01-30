import sys
import os
from time import sleep
import keyboard

from .game_elements import Attack, Action, Object, Pokemon, Type, Void


####################################################################################################################
# Window & display management classes

class SelectBox :
    def __init__ (self, element) : 
        self.width  = 35

        if element.type in ["Game", "PVP"] :
            self.width = 2 * self.width

        # If void object is passed, set is_void to true in order to format an empty structure
        self.is_Void = False

        if type(element).__name__ == "Void" :
            self.is_Void = True

        else :
            self.element = element
            self.h_outline = "**{}**".format((self.width - 2) * "-")
            self.v_outline = [ "*" , "|" ]
            
            # Set content of bottom right of the box
            if type(element).__name__ == "Pokemon" :
                self.l_r_content = element.HP
            elif type(element).__name__ == "Attack" :
                self.l_r_content = element.PP
            elif type(element).__name__ == "Object" :
                self.l_r_content = element.qty
            elif type(element).__name__ == "Action" :
                self.l_r_content = element.type    
             
            
    def set_size (self, width) :
        # Change size of a single box

        self.width = width

    def select_it (self) :
        # Change layout style if selected
    
        self.h_outline = "¤¤{}¤¤".format((self.width - 2) * "=")
        self.v_outline = [ "¤" , "H" ]

    def deselect_it (self) :
        # Change layout style if deselected
    
        self.h_outline = "**{}**".format((self.width - 2) * "-")
        self.v_outline = [ "*" , "|" ]

    def start_up_structure (self) :
        pass
        

    def get_structure (self) :
        # Returns the structure of a single box, 
        # i.e. a list where ech line is a string contiaing the box informations

        if self.is_Void :
            # If box is void, creat an empty box
            self.structure = [
                ( " " * (self.width  + 4) ) for i in range(7)
            ]

        elif self.element.type in ["Game", "PVP"] :
            # If box is a component of the start up menu :
            self.structure = [
                self.h_outline,
                f"{self.v_outline[0]}{ ' ' * ( 2 * (self.width) // 2 ) }{self.v_outline[0]}",
                f"{self.v_outline[1]}{ ' ' * ( (self.width - len(self.element.name)) // 2 ) }{self.element.name}{ ' ' * ( (self.width - len(self.element.name)) // 2 ) }{self.v_outline[1]}",
                f"{self.v_outline[0]}{ ' ' * ( 2 * (self.width) // 2 ) }{self.v_outline[0]}",
                self.h_outline
            ]

        else :
            # If it isn't a void object, create structure of the box
            if type(self.element).__name__ in ["Pokemon", "Attack"] :
                self.element_type = self.element.type.long
            else :
                self.element_type = self.element.type

            # Create the structure of the box
            self.upper_left = " {} |{}".format(
                self.element_type,
                ( " " * ( self.width - 3 - len(self.element_type) )))

            self.upper_left_outline = "{}+{}".format(
                ( "-" * (2 + len(self.element_type) ) ), 
                ( " " * ( self.width - 3 - len(self.element_type) ) ))
            
            self.lower_right = "{}| {} ".format(
                ( " " * ( self.width - 3 - len( str(self.l_r_content) ) ) ), 
                self.l_r_content)

            self.lower_right_outline = "{}+{}".format( 
                ( " " * ( self.width - 3 - len( str(self.l_r_content) ) ) ),
                ( "-" * (2 + len( str(self.l_r_content) ) ) ) )
            
            # In case the name of the element is two long for the box, trim it and add ... to the end
            self.name_displayed = self.element.name if len(self.element.name) <= (self.width - 4) else ( self.element.name[:(self.width - 3)] + "..." )
            
            center_center = self.width - ( len(self.element.name) )
            self.center = "{a}{b}{c}".format(a = " " * (center_center // 2), 
                                            b = self.element.name, 
                                            c = " " * ( (center_center if ( center_center % 2 ) == 0 else center_center + 1) // 2 ) )

            # Actual structure of the box
            self.structure = [
                self.h_outline,
                f"{self.v_outline[0]}{self.upper_left}{self.v_outline[0]}",
                f"{self.v_outline[1]}{self.upper_left_outline}{self.v_outline[1]}",
                f"{self.v_outline[1]}{self.center}{self.v_outline[1]}",
                f"{self.v_outline[1]}{self.lower_right_outline}{self.v_outline[1]}",
                f"{self.v_outline[0]}{self.lower_right}{self.v_outline[0]}",
                self.h_outline
            ]

        return self.structure
     


class Menu :
    def __init__ (self, elem1, elem2, elem3, elem4) :
        self.name = type(elem1).__name__
        
        self.u_l_box = SelectBox(elem1)
        self.u_r_box = SelectBox(elem2)
        self.l_l_box = SelectBox(elem3)
        self.l_r_box = SelectBox(elem4)
        
        # Poition of the "cursor" in the menu
        self.cursor_pos   = [0, 0]

        # Default selected item
        self.select = self.u_l_box
        self.select.select_it()         

    def change_selected (self, motion) :
        # Change the selected box in the menu

        # Get the new position of the cursor by adding the motion vector to the actula position
        self.cursor_pos = [ abs(p + m) for p,m in zip( self.cursor_pos, motion ) ]
        
        self.select.deselect_it()        

        # Set the required box as selected according to new pos, except if new pos refers to a void object
        if      self.cursor_pos == [0, 0] and not self.u_l_box.is_Void :
            self.select = self.u_l_box
        elif    self.cursor_pos == [0, 1] and not self.u_r_box.is_Void :
            self.select = self.u_r_box
        elif    self.cursor_pos == [1, 0] and not self.l_l_box.is_Void :
            self.select = self.l_l_box
        elif    self.cursor_pos == [1, 1] and not self.l_r_box.is_Void :
            self.select = self.l_r_box
        else :
            self.cursor_pos = [ abs(p + m) for p,m in zip( self.cursor_pos, motion ) ]
        
        # Select the required box
        self.select.select_it()
        
    
    def render_menu (self) :
        # Render the menu into a list so it can be displayed in the window.

        # Render the first row of boxes
        first_row = [
            f"{i}  {j}" for i,j in zip( self.u_l_box.get_structure(), self.u_r_box.get_structure() if not self.u_l_box.element.type in ["Game" , "PVP"] else [ "" for rep in range(len(self.u_r_box.get_structure()))])
        ]

        # Render the second row of boxes
        second_row = [
            f"{i}  {j}" for i,j in zip( self.l_l_box.get_structure(), self.l_r_box.get_structure() if not self.l_l_box.element.type in ["Game" , "PVP"] else [ "" for rep in range(len(self.l_r_box.get_structure()))])
        ]

        # Pool the two rows together
        first_row.extend(second_row)

        return first_row

    def print_menu (self) :
        #Test function to verify menus are formated corectly

        for i in self.render_menu() :
            print(i)        
    


class MainFrame :
    def __init__ (self, type) :
        if type == "startup" :
            self.content = ["                                .::.                          ",
                            "                              .;:**'                          ",
                            "                              `                               ",
                            "  .:XHHHHk.              db.   .;;.     dH  MX                ",
                            "oMMMMMMMMMMM       ~MM  dMMP :MMMMMR   MMM  MR      ~MRMN     ",
                            "QMMMMMb  'MMX       MMMMMMP !MX' :M~   MMM MMM  .oo. XMMM 'MMM",
                            "  `MMMM.  )M> :X!Hk. MMMM   XMM.o'  .  MMMMMMM X?XMMM MMM>!MMP",
                            "   'MMMb.dM! XM M'?M MMMMMX.`MMMMMMMM~ MM MMM XM `' MX MMXXMM ",
                            "    ~MMMMM~ XMM. .XM XM`'MMMb.~*?**~ .MMX M t MMbooMM XMMMMMP ",
                            "     ?MMM>  YMMMMMM! MM   `?MMRb.    `'''   !L'MMMMM XM IMMM  ",
                            "      MMMX   'MMMM'  MM       ~%:           !Mh.''' dMI IMMP  ",
                            "      'MMM.                                             IMX   ",
                            "       ~M!M                                             IMP   ",
                            ]
        
        elif type == "map" :
            pass

        elif type == "fight" :
            pass



class Input :
    def __init__ (self) :
        pass

    def check (self, window, refresh = 0.5) :
        for key in ["haut", "bas", "droite", "gauche"] :
            if keyboard.is_pressed(key) :
                window.change_menu_sel(key)
                sleep(refresh)

        if keyboard.is_pressed("enter") :
            window.validate_item()
            sleep(refresh)

        elif keyboard.is_pressed("backspace") :
            if not window.displayed_menu.select.element.type in ["Game", "PVP"] :
                window.change_components(None, "Action")
                sleep(refresh)

        elif keyboard.is_pressed("esc") :
            sys.exit()



class Window :
    def __init__ (self, x = 200, y = 50) :
        self.x_len = x
        self.y_len = y

        # Main frames are not prgrammed yet
        self.mainframe      = None

        # Set the possible menus of the window
        self.startup_menu    = Menu(Action("Game"),    Void(),   Action("PVP"),  Void())
    
        self.action_menu    = Menu(Action("Attack"),    Action("Object"),       Action("Pokemon"),      Void())
        self.pokemon_menu   = Menu(Pokemon("Pikachu"),  Pokemon("Squirtle"),    Pokemon("Charmander"),  Pokemon("Bulbasaur"))
        self.object_menu    = Menu(Object(),            Object(),               Object(),               Object())
        self.atk_menu       = Menu(Attack(),            Attack(),               Attack(),               Attack())

        # By default, the action menu is displayed
        self.displayed_menu = self.startup_menu

        # Boolean th check wether anything was changed in the game
        self.state_changed = True

        self.outline = [
            "-", "|", "+"
        ]
        self.title = "Pokemon.py"

    def set_menu_contents (self, menu, list) :
        if menu == "Pokemon" :
            self.pokemon_menu = Menu(list[0], list[1], list[2], list[3])
        elif menu == "Object" :
            self.object_menu = Menu(list[0], list[1], list[2], list[3])
        elif menu == "Attack" :
            self.atk_menu = Menu(list[0], list[1], list[2], list[3])



    def change_components (self, mainframe, asked_menu) :
        # If a combat is entered or left, change the main frame
        if not mainframe == None :
            self.mainframe  = mainframe
        
        # If an item is selected in the menu, change the menu and the main frame if an action is performed
        if not asked_menu == None :

            for choice, choosed_menu in {   "Game"      : self.action_menu, 
                                            "PVP"       : self.action_menu, 
                                            "Action"    : self.action_menu, 
                                            "Pokemon"   : self.pokemon_menu, 
                                            "Object"    : self.object_menu, 
                                            "Attack"    : self.atk_menu
                                        }.items() :
                if asked_menu == choice :
                    # TO ADD --> refreshing mainframe if action is required
                    self.displayed_menu = choosed_menu
                    break
 
        # Boolean value to check wether the window should be rendered or not
        self.state_changed = True
    
    def change_menu_sel (self, input) :
        # Change the selected box in the menu
        self.state_changed = True
        if input == "haut" :
            self.displayed_menu.change_selected([-1,0])
        elif input == "bas" :
            self.displayed_menu.change_selected([-1,0])
        elif input == "droite" :
            self.displayed_menu.change_selected([0,-1])
        elif input == "gauche" :
            self.displayed_menu.change_selected([0,-1])


    def validate_item (self) :
        # If a box has been validated with enter key, render corresponding menu 
        self.item_validated = type(self.displayed_menu.select.element).__name__

        if self.item_validated == "Action" :

            for i in ["Game", "PVP", "Pokemon", "Object", "Attack"] :
                if self.displayed_menu.select.element.type == i :
                    self.change_components(None, i)
                    break


    def display_window (self) :
        self.actual_menu = [
            f"{self.outline[1]}{' ' * ( (self.x_len - 2 - len(menu_line)) // 2)}{menu_line}{' ' * ( (self.x_len - 2 -len(menu_line)) // 2)}{self.outline[1]}" for menu_line in self.displayed_menu.render_menu()
        ]

        for menu_header in [
            f"{self.outline[2]}{self.outline[0] * (self.x_len - 2)}{self.outline[2]}",
            f"{self.outline[1]} Choose {self.displayed_menu.name} {self.outline[1]}{' ' * (self.x_len - 12 - len(self.displayed_menu.name))}{self.outline[1]}",
            f"{self.outline[2]}{self.outline[0] * (self.x_len - 2)}{self.outline[2]}"
            ] :
            self.actual_menu.insert(0, menu_header)

        self.actual_menu.append(f"{self.outline[2]}{self.outline[0] * (self.x_len - 2)}{self.outline[2]}")

        
        for i in self.actual_menu :
            print (i)
        

        self.state_changed = False

    def clear_window (self) :
        command = 'clear'
        if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)

    def refresh_window (self) :
        self.clear_window()
        self.display_window()