'''
    Auteur: Felix-Antoine Guimont

    Labo 2 multiproccessing et multithreading
    Partie Concurrence
    
    consommation: 3617820
'''

from threading import Thread as th
from threading import Lock
import keyboard
import pygame as pg
from time import sleep as s
import os
import tracemalloc

tracemalloc.start()

line =''
lock = Lock()

def app():
    global line
    lt = []
    for i in range(0, 100000):
        lt.append(i)

    line = (tracemalloc.get_traced_memory())

def lyrics():
    global line
    file = open('lyrics.txt', 'r')
    s(4.7)     # mettre le son au meme moment que le debut de la chanson
    for x in range(278):
        line = (file.readline())
        s(1.5)

def cligno():
    global line
    while True:
            if keyboard.is_pressed('r'):
                for x in range(3):
                    line = ("clignotant right")
                    s(1)
                    
            elif keyboard.is_pressed('l'):
                for x in range(3):
                    line = ("clignotant left")
                    s(1)

def music():
    global lines

    pg.mixer.init()
    pg.mixer.music.load('soud of silence.ogg')
    pg.mixer.music.play()

    while pg.mixer.music.get_busy():
        pg.time.Clock().tick(10)

    pg.quit()    


if __name__ == '__main__':
    app()
    tracemalloc.stop()

    t1 = th(target=lyrics, args= ())
    t2 = th(target=cligno, args= ())
    t3 = th(target=music, args=()) 

    t2.start()
    t1.start()

    t3.start()

    while KeyboardInterrupt:
        if line != '':
            lock.acquire()
            print(line)
            line = ''
            lock.release()
