# BGS project by La Branche (https://discord.gg/AD7H4jX)
# Developpers : Antoine D., Kernel
# GameMaker file -- classes and functions for the game

# __author__ = "tenukibestmove"

""" this code allows to prepare the algorithm which repairs the groups and 
the interactive goban made with the sdl / pygame"""

import numpy as np
import pygame
import pygame.freetype as fnt
from GameMakerExceptions import *

fnt.init()
pygame.display.init()
pygame.display.set_mode((700,500))

#Police pour le texte (sujette à changement)
main_font = fnt.Font("./wellbutrin.ttf", 18)

#Constantes du module (y en beaucoup)
ALPHABET = "A.B.C.D.E.F.G.H.I.J.K.L.M.N.O.P.Q.R.S.T.U.V.W.X.Y.Z".split('.')
ALPHANUM_DICT = {ALPHABET[i]:i for i in range(len(ALPHABET))}
BLACK_STONE = pygame.image.load("pierre.png").convert_alpha()
WHITE_STONE = pygame.image.load("pierre2.png").convert_alpha()
BLACK_TEXTSURFACE = main_font.render('Noir', (0,0,0))[0]
WHITE_TEXTSURFACE = main_font.render('Blanc', (255,255,255))[0]
PLAYER_TEXTSAFEZONE = main_font.render('Blanc', (0,0,0))[1]
VOID_SURFACE = pygame.Surface((0,0)) #Surface vide (même si ça ne sert pas, je la garde au cas où)
PLAYER_TURN_COORDINATES = (585,50) #Coordonnées graphiques pour l'affichage du tour actuel
TURN_NUMBER_COORDINATES = (520,50) #Coordonnées graphiques pour l'affichage du numéro de tour

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
        self.board = np.zeros((n,n), dtype=int)
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
        Fonction d'ajout d'une pierre sur le goban. Ne l'ajoute pas si l'intersection est déjà occupée. 
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
        graphic_ns = [self._graphic_coordinates(nearby_spaces[i]) for i in range(4)] #Conversion en coordonnées graphiques

        #Table des distances
        dist_table = [np.sqrt(((x-self._graphic_coordinates(nearby_spaces[i])[0])**2)+((y-self._graphic_coordinates(nearby_spaces[i])[1])**2)) for i in range(4)]
        closest_space = nearby_spaces[dist_table.index(min(dist_table))]

        #Test de tolérance du clic et de l'occupation de l'intersection
        if min(dist_table) <= tolerance and not self.board[closest_space[0]][closest_space[1]]: 

            stone_graphic_coordinates = self._graphic_coordinates((closest_space[0], closest_space[1]))
            stone_object = BLACK_STONE if turn == 'b' else WHITE_STONE

            self.board[closest_space[0]][closest_space[1]] = stone_code(turn)

            return (stone_object,stone_graphic_coordinates)

        elif min(dist_table) <= tolerance and self.board[closest_space[0]][closest_space[1]]:
            raise UserStoneOverwriteError

        else:
            raise TooFarFromIntersectionWarning

    def remove_stone(self, goban_image, mat_pos):
        """
        Fonction de retrait d'une pierre sur le goban. 
        Modifie la matrice et renvoie les coordonnées graphiques pour l'affichage.
        ARGUMENTS --
        mat_pos -> (int,int) : représente la position matricielle de la pierre à enlever
        SORTIE --
        (X,Y,Z) -> tuple : tuple de paramètres pour pygame.Surface.blit
        """

        self.board[mat_pos[0]][mat_pos[1]] = 0
        redraw_graphic_coordinates = (self._graphic_coordinates(mat_pos)[0] - 9, self._graphic_coordinates(mat_pos)[1] - 9)
        area_redraw = pygame.Rect(redraw_graphic_coordinates[0],redraw_graphic_coordinates[1],20,20)

        return (goban_image,redraw_graphic_coordinates,area_redraw)

    def get_line(self, i):
        """
        Convertit une ligne du goban en chaîne de caractères.
        ARGUMENTS --
        i -> int : numéro de la ligne
        SORTIE --
        line -> str : chaîne de caractères représentant la ligne
        """

        return "".join([str(x) for x in self.board[i]])

    def get_col(self, j):
        """
        Convertit une colonne du goban en chaîne de caractères.
        ARGUMENTS --
        i -> int : numéro de la colonne
        SORTIE --
        line -> str : chaîne de caractères représentant la colonne
        """

        return "".join([str(self.board[i][j]) for i in range(self.length)])
