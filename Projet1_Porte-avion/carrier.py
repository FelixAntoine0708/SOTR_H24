"""
Author: Félix-Antoine Guimont & Carl-Dominic Aubin
Date: 15 avril 2024
Description: Simulation d'un porte-avion commande par des touches de clavier
"""

##############IMPORT##############
import multiprocessing.process
import time
import threading
import multiprocessing
import os
import keyboard
from random import randint
import deck
from ctypes import c_bool

##############GLOBAL##############
VALID_COMMANDS = {'l', 'r', 's', '1', '2', '3', '4', 'v', 'q'}
goodKey = ''
catapulte_D_AV = True
catapulte_D_AV2 = True
catapulte_DA_CO = True
catapulte_DA_CO2 = True
planeIndentity = {}

##############FONCTION##############
def getRekt():
    os.system('clear')
    print("\n\nUse the key, you peasant!\n")
    
def printKey():
    print("________________________________________\n")
    print("\t\t*The Keys*\n")
    print("l = lauch a plane \nr = land all plane \ns = display all planes states \n1 = close front catapults for maintenance \n2 = reopen front catapults \n3 = close side catapults for maintenance \n4 = reopen side catapults \nv = display catapults states \nq = dock carrier (end program)")
    print("________________________________________")
    
def dashboard():
    
    global goodKey
    
    enteredKeys = ""
    keys = ""
    
    while deck.CatapultQueue["stop"]: 
        
        if(keyboard.read_key()):
            keys = keyboard.read_key()
            enteredKeys = enteredKeys + keys
        
        if(keys == 'enter'):
            enteredKeys = enteredKeys[:-5]
            if len(enteredKeys) == 1:
                if(enteredKeys in VALID_COMMANDS):
                    goodKey = enteredKeys
                    deck.Deck.listener_plane(deck.Deck, enteredKeys)
                    enteredKeys = ""
                else:
                    enteredKeys = ""
                    getRekt()
                    printKey()
            else:
                enteredKeys = ""
                getRekt()
                printKey()
                
        time.sleep(0.01)

def catapult_available():
        os.system('clear')
        print("________________________________________\n")
        print("Catapultes disponibles :\n")
            
        if(deck.CatapultQueue["catapulte_D_AV"]):
            print("Catapulte avant #1")

        if(deck.CatapultQueue["catapulte_D_AV2"]):
            print("Catapulte avant #2")
            
        if deck.CatapultQueue["catapulte_DA_CO"]: 
            print("Catapulte de côté # 3")

        if deck.CatapultQueue["catapulte_DA_CO2"]: 
            print("Catapulte de côté # 4")
                
        if not deck.CatapultQueue["catapulte_D_AV"] and not deck.CatapultQueue["catapulte_D_AV2"] and not deck.CatapultQueue["catapulte_DA_CO"] and not deck.CatapultQueue["catapulte_DA_CO2"]:
            print("- Aucune")

def identifierAvion(NOavion, key):
    global planeIndentity

    if key == '':
        number = randint(1, 999)
        result = (NOavion * number) %1000
        planeIndentity[NOavion] = result

    if key == 'r':
        planeIndentity.pop(NOavion)

    if key == 's':
        os.system('clear')
        if len(planeIndentity) > 0:
            for x in range(len(planeIndentity)):
                print(f"Plane {x+1}, Indentity {planeIndentity[x+1]}")
        else:
            print("No plane in the air")      
              
def tourControle():    
    t1 = threading.Thread(target=dashboard)
    t1.start()
    t1.join()

def pont():
    t2 = threading.Thread(target=deck.Deck.launch_loop, args=(deck.Deck, ))
    t2.start()


if __name__ == "__main__":
    os.system('clear')
    printKey()
    
    mp1 = multiprocessing.Process(target=tourControle)
    mp2 = multiprocessing.Process(target=pont)
    
    mp1.start()
    mp2.start()
    
    mp1.join()
