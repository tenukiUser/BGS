# BGS project by La Branche (https://discord.gg/AD7H4jX)
# Version 0.2 - April 2021
# Developpers : Antoine D., Kernel
# GobanSDL main script -- graphical engine

import pygame
import pygame.freetype as fnt
import math
from GameMaker import *
from pygame.locals import *

pygame.init()
master = Goban(19)

#Initialisation des sous-modules de pygame
pygame.display.init()
fnt.init()

#Réglages de la fenêtre
pygame.display.set_caption("BGS version 0.2") #Titre de la fenêtre
pygame.display.set_icon(pygame.image.load("./branche_icon.ico")) #Icône de la fenêtre

#Police pour le texte (sujette à changement)
main_font = fnt.Font("./wellbutrin.ttf", 18)

#Chargement de la fenêtre et des images
root = pygame.display.set_mode((700,500))
goban = pygame.image.load("goban_teste.png").convert()
background_goban = pygame.image.load("background_goban.png").convert()

root.blit(goban,(0,0))

#Le texte des tours
current_turn_textsurface,safe_current_turn_text_zone = main_font.render('Tour actuel :', (0,0,0))
root.blit(current_turn_textsurface,(520,20))
root.blit(BLACK_TEXTSURFACE,PLAYER_TURN_COORDINATES)
root.blit(main_font.render('001 -',(0,0,0))[0],(520,50))

pygame.display.flip()
exit = False
turn = "b"
turn_number = 1


while not exit:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit = True
        if event.type == MOUSEMOTION:
            #print(event.pos)
            pass
        if event.type == MOUSEBUTTONDOWN and event.button == 1:

            click_pos = (event.pos[0], event.pos[1])

            if not master.is_oob((click_pos[0]-9,click_pos[1]-9)):

                try:
                    root.blit(*master.add_stone(click_pos,turn))

                except UserStoneOverwriteError:
                    pass

                except TooFarFromIntersectionWarning:
                    pass

                else:

                    try:
                        #Mise à jour des groupes
                        master.update_groups(click_pos,turn)

                    except CreateNewStoneGroupSignal as sig:
                        master.add_group(StoneGroup(turn,sig.init_member))

                    print(master.groups)
                    #Changement du numéro de tour
                    turn_number += 1
                    turn_number_string = str(turn_number).zfill(3)
                    turn_number_color = (0,0,0) if turn == 'w' else (255,255,255)

                    #Préparation des objets Surface pour le tour suivant
                    next_player_turn_text = BLACK_TEXTSURFACE if turn == 'w' else WHITE_TEXTSURFACE
                    next_turn_number_text, next_turn_safezone = main_font.render('{} -'.format(turn_number_string),turn_number_color)
                    next_turn_safezone.width += 5 #Pour éviter des petits soucis avec des tirets trop loin (à ajuster si nécessaire)

                    #Exécution du dessin
                    root.blit(background_goban,TURN_NUMBER_COORDINATES,next_turn_safezone)
                    root.blit(next_turn_number_text,TURN_NUMBER_COORDINATES)
                    root.blit(background_goban,PLAYER_TURN_COORDINATES,PLAYER_TEXTSAFEZONE)
                    root.blit(next_player_turn_text,PLAYER_TURN_COORDINATES)


                    turn = turn_flip(turn)

        pygame.display.flip()
