# BGS project by La Branche (https://discord.gg/AD7H4jX)
# Version 0.1 - April 2021
# Developpers : Antoine D., Kernel

import pygame
import math
import ctypes
from GameMaker import Goban
from pygame.locals import *

pygame.init()
master = Goban(19)

pygame.display.init()
pygame.display.set_caption("BGS version 1.0") #Titre de la fenêtre
pygame.display.set_icon(pygame.image.load("./branche_icon.ico")) #Icône de la fenêtre

# Les deux lignes suivantes servent à définir l'icône sur la barre des tâches
# identique à celle de la fenêtre (uniquement fonctionnel sous Windows) 
try:
    myappid = 'LaBranche.BGS.1.0' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

except Exception:
    pass


#Chargement de la fenêtre et des images
root = pygame.display.set_mode((500,500))
goban = pygame.image.load("goban_teste.png").convert()

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

            click_pos = (event.pos[0], event.pos[1])
            if not master.is_oob((click_pos[0]-9,click_pos[1]-9)):
                root.blit(*master.add_stone(click_pos,turn))
                turn = turn_flip(turn)

            pygame.display.flip()
