import progressbar
import pygame
import keyboard
from threading import Thread
from time import sleep as s
import models

class usine:
    def __init__(self):
        self.valid = {'l', 'd', 'a', 'q'}
        self.gram = 0
        self.model = 0

    def showDetail(self):
        print(f"Granule reserve at: {self.gram}g")
        
    def addGranule(self):
        if self.gram < 150:
            self.gram+=100
            print("You just add 100g")
            if self.gram >= 150:
                print("You are full of Granule")
                self.gram = 150
        else:
            print("You are full of Granule")

    def command(self):
        model = models.SmurfModel(1)
        print(model.name)
        m = 100
        with progressbar.ProgressBar(max_value=m) as bar:
            for i in range(m):
                bar.update(i)
                s(0.01)
        

    def listener(self):
        enteredKeys = ""
        keys = ""
        keysCounter = 0
        while True:
            

            if(keyboard.read_key()):
                keys = keyboard.read_key()
                if keysCounter == 1:
                    if keys != 'enter':
                        keysCounter+=1
                        self.model = int(keys)
                        enteredKeys = enteredKeys + keys
                        keysCounter = 0
                else:
                    enteredKeys = enteredKeys + keys
                    keysCounter+=1
        
                if(keys == 'enter'):
                    if keysCounter == 2: 
                        enteredKeys = enteredKeys[:-6]
                    keysCounter = 0
                    enteredKeys = enteredKeys[:-5]
                    if len(enteredKeys) < 3:
                        if(enteredKeys in self.valid):
                            if enteredKeys == 'a':
                                self.addGranule()
                                enteredKeys = ''

                            if enteredKeys == 'd':
                                self.showDetail()
                                enteredKeys = ''
                            
                            if enteredKeys == 'l':
                                self.command()
                                enteredKeys = ''

                        
                        else:
                            enteredKeys = ''
                            print('use good keys')

                    else:
                        enteredKeys = ''
                        print('use good keys')

                s(0.2)

            
            


    
if __name__ == '__main__':
    fab = usine()

    t1 = Thread(target=fab.listener)
    t1.start()


