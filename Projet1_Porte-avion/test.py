import keyboard
from threading import Thread, Semaphore
from multiprocessing import Process
from time import sleep as s
import progressbar

plane_number = 0
planes_to_launch = []  # Queue to store pending launches
launch_semaphore = Semaphore(1)  # Semaphore for thread safety
stop = True


class Deck:
    def __init__(self):
        pass

    def launch_plane(self, plane_number):
        global planes_to_launch
        launch_semaphore.acquire()

        widgets_landing = [
            f'Plane {plane_number} launching:',
            progressbar.AnimatedMarker(markers='◐◓◑◒'),
            progressbar.PercentageLabelBar(),
            progressbar.Timer()
        ]

        for i in progressbar.progressbar(range(100), widgets=widgets_landing):
            s(0.1)
            if keyboard.is_pressed('l'):
                self.add_plane_to_queue()

        print(f"Plane {plane_number} launched!")

        planes_to_launch = self.erase_from_queue(planes_to_launch, plane_number)

        launch_semaphore.release() 

    def land_plane(self, plane_number):
        if plane_number > 0:    
            for x in range(plane_number):
                widgetsLanding=[
                    f'Plane {plane_number} landing:', 
                    progressbar.AnimatedMarker(markers='◐◓◑◒'),
                    progressbar.PercentageLabelBar(),
                    progressbar.Timer()
                ]
                for i in progressbar.progressbar(range(100),widgets=widgetsLanding):
                    s(0.2)    
                plane_number-=1
                    
        else:
            print("\n\rNo plane are in the air")

    def launch_loop(self):
        while stop: # si le programme est pas arreter
            if planes_to_launch:  # check si la list est pas vide
                self.launch_plane(planes_to_launch[0])   # launch les avions
            s(0.2)
        
        print("retrieving all plane before going")
        self.land_plane(plane_number)    # fait atterir si on arrete le programme

    def add_plane_to_queue():   
        global plane_number
        plane_number += 1   # ajoute 1 avions
        planes_to_launch.append(plane_number)  # ajout d'en la liste 
        print(f"Plane {plane_number} is waiting to launch.")
        s(0.2)

    def erase_from_queue(listing, value):
        new_list = []  # fait une nouvelle list
        for element in listing: 
            if element != value:    # si element est pas lui dans la liste 
                new_list.append(element)    #ajoute dans la liste
        return new_list #retourne la nouvelle liste


def processDeck():
    deck= Deck
    launch_thread = Thread(target=deck.launch_loop, args=()) # initiation du thread de verification des avions
    launch_thread.start()   # debut du thread


# MAIN
if __name__ == '__main__':
    deck= Deck
    process1 = Process(target=processDeck, args=()) # initiation d'un process du Deck
    process1.start()    # debut le process

    while True:

        if keyboard.is_pressed('l'):    # si "l" press
            deck.add_plane_to_queue()    # ajoute 1 avion a la liste de decollage

        elif keyboard.is_pressed('r'):  # si "r" press
            deck.land_plane(plane_number)    # fait atterir tout les avions

        elif keyboard.is_pressed('q'):  # si "q" press
            break   # sort du while

        s(0.2)

    # si "q" a ete press
    process1.terminate()    # supprime le process
    stop = False    # arrete le while 