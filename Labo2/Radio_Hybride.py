'''
    Auteur: Felix-Antoine Guimont

    Labo 2 multiproccessing et multithreading
    Partie Hybride

    consommation: 3805013
'''

from multiprocessing import Process, Queue
from threading import Thread as th
from threading import Lock
import keyboard as kb
import pygame 
from time import sleep as s
import tracemalloc

tracemalloc.start()

def app(q):
    global line
    lt = []
    for i in range(0, 100000):
        lt.append(i)

    q.put(tracemalloc.get_traced_memory())

def lyrics(q):
    file = open('lyrics.txt', 'r')
    s(4.7)
    for x in range(278):
        q.put(file.readline())
        s(1.5)

def cligno(q):
    while True:
        if kb.is_pressed('r'):
            for x in range(3):
                q.put("clignotant right")
                s(1)
                
        if kb.is_pressed('l'):
            for x in range(3):
                q.put("clignotant left")
                s(1)

def music():
    pygame.mixer.init()
    try:
        pygame.mixer.music.load('soud of silence.ogg')
    except pygame.error as e:
        print("Error loading audio file:", e)
        return

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def process1():
    t3 = th(target=music)
    t3.start()

def process2(q):
    t1 = th(target=cligno, args=(q,))
    t2 = th(target=lyrics, args=(q,))
    t1.start()
    t2.start()
  
if __name__ == '__main__':
    q = Queue()

    app(q)
    tracemalloc.stop()

    p1 = Process(target=process1, args= ())
    p2 = Process(target=process2, args= (q,))
    p2.start()
    p1.start()
    

    try:
        while True:
            if not q.empty():
                print(q.get())

    except KeyboardInterrupt:
        p1.terminate()  # Terminate the process
        p2.terminate()
        pygame.quit()