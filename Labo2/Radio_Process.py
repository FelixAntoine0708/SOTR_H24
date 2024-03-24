'''
    Auteur: Felix-Antoine Guimont

    Labo 2 multiproccessing et multithreading
    Partie Process
	
    consommation: 3803629
'''

from time import sleep as s
import keyboard
import multiprocessing as mp
import pygame 
import tracemalloc

tracemalloc.start()

def app(q):
    lt = []
    for i in range(0, 100000):
        lt.append(i)
    q.put(tracemalloc.get_traced_memory())


def process3():
    pygame.mixer.init()
    pygame.mixer.music.load('soud of silence.ogg')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()

def process1(q):
	while True:
		if keyboard.is_pressed('r'):
			for x in range(3):
				q.put("clignotant droit")
				s(1)

		if keyboard.is_pressed('l'):
			for x in range(3):
				q.put("clignotant droit")
				s(1)
		
     
def process2(q):
	while True:
		file = open('lyrics.txt', 'r')
		s(4.7)
		for x in range(278):
			q.put(file.readline())
			s(1.5)


if __name__ == '__main__':
    q =  mp.Queue()
    app(q)

    tracemalloc.stop()

    p1 = mp.Process(target=process1, args=(q,))
    p2 = mp.Process(target=process2, args=(q,))
    p3 = mp.Process(target=process3, args=())
	
    p1.start()
    p2.start()
    p3.start()
    
    while True:
        if not q.empty():
        	print(q.get())