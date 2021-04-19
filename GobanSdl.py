# BGS project by La Branche (https://discord.gg/AD7H4jX)
# Version 1.0 - April 2021
# Developpers : Antoine D., Kernel

import pygame
import math
import ctypes
from GameMaker import Goban
from pygame.locals import *

pygame.init()
allReturn = Goban()
coo = allReturn[0]

pygame.display.init()
pygame.display.set_caption("BGS version 1.0") #Titre de la fenêtre
pygame.display.set_icon(pygame.image.load("./branche_icon.ico")) #Icône de la fenêtre

# Les deux lignes suivantes servent à définir l'icône sur la barre des tâches
# identique à celle de la fenêtre
myappid = 'LaBranche.BGS.1.0' 
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


root = pygame.display.set_mode((500,500))
goban = pygame.image.load("goban_teste.png").convert()
pierre = pygame.image.load("pierre.png").convert_alpha()
pierre2 = pygame.image.load("pierre2.png").convert_alpha()

root.blit(goban,(0,0))

pygame.display.flip()
a = True 
turn = "n"

while a:
    for event in pygame.event.get():
        if event.type == QUIT:
            a = False
        if event.type == MOUSEMOTION:
            #print(event.pos)
            pass
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            variant = ()
            
            if event.pos in coo:
                
               
                print(event.pos)
                cooblit = (event.pos[0] - 9, event.pos[1] - 9)
                
                if turn == "n":
                    root.blit(pierre,cooblit)
                    turn = "b"
                elif turn == "b":
                    root.blit(pierre2,cooblit)
                    turn = "n"
                pygame.display.flip()
            else:
                i = 0 
                distanceM = 10
                
                while i != len(coo):
                    p1 = coo[i]
                    p2 = event.pos
                    distance = math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))
                    if distance <= distanceM:
                        print("oui")
                        cooblit = (p1[0] - 9,p1[1] -9)
                        if turn == "n":
                            root.blit(pierre,cooblit)
                            turn = "b"
                        elif turn == "b":
                            root.blit(pierre2,cooblit)
                            turn = "n"
                        
                    pygame.display.flip()
                    i+=1