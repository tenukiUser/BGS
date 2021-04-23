# BGS project by La Branche (https://discord.gg/AD7H4jX)
# Version 0.1 - April 2021
# Developpers : Antoine D., Kernel

import pygame
import math
import ctypes
from GameMaker import *
from pygame.locals import *

pygame.init()
master = Goban(19)
#coo = allReturn[0]

pygame.display.init()
pygame.display.set_caption("BGS version 1.0") #Titre de la fenêtre
pygame.display.set_icon(pygame.image.load("./branche_icon.ico")) #Icône de la fenêtre

# Les deux lignes suivantes servent à définir l'icône sur la barre des tâches
# identique à celle de la fenêtre (uniquement fonctionnel sous Windows) 
try:
    myappid = 'LaBranche.BGS.1.0' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

except: #Pas besoin de spécifier
    pass


#Chargement de la fenêtre et des images
root = pygame.display.set_mode((500,500))
goban = pygame.image.load("goban_teste.png").convert()
pierre = pygame.image.load("pierre.png").convert_alpha()
pierre2 = pygame.image.load("pierre2.png").convert_alpha()

root.blit(goban,(0,0))
pygame.display.flip()
a = True 
turn = "b"

while a:
    for event in pygame.event.get():
        if event.type == QUIT:
            a = False
        if event.type == MOUSEMOTION:
            #print(event.pos)
            pass
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            variant = ()

            cooblit = (event.pos[0], event.pos[1])
            if not master.is_oob((cooblit[0]-9,cooblit[1]-9)):
                root.blit(*master.add_stone(cooblit,turn))
                turn = turn_flip(turn)

            pygame.display.flip()


            # if event.pos in coo: #ça n'arrive jamais, on peut le virer
                
               
            #     print(event.pos)
            #     cooblit = (event.pos[0] - 9, event.pos[1] - 9)
                
            #     if turn == "n":
            #         root.blit(pierre,cooblit)
            #         turn = "b"
            #     elif turn == "b":
            #         root.blit(pierre2,cooblit)
            #         turn = "n"
            #     pygame.display.flip()

            # else:
            #     i = 0 
            #     distanceM = 10
            #     print(event.pos)

            #     while i != len(coo):
            #         p1 = coo[i]
            #         p2 = event.pos
            #         distance = math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))
            #         if distance <= distanceM:
                        
            #             cooblit = (p1[0] - 9,p1[1] -9)
            #             #print(cooblit)
            #             if turn == "n":
            #                 root.blit(pierre,cooblit)
            #                 turn = "b"
            #             elif turn == "b":
            #                 root.blit(pierre2,cooblit)
            #                 turn = "n"
                        
            #         pygame.display.flip()
            #         i+=1
