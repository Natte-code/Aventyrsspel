import time
import random
import curses
import os

#alternativt: koden ska göra terminalen i fullscreen

#kod skaffad från Chatgpt och används för att insperara denna kod.
####################################################################################################
# Loggan definierad som en lista av strängar
logo = [
    " ________  ___  ___  ___  ________                    ",
    "|\\   __  \\|\\  \\|\\  \\|\\  \\|\\_____  \\                   ",
    "\\ \\  \\|\\  \\ \\  \\\\\\  \\ \\  \\\\|___/  /|                  ",
    " \\ \\  \\\\\\  \\ \\  \\\\\\  \\ \\  \\   /  / /                  ",
    "  \\ \\  \\\\\\  \\ \\  \\\\\\  \\ \\  \\ /  /_/__                 ",
    "   \\ \\_____  \\ \\_______\\ \\__\\\\________\\               ",
    "    \\|___| \\__\\|_______|\\|__|\\|_______|              ",
    "          \\|__|                                       ",
    "                                                     ",
    " ________  ___       ________  ________  ___  ___    ",
    "|\\   ____\\|\\  \\     |\\   __  \\|\\   ____\\|\\  \\|\\  \\   ",
    "\\ \\  \\___|\\ \\  \\    \\ \\  \\|\\  \\ \\  \\___|\\ \\  \\\\\\  \\  ",
    " \\ \\  \\    \\ \\  \\    \\ \\   __  \\ \\_____  \\ \\   __  \\ ",
    "  \\ \\  \\____\\ \\  \\____\\ \\  \\ \\  \\|____|\\  \\ \\  \\ \\  \\",
    "   \\ \\_______\\ \\_______\\ \\__\\ \\__\\____\\_\\  \\ \\__\\ \\__\\",
    "    \\|_______|\\|_______|\\|__|\\|__|\\_________\\|__|\\|__|",
    "                                 \\|_________|         "
]

def logo_print(logo, delay=0.15):
    for line in logo:
      print(line)
      time.sleep(delay) 
#funktionen skriver ut loggan rad för rad med tiden 0.2 s per rad.



def start_screen(name): #startar start skärmen, förklarar hur man spelar och visar loggan
   print("")
   print("\n" * 100)
   print("")
   print("välkommen till ♦Quiz Clash♦")
   time.sleep(1)
   print("")
   print("....")
   print("")
   time.sleep(1)
   logo_print(logo)
   time.sleep(1)
   print("")
   print("""Hur man spelar:
                Rör dig med WASD eller PILLAR-tangenterna. 
                Samla mynt, öppna lådor och upptäck klassrum. 
                Svara på lärarens frågor. Fel svar leder till turordningsbaserade strider.
                Håll terminalen i FULL SCREEN!!
                Tryck "i" för att öppna ditt inventory (går ej att släppa saker, så använd varsamt!)
                Lycka till!!
         """)
   print("")
   print("\nTryck på ENTER knappen för att starta spelet!")
   input()


if __name__ == "__main__":
    start_screen(NameError)
#Kontrollerar om filen körs direkt (inte importeras som en modul).

name = input("innan spelet börjar helt... Ange ditt namn: ")






###########################################################################

#classes för allt i spelet
#altså där vi lagrar all info om alla saker som kan förändras

#koden skrivs av nathaniel och eliot

class Item:
    def __init__(self, potion, coin, sword, shield, totems):
        self.potion = potion
        self.coin = coin
        self.sword = sword
        self.shield = shield
        self.totems = totems

class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health
        self.inventory = {"swords": {}, "potions": {}, "shields": 0, "totems": 0}
        self.coins = 5
        self.max_inventory = 10

    def attack(self, sword_name):
        if sword_name in self.inventory["swords"]:
            min_damage, max_damage = self.inventory["swords"][sword_name]
            critical = random.random() < 0.05  # 5% chans för kritisk träff
            damage = random.randint(min_damage, max_damage)
            if critical:
                damage *= 2
                print("Kritisk träff")
            return damage
        else:
            print("Fel svar, försök igen!")
            return 0

    def heal(self, potion_type):
        if potion_type in self.inventory["potions"]:
            heal_amount = self.inventory["potions"].pop(potion_type)
            self.health += heal_amount
            self.health = min(self.health, 100)  # Max hälsa är 100
            print(f"Du använde {potion_type} potion och healade {heal_amount} HP!")
        else:
            print("Du har inte den potionen")

    def passive_block(self):
        if self.inventory["shields"] > 0:
            return random.random() < 0.3  # 30% chans att blockera
        return False

    def add_item(self, item_type, item_name=None, value=0):
        if len(self.inventory) >= self.max_inventory:
            print("Inventory fullt!")
            return False
        if item_type == "coins":
            self.coins += value
        elif item_type == "totems":
            self.inventory["totems"] += value
        elif item_type == "shields":
            self.inventory["shields"] += value
        else:
            self.inventory[item_type][item_name] = value

    def use_totem(self):
        if self.inventory["totems"] > 0:
            self.inventory["totems"] -= 1
            self.health = 100
            print("Du använde en totem, HP 100 nu!")
            return True
        return False

class Teacher:
            def __init__(self, name, health, damage):
                self.name = name
                self.health = health
                self.damage = damage

#koden för combat systemet
#--------------------------------------------------------------------------
def combat_round(player, teacher):
        #spelarens tur (spelaren börjar alltid)
    print(f"\n{player.name}'s turn!")
    print(f"\n ditt Inventory: {player.inventory} ")

    if player.inventory["potions"]:
        action = input("Välj en attack (attack/heal/stand)").strip().lower()
    else:
        action = "attack/stand" #Använder attack eller stand om det inte finns några potions

#attack, spelaren får en lista på vad den kan använda som attack, om spelaren inte har några svärd så kan den anävnda handen som gör base damage
#om spelaren gör damage med svärd läggs base skadan på plus svärdets extra stats
    if action == "attack":
        print("tillgängliga svärd: ", list(player.inventory["swords"].keys())) 
        sword = input("Välj svärd (eller tryck ENTER om du inte har några / vill slå med handen): ").strip().lower()
        damage = player.attack(sword)
        teacher.health -= damage
        print(f"du attackerade {teacher.name} med {"Dina händer" if sword =="" else sword}, som gjorde {damage} skada!")

#om spelaren väljer heal ska den ge spelare en lista på vilken heal potion spelaren kan använda sedan välja den, den tar mängden den healar och lägger i en-
#variabel så den kan printas på ett bättre sätt
    if action == "heal":
        print("Svärd du har:", list(player.inventory["swords"].keys()))
        potion = input("välj din potion (Normal / Epic): ").strip().lower()
        heal_amount =  player.heal(potion)
        player.health += heal_amount #ändrar spelarens hälsa
        print(f"Du använde {potion}, vilket helade dig {heal_amount}!")
        potion -= player.potions #tar bort potion som precis användits ur spelarens inventory
        print("Du har {player.potions} kvar.")


    elif action == "stand":
        print("Du stog ditt kast, Nästa persons tur!")

    #lärarens tur
    #vi ska lägga in passiv block att det är 20% chans att blocka 100% skada
    if teacher.health > 0:
        print(f"{teacher.name}s tur")
        damage = teacher.attack()

        if player.block():
            print("Din sköld blockerade all skada")
            damage = 0
        else:
            print(f"{teacher.name} attackerade för {damage} damage!")
            player.health -= damage

        print(f"{player.name} HP efter attack: {player.health}")


        if teacher.health == 0:
            print("Du van!")

        if player.health == 0:
            print("Du förlorade")
    


#--------------------------------------------------------------------------



#koden är skriven helt av nathaniel och skrivet HELT från scratch. inga idér från intenet utan helt från grunden upp.
#koden ska trigga när dem olika sluta ska triggas
#--------------------------------------------------------------------------

####################################
#importerad från chatgpt för att tömma terminalen
def clear_terminal_visual():
    print("\n" * 1000)

# Använder funktionen


##################################
def end1():
    clear_terminal_visual()
    print(""" 
 __   __            ____  _          _   _ 
 \ \ / /__  _   _  |  _ \(_) ___  __| | | |
  \ V / _ \| | | | | | | | |/ _ \/ _` | | |
   | | (_) | |_| | | |_| | |  __/ (_| | |_|
   |_|\___/ \__,_| |____/|_|\___|\__,_| (_)


    --Tack för du har spelat Quiz Clash--
    --Spela igen för hela slutet--
    --Slut 1 av 4, (Bad ending)--
    
    """)
    exit()

def end2():
    clear_terminal_visual()
    print("""
__   __                     _       _ 
\ \ / /__  _   _  __      _(_)_ __ | |
 \ V / _ \| | | | \ \ /\ / / | '_ \| |
  | | (_) | |_| |  \ V  V /| | | | |_|
  |_|\___/ \__,_|   \_/\_/ |_|_| |_(_)

    --Tack för du har spelat Quiz Clash--
    --Gjord av Nathaniel, Felix och Elliot--
    --Slut 2 av 4, (Good ending)--""")
    exit()

def end3():
    clear_terminal_visual()
    print("""
    _     __           _     _       
   / \   / _|_ __ __ _(_) __| |      
  / _ \ | |_| '__/ _` | |/ _` |      
 / ___ \|  _| | | (_| | | (_| |_ _ _ 
/_/   \_\_| |_|  \__,_|_|\__,_(_|_|_)

    --Tack för du har spelat Quiz Clash--
    --Spela igen för hela slutet--
    --Slut 3 av 4, (afraid ending)--""")
    exit()

def end4():
    clear_terminal_visual()
    print("""
                        _    __   _         _   
 _ __     __ _    ___  (_)  / _| (_)  ___  | |_ 
| '_ \   / _` |  / __| | | | |_  | | / __| | __|
| |_) | | (_| | | (__  | | |  _| | | \__ \ | |_ 
| .__/   \__,_|  \___| |_| |_|   |_| |___/  \__|
|_|                                             
    --Tack för du har spelat Quiz Clash--
    --Spela igen för hela slutet--
    --Slut 4 av 4, (pacifist ending)--""")
    exit()
    
#--------------------------------------------------------------------------


###########################################################################
#koden för rörelse i spelet och att skapa spelkartan
#bas kod är skaffad av ChatGPT och modifierad av Felix

def main(stdscr):
     # Initiera curses
    curses.curs_set(0)  # Dölj markören
    stdscr.nodelay(1)   # Gör getch icke-blockerande
    stdscr.timeout(2000) # Ställ in en timeout för getch (ms)
    
     # Spelvariabler
    rows, cols = 40, 40  # Storlek på spelplanen
    player_pos = [38, 19]  # Startposition för spelaren (centrerad)
    block_pos = []  # Position för objekt
    goal_pos = [20, 20]  # Positionen för rörbart objekt#
    door_pos = [[13, 1], [12, 2], [11, 3], [33, 1], [32, 2], [31, 3]]
    wall_hole = [30, 0]
    key = None            # Håller koll på vilken knapp som trycks
    message = ""
    while True:
        # Ritning av spelplanen
         stdscr.clear()
         for r in range(rows):
             for c in range(cols):
                 # Rita väggar på kanterna
                 if (r == 0 or r == rows - 1 or c == 0 or c == cols - 1) and (r, c) != wall_hole:
                     stdscr.addch(r, c, '#')  # Vägg
                 elif [r, c] in door_pos:
                     stdscr.addch(r, c, '/')
                 elif [r, c] in block_pos:
                     stdscr.addch(r, c, 'B') # Placerar object
                 elif [r, c] == goal_pos:
                     stdscr.addch(r, c, 'X')  # Placerar rörbart objekt
                 elif [r, c] == player_pos:
                     stdscr.addch(r, c, 'O')  # Placera spelaren
                 else:
                     stdscr.addch(r, c, ' ')  # Ritning av spelplanen
                     
         stdscr.addstr(rows, 0, f"Message: {message}")
         stdscr.refresh()
         

         # Hantera användarinput
         key = stdscr.getch()
         new_pos = player_pos.copy()
         if key == ord('q'):  # Avsluta spelet
             break
         elif key == ord('w'):  # Upp
             new_pos[0] -= 1
         elif key == ord('s'):  # Ner
             new_pos[0] += 1
         elif key == ord('a'):  # Vänster
             new_pos[1] -= 1
         elif key == ord('d'):  # Höger
             new_pos[1] += 1
         # Kontrollera om spelaren försöker gå in i en vägg eller ett objekt
         if not ((new_pos[0] == 0 or new_pos[0] == rows - 1 or 
                 new_pos[1] == 0 or new_pos[1] == cols - 1) and tuple(new_pos) != wall_hole) and \
                new_pos not in block_pos:
            
             player_pos = new_pos
            
         if player_pos == goal_pos:
            message = "you win" #Ändra denna till vad man vill ska hända
            

if __name__ == "__main__": 
	curses.wrapper(main)

###########################################################################