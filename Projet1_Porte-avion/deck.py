from threading import Thread, Semaphore
from multiprocessing import Process, Queue
import keyboard
from time import sleep as s
from tqdm import tqdm
import os

sema = Semaphore()
semaphore = Semaphore(1)
queue = Queue()
plane_number = 0
stop = True
catapulte_DA_CO = True
catapulte_D_AV = True
catapulte_D_AV2 = True
catapulte_DA_CO2 = True
front_plane1 = 0
front_plane2 = 0
side_plane3 = 0
side_plane4 = 0

class Deck:
    def __init__(self, plane_number):
        self.plane_number = plane_number

    def add_plane_to_queue(self): 
        self.plane_number += 1   # ajoute 1 avions
        queue.put(self.plane_number)
        os.system('clear')
        print(f"\n\rPlane {self.plane_number} is waiting to launch.")
        s(0.1)

    def launch_plane(self, catapult, plane):
        global catapulte_D_AV, catapulte_DA_CO, catapulte_D_AV2, catapulte_DA_CO2

        if catapult == "D_AV1":
            catapulte_D_AV = False
            plane_launching_front = plane
            for i in tqdm(range(100), colour= "GREEN",desc =f"Plane {plane_launching_front}"):
                s(0.1)

            sema.acquire()
            os.system('clear')
            print(f"\n\rPlane {plane_launching_front} launched!")
            sema.release()
            catapulte_D_AV = True

        if catapult == "D_AV2":
            catapulte_D_AV2 = False
            plane_launching_front2 = plane
            for i in tqdm(range(100), colour= "GREEN",desc =f"Plane {plane_launching_front2}"):
                s(0.1)

            sema.acquire()
            os.system('clear')
            print(f"\n\rPlane {plane_launching_front2} launched!")
            sema.release()
            catapulte_D_AV2 = True

        if catapult == "DA_CO3":
            catapulte_DA_CO = False
            plane_launching_side = plane
            for i in tqdm(range(100), colour= "GREEN",desc =f"Plane {plane_launching_side}"):
                s(0.1)

            sema.acquire()
            os.system('clear')
            print(f"\n\rPlane {plane_launching_side} launched!")
            sema.release()
            catapulte_DA_CO = True

        if catapult == "DA_CO4":
            catapulte_DA_CO2 = False
            plane_launching_side2 = plane
            for i in tqdm(range(100), colour= "GREEN",desc =f"Plane {plane_launching_side2}"):
                s(0.1)

            sema.acquire()
            os.system('clear')
            print(f"\n\rPlane {plane_launching_side2} launched!")
            sema.release()
            catapulte_DA_CO2 = True  

    def land_plane(self):
        global catapulte_D_AV, catapulte_DA_CO, catapulte_D_AV2, catapulte_DA_CO2
        if self.plane_number > 0: 
            if catapulte_DA_CO and catapulte_DA_CO2 and catapulte_D_AV and catapulte_D_AV2:
                for x in range(self.plane_number):
                    for i in tqdm(range(100), colour= "RED",desc =f"Plane {self.plane_number}"):
                        s(0.2)    
                    self.plane_number-=1
            else:
                os.system('clear')
                print("There are plane Launching")
                    
        else:
            print("\n\r No plane are in the air")

    def launch_loop(self):
        global catapulte_D_AV, catapulte_DA_CO, catapulte_D_AV2, catapulte_DA_CO2
        global front_plane1, front_plane2, side_plane3, side_plane4

        while stop:
            with semaphore:
                if catapulte_D_AV and not queue.empty():
                    front_plane1 = queue.get()
                    if front_plane1 != side_plane3 and front_plane1 != front_plane2 and front_plane1 != side_plane4:
                        os.system('clear')
                        print("Front catapult in use")
                        launch_thread_D_AV = Thread(target=self.launch_plane, args=("D_AV1",front_plane1))  # Pass "D_AV" as argument
                        launch_thread_D_AV.start()

                if catapulte_DA_CO and not queue.empty():
                    side_plane3 = queue.get()
                    if side_plane3 != front_plane1 and side_plane3 != front_plane2 and side_plane3 != side_plane4:
                        os.system('clear')
                        print("\n\rSide catapult in use")
                        launch_thread_DA_CO = Thread(target=self.launch_plane, args=("DA_CO3",side_plane3))  # Pass "DA_CO" as argument
                        launch_thread_DA_CO.start()

                if catapulte_D_AV2 and not queue.empty():
                    front_plane2 = queue.get()
                    if front_plane2 != side_plane3 and front_plane2 != front_plane1 and front_plane2 != side_plane4:
                        os.system('clear')
                        print("Front catapult in use")
                        launch_thread_DA_CO = Thread(target=self.launch_plane, args=("D_AV2",front_plane2))  # Pass "DA_CO" as argument
                        launch_thread_DA_CO.start()
                
                if catapulte_DA_CO2 and not queue.empty():
                    side_plane4 = queue.get()
                    if side_plane4 != side_plane3 and side_plane4 != front_plane1 and side_plane4 != front_plane2:
                        os.system('clear')
                        print("\n\rSide catapult in use")
                        print("\n\rAll catapult is in use")
                        launch_thread_DA_CO = Thread(target=self.launch_plane, args=("DA_CO4",side_plane4))  # Pass "DA_CO" as argument
                        launch_thread_DA_CO.start()

            s(0.1)  

        if self.plane_number != 0:
            if catapulte_D_AV and catapulte_DA_CO and catapulte_D_AV2 and catapulte_DA_CO2:
                print("\n\r Leaving no man behind")
                self.land_plane()
                print("\n\r Sleep Time")
            else:
                pass
        else:
            print("\n\r Sleep Time")

    def catapult_free(self):
        global catapulte_D_AV, catapulte_DA_CO, catapulte_D_AV2, catapulte_DA_CO2
        catapult_valid =0

        if catapulte_D_AV:
            catapult_valid+=1

        if catapulte_DA_CO:
            catapult_valid+=1

        if catapulte_D_AV2:
            catapult_valid+=1

        if catapulte_DA_CO2:
            catapult_valid+=1

        os.system('clear')
        print(f"There is {catapult_valid} available")
            

    def listener_plane(self):
        global stop
        while True:
            if keyboard.is_pressed('l'):
                s(0.2)
                sema.acquire()
                self.add_plane_to_queue()
                sema.release()

            if keyboard.is_pressed('r'):
                self.land_plane()
                
            if keyboard.is_pressed('v'):
                self.catapult_free()

            if keyboard.is_pressed('q'):
                if catapulte_D_AV and catapulte_DA_CO and catapulte_D_AV2 and catapulte_DA_CO2:
                    stop = False
                    break
                else:
                    pass

            s(0.1)

    def processDeck(self):
        launch_thread = Thread(target=self.launch_loop) # initiation du thread de verification des avions
        launch_thread.start()   # debut du thread

        add_plane = Thread(target=self.listener_plane)
        add_plane.start()

if __name__ == "__main__":
    Object1 = Deck(plane_number)
    process1 = Process(target=Object1.processDeck) # initiation d'un process du Deck
    os.system('clear')
    process1.start()    # debut le process
    process1.join()
    process1.terminate()
