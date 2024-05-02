"""
Author: Félix-Antoine Guimont & Carl-Dominic Aubin
Date: 15 avril 2024
Description: Simulation d'un porte-avion commande par des touches de clavier
"""

##############IMPORT##############
import time
import threading
import multiprocessing
import sys, select, termios, tty
import keyboard
import random

from plane import Plane, PlaneStates
from ctypes import c_bool

##############GLOBAL##############
VALID_COMMANDS = {'l', 'r', 's', '1', '2', '3', '4', 'v', 'q'}
goodKey = ''
catapulte_D_AV = True
catapulte_DA_CO = True

##############FONCTION##############
def getRekt():
    print("\n\nUse the key, you peasant!\n")
    
def printKey():
    print("________________________________________\n")
    print("\t*The Keys*\n")
    print("l = lauch a plane \nr = land all plane \ns = display all planes states \n1 = close front catapults for maintenance \n2 = reopen front catapults \n3 = close side catapults for maintenance \n4 = reopen side catapults \nv = display catapults states \nq = dock carrier (end program)")
    print("________________________________________")
    
def dashboard():
    
    global goodKey
    
    enteredKeys = ""
    keys = ""
    
    while True :
        
        if(keyboard.read_key()):
            keys = keyboard.read_key()
            enteredKeys = enteredKeys + keys
        
        if(keys == 'enter'):
            enteredKeys = enteredKeys[:-5]
            if len(enteredKeys) == 1:
                if(enteredKeys in VALID_COMMANDS):
                    goodKey = enteredKeys
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
 
def logiqueOperation():
    
    global goodKey
    global catapulte_D_AV
    global catapulte_DA_CO
    
    avion = 1
    
    while 1:
        
        if goodKey == '1': #ferme catapulte avant, (peut seuelemnt décoler)
            catapulte_D_AV = False

        if goodKey == '2': #ouvre catapulte avant, (peut seulement décoler)
            catapulte_D_AV = True

        if goodKey == '3': #ferme catapulte cote, (peut décoler et attérir, si false ne peut pas attérir)
            catapulte_DA_CO = False
            
        if goodKey == '4': #ouvre catapulte cote, (peut décoler et attérir, si false ne peut pas attérir)
            catapulte_DA_CO = True         
            
        if goodKey == 'v': #display catapultes states
            
            print("________________________________________\n")
            print("Catapultes disponibles :")
            
            if(catapulte_DA_CO == True): 
                print("- Catapulte de côté")
            
            if(catapulte_D_AV == True):
                print("- Catapulte avant")
                
            if(catapulte_D_AV == False) & (catapulte_DA_CO == False):
                print("- Aucune")

        if goodKey == 's':
            print("________________________________________\n")
            print("\nAvion numéro : ", avion ,"\tIdentifiant de vol : ", identifierAvion(avion))
            avion += 1
            
        goodKey = ""
        time.sleep(0.01)   
         
        
def tourControle():
    
    global settings
    
    t1 = threading.Thread(target=dashboard)
    t2 = threading.Thread(target=logiqueOperation)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()

#def gererCatapulte():
    
    #global semaphore1
    #global semaphore2
    
    #semaphore1 = multiprocessing.Semaphore(1)
    #semaphore2 = multiprocessing.Semaphore(1)
    
def identifierAvion(NOavion):
    result = (NOavion * 33) % 1000
    return result

if __name__ == "__main__":
    
    printKey()
    
    mp1 = multiprocessing.Process(target=tourControle)
    #mp2 = multiprocessing.Process(target=gererCatapulte, args=semaphore1) #ajouter 2 arg pour la sémaphore
    
    mp1.start()
    #mp2.start()
    
    mp1.join()
    #mp1.join()