# BGS project by La Branche (https://discord.gg/AD7H4jX)
# Developpers : Antoine D., Kernel
# GameMaker file -- classes and functions

# __author__ = "tenukibestmove"

""" this code allows to prepare the algorithm which repairs the groups and 
the interactive goban made with the sdl / pygame"""

import numpy as np
import pygame

pygame.display.init()
pygame.display.set_mode((500,500))

ALPHABET = "A.B.C.D.E.F.G.H.I.J.K.L.M.N.O.P.Q.R.S.T.U.V.W.X.Y.Z".split('.')
ALPHANUM_DICT = {ALPHABET[i]:i for i in range(len(ALPHABET))}
BLACK_STONE = pygame.image.load("pierre.png").convert_alpha()
WHITE_STONE = pygame.image.load("pierre2.png").convert_alpha()
VOID_SURFACE = pygame.Surface((0,0)) #Surface vide

# Fonction de codage des pierres pour Goban.board
# Codage : 1 -> blanc, 2 -> noir (ce sera pratique pour les détections d'atari)
stone_code = lambda s: 1 if s == 'w' else 2

# Fonction de changement de tour
turn_flip = lambda t: 'b' if t == 'w' else 'w'

class Goban():
    """Classe représentant un goban, ainsi que les actions qui y sont liées."""

    def __init__(self, n):
        """
        Constructeur du goban.
    
        ATTRIBUTS --
        length : taille du goban
        board : plateau sous forme d'une matrice carrée de taille n.
        GRAPHIC_OFFSET : Coordonnée graphique de la première intersection, constante.
        SQ_LENGTH : Distance entre deux intersections (square length), constante.    
        """

        self.length = n
        self.board = np.zeros((n,n))
        self.GRAPHIC_OFFSET = (35,31)
        self.SQ_LENGTH = 23 

    def is_oob(self,pos):
        """
        Fonction de vérification des bords de la grille (Out Of Bounds).
        ARGUMENTS --
        pos -> (int,int) : représente la position du clic
        SORTIE --
        X -> bool : résultat du test

        """
        offset_x,offset_y = self.GRAPHIC_OFFSET
        n = self.length
        return not(offset_x <= pos[0] <= offset_x+(n-1)*self.SQ_LENGTH and offset_y <= pos[1] <= offset_y+(n-1)*self.SQ_LENGTH)

    def _matrix_coordinates(self, sp):
        """
        Fonction de conversion : nom de case vers coordonnées matricielles.
        ARGUMENTS --
        sp -> str : deux ou trois caractères caractérisant une case. 
        SORTIE --
        (mat_x, mat_y) : coordonnées matricielles de l'intersection.
        """
        column = sp[0]
        line = int(sp[1:])

        return (ALPHANUM_DICT[column],line-1)

    def _graphic_coordinates(self,sp):
        """
        Fonction de conversion : coordonnées matricielles vers coordonnées graphiques.
        (pour l'affichage des pierres)
        ARGUMENTS --
        sp -> str : deux ou trois caractères caractérisant une case.
        SORTIE --
        (graphic_x, graphic_y) : coordonnées graphiques de l'intersection.
        """
        offset_x,offset_y = self.GRAPHIC_OFFSET
        i,j = sp

        return (offset_x + i*self.SQ_LENGTH, offset_y + j*self.SQ_LENGTH)

    def add_stone(self,pos,turn):
        """
        Fonction d'ajout d'une pierre sur le goban. 
        Modifie la matrice et renvoie le couple (pierre, coordonnées graphiques) pour l'affichage.
        ARGUMENTS --
        pos -> (int,int) : représente la position du clic
        turn -> 'b' ou 'w' : couleur du tour actuel
        SORTIE --
        stone_object -> BLACK_STONE ou WHITE_STONE : image à afficher
        stone_graphic_coordinates : coordonnées graphiques
        """

        tolerance = 10
        x,y = (pos[0]-9, pos[1]-9)
        offset_x,offset_y = self.GRAPHIC_OFFSET

        # Intersection la plus proche par défaut (Closest Default Intersection) en coord. matricielles
        cdi_x, cdi_y = ((x - offset_x)//self.SQ_LENGTH, (y - offset_y)//self.SQ_LENGTH)
        nearby_spaces = [(cdi_x,cdi_y),(cdi_x+1,cdi_y),(cdi_x,cdi_y+1),(cdi_x+1,cdi_y+1)] #Intersections proches
        graphic_ns = [self.__graphic_coordinates(nearby_spaces[i]) for i in range(4)] #Conversion en coordonnées graphiques

        #Table des distances
        dist_table = [np.sqrt(((x-self.__graphic_coordinates(nearby_spaces[i])[0])**2)+((y-self.__graphic_coordinates(nearby_spaces[i])[1])**2)) for i in range(4)]

        if min(dist_table) <= tolerance:

            closest_space = nearby_spaces[dist_table.index(min(dist_table))]
            stone_graphic_coordinates = self.__graphic_coordinates((closest_space[0], closest_space[1]))
            stone_object = BLACK_STONE if turn == 'b' else WHITE_STONE

            self.board[closest_space[0]][closest_space[1]] = stone_code(turn)

            return (stone_object,stone_graphic_coordinates)

        else:
            return (VOID_SURFACE,(0,0))

    def remove_stone(self, goban_image, mat_pos):
        """
        Fonction de retrait d'une pierre sur le goban. 
        Modifie la matrice et renvoie les coordonnées graphiques pour l'affichage.
        ARGUMENTS --
        mat_pos -> (int,int) : représente la position matricielle de la pierre à enlever
        SORTIE --
        (goban_image,redraw_graphic_coordinates,area_redraw) : tuple de paramètres pour pygame.Surface.blit
        """

        self.board[mat_pos[0]][mat_pos[1]] = 0
        redraw_graphic_coordinates = (self.__graphic_coordinates(mat_pos)[0] - 9, self.__graphic_coordinates(mat_pos)[1] - 9)
        area_redraw = pygame.Rect(redraw_graphic_coordinates[0],redraw_graphic_coordinates[1],20,20)

        return (goban_image,redraw_graphic_coordinates,area_redraw)
        
