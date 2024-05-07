"""
Author: Félix-Antoine Guimont & Carl-Dominic Aubin
Date: 15 avril 2024
Description: Simulation d'un porte-avion commande par des touches de clavier
"""
##############IMPORT##############
from threading import Thread, Semaphore
from multiprocessing import Queue, Manager
from time import sleep as s
from tqdm import tqdm
import os
import carrier

##############GLOBAL##############
sema = Semaphore()
PlaneQueue = Queue()
manager = Manager()
CatapultQueue = manager.dict()
CatapultQueue["catapulte_D_AV"] = True
CatapultQueue["catapulte_DA_CO"] = True
CatapultQueue["catapulte_D_AV2"] = True
CatapultQueue["catapulte_DA_CO2"] = True
CatapultQueue["stop"] = True
catapultCounterFront = 2
catapultCounterSide = 2
plane_number = 0
front_plane1 = 0
front_plane2 = 0
side_plane3 = 0
side_plane4 = 0

class Deck():
    def add_plane_to_queue(self): 
        global plane_number
        plane_number += 1   # ajoute 1 avions
        PlaneQueue.put(plane_number)
        carrier.identifierAvion(plane_number, '')
        os.system('clear')
        print(f"\n\rPlane {plane_number} is waiting to launch.")
        s(0.1)

    def launch_plane(self, catapult, plane):
        if catapult == "D_AV1":
            CatapultQueue["catapulte_D_AV"] = False
            plane_launching_front = plane
            for i in tqdm(range(100), colour= "GREEN",desc =f"Plane {plane_launching_front}"):
                s(0.1)

            os.system('clear')
            print(f"\n\rPlane {plane_launching_front} launched!")
            CatapultQueue["catapulte_D_AV"] = True

        if catapult == "D_AV2":
            CatapultQueue["catapulte_D_AV2"] = False
            plane_launching_front2 = plane
            for i in tqdm(range(100), colour= "GREEN",desc =f"Plane {plane_launching_front2}"):
                s(0.1)

            os.system('clear')
            print(f"\n\rPlane {plane_launching_front2} launched!")
            CatapultQueue["catapulte_D_AV2"] = True

        if catapult == "DA_CO3":
            CatapultQueue["catapulte_DA_CO"] = False
            plane_launching_side = plane
            for i in tqdm(range(100), colour= "GREEN",desc =f"Plane {plane_launching_side}"):
                s(0.1)

            os.system('clear')
            print(f"\n\rPlane {plane_launching_side} launched!")
            CatapultQueue["catapulte_DA_CO"] = True

        if catapult == "DA_CO4":
            CatapultQueue["catapulte_DA_CO2"] = False
            plane_launching_side2 = plane
            for i in tqdm(range(100), colour= "GREEN",desc =f"Plane {plane_launching_side2}"):
                s(0.1)
            os.system('clear')
            print(f"\n\rPlane {plane_launching_side2} launched!")
            CatapultQueue["catapulte_DA_CO2"] = True 

    def land_plane(self):
        global plane_number
        if plane_number > 0: 
            if CatapultQueue["catapulte_DA_CO"] or CatapultQueue["catapulte_DA_CO2"]:
                for x in range(plane_number):
                    for i in tqdm(range(100), colour= "RED",desc =f"Plane {plane_number}"):
                        s(0.2) 
                    carrier.identifierAvion(plane_number, 'r')   
                    plane_number-=1
                    
            else:
                os.system('clear')
                print("You can land right now")
                    
        else:
            print("\n\r No plane are in the air")

    def launch_loop(self):
        global front_plane1, front_plane2, side_plane3, side_plane4
        global plane_number

        while CatapultQueue["stop"]:
            with sema:
                if CatapultQueue["catapulte_D_AV"] and not PlaneQueue.empty():
                    front_plane1 = PlaneQueue.get()
                    if front_plane1 != side_plane3 and front_plane1 != front_plane2 and front_plane1 != side_plane4:
                        os.system('clear')
                        print("Front 1 catapult in use")
                        launch_thread_D_AV = Thread(target=self.launch_plane, args=(self, "D_AV1",front_plane1, ))  # Pass "D_AV" as argument
                        launch_thread_D_AV.start()

                if CatapultQueue["catapulte_DA_CO"] and not PlaneQueue.empty():
                    side_plane3 = PlaneQueue.get()
                    if side_plane3 != front_plane1 and side_plane3 != front_plane2 and side_plane3 != side_plane4:
                        os.system('clear')
                        print("\n\rSide catapult in use")
                        launch_thread_DA_CO = Thread(target=self.launch_plane, args=(self, "DA_CO3",side_plane3, ))  # Pass "DA_CO" as argument
                        launch_thread_DA_CO.start()

                if CatapultQueue["catapulte_D_AV2"] and not PlaneQueue.empty():
                    front_plane2 = PlaneQueue.get()
                    if front_plane2 != side_plane3 and front_plane2 != front_plane1 and front_plane2 != side_plane4:
                        os.system('clear')
                        print("Front 2 catapult in use")
                        launch_thread_DA_CO = Thread(target=self.launch_plane, args=(self, "D_AV2",front_plane2, ))  # Pass "DA_CO" as argument
                        launch_thread_DA_CO.start()
                
                if CatapultQueue["catapulte_DA_CO2"] and not PlaneQueue.empty():
                    side_plane4 = PlaneQueue.get()
                    if side_plane4 != side_plane3 and side_plane4 != front_plane1 and side_plane4 != front_plane2:
                        os.system('clear')
                        print("\n\rSide catapult in use")
                        print("\n\rAll catapult is in use")
                        launch_thread_DA_CO = Thread(target=self.launch_plane, args=(self, "DA_CO4",side_plane4, ))  # Pass "DA_CO" as argument
                        launch_thread_DA_CO.start()

            s(0.1)  

    def catapult_maintenance(self, key):
        global catapultCounterFront, catapultCounterSide

        if key == '1': 
            os.system('clear')
            if catapultCounterFront >= 0:
                catapultCounterFront-=1
                if catapultCounterFront == 1:
                    CatapultQueue["catapulte_D_AV"] = False
                    print("Front Catapult #1  is close")

                if catapultCounterFront == 0:
                    CatapultQueue["catapulte_D_AV2"] = False
                    print("Front Catapult #2 is close")
                    print("All Front Catapult is close")

                if catapultCounterFront == -1:
                    catapultCounterFront = 0
                    print("All Front Catapult is close")
                
        if key == '2': 
            os.system('clear')
            if catapultCounterFront <= 2:
                catapultCounterFront+=1
                if catapultCounterFront == 2:
                    CatapultQueue["catapulte_D_AV"] = True
                    print("Front Catapult #1 is Open")
                    print("All Front Catapult is Open")

                if catapultCounterFront == 1:
                    CatapultQueue["catapulte_D_AV2"] = True
                    print("Front Catapult #2 is Open")

                if catapultCounterFront == 3:
                    catapultCounterFront = 2
                    print("All Front Catapult is Open")
                    
        if key == '3': 
            os.system('clear')
            if catapultCounterSide >= 0:
                catapultCounterSide-=1
                if catapultCounterSide == 1:
                    CatapultQueue["catapulte_DA_CO"] = False
                    print("Side Catapult #3 is close")

                if catapultCounterSide == 0:
                    CatapultQueue["catapulte_DA_CO2"] = False
                    print("Side Catapult #4 is close")
                    print("All Side Catapult is close")

                if catapultCounterSide == -1:
                    catapultCounterSide = 0
                    print("All Side Catapult is close")
            
        if key == '4': 
            os.system('clear')
            if catapultCounterSide <= 2:
                catapultCounterSide+=1
                if catapultCounterSide == 2:
                    CatapultQueue["catapulte_DA_CO"] = True
                    print("Side Catapult # 3 is Open")
                    print("All Side Catapult is Open")

                if catapultCounterSide == 1:
                    CatapultQueue["catapulte_DA_CO2"] = True
                    print("Side Catapult is Open") 

                if catapultCounterSide == 3:
                    catapultCounterSide = 2
                    print("All Side Catapult is Open")

    def listener_plane(self, keyPress):
        global plane_number
        
        if keyPress == 'l':
            s(0.2)
            sema.acquire()
            self.add_plane_to_queue(self)
            sema.release()

        if keyPress == 'r':
            self.land_plane(self)

        if keyPress == 'v':
            carrier.catapult_available()

        if keyPress == 's':
            carrier.identifierAvion(plane_number, keyPress)

        if keyPress == '1':
            self.catapult_maintenance(self, keyPress)

        if keyPress == '2':
            self.catapult_maintenance(self, keyPress)

        if keyPress == '3':
            self.catapult_maintenance(self, keyPress)

        if keyPress == '4':
            self.catapult_maintenance(self, keyPress)

        if keyPress == 'q':
            os.system('clear')
            #if CatapultQueue["catapulte_D_AV"]  and CatapultQueue["catapulte_D_AV2"] and CatapultQueue["catapulte_DA_CO"] and CatapultQueue["catapulte_DA_CO2"]:
            if plane_number > 0:
                self.land_plane(self)
                CatapultQueue["stop"]  = False
                print("Mission succesful - The two towers are down")
            else:
                print("The Pentagon want you to finish the mission")  