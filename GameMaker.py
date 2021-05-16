# BGS project by La Branche (https://discord.gg/AD7H4jX)
# Developpers : Antoine D., Kernel
# GameMaker module -- classes and functions for the game

import numpy as np
import pygame
import pygame.freetype as fnt
from GameMakerExceptions import *
from typetools import *

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
        length : taille du goban.
        board : plateau sous forme d'une matrice carrée de taille n.
                ATTENTION (!) : les lignes de la matrice sont les colonnes du goban et inversement !!
        groups : ensemble des groupes sur le plateau.
        states : répertorie les états du goban. Voir la méthode calc_GS pour le détail du calcul.
        GRAPHIC_OFFSET : Coordonnée graphique de la première intersection, constante.
        SQ_LENGTH : Distance entre deux intersections (square length), constante.    
        """

        self.length = n
        self.board = np.zeros((n,n), dtype=int)
        self.groups = set()
        self.states = [0]
        self.GRAPHIC_OFFSET = (35,31)
        self.SQ_LENGTH = 23 

    def is_oob(self,pos):
        """
        Méthode de vérification des bords de la grille (Out Of Bounds).
        ARGUMENTS --
        pos -> (int,int) : représente la position du clic
        SORTIE --
        X -> bool : résultat du test
        """

        offset_x,offset_y = self.GRAPHIC_OFFSET
        n = self.length
        return not(offset_x <= pos[0] <= offset_x+(n-1)*self.SQ_LENGTH and offset_y <= pos[1] <= offset_y+(n-1)*self.SQ_LENGTH)

    def is_boundary(self,mat_pos, neighbors_eject=False):
        """
        Méthode de vérification matricielle du bord de la grille.
        Revoie un indicateur de bord défini comme suit, si mat_pos = (x,y) :
            * coordonnée x (resp. y) valant 0 -> -10 (resp. -1)
            * coordonnée x (resp. y) valant 18 (dépend du goban) -> +10 (resp. +1)
            * L'indicateur vaut 0 auquel on ajoute les valeurs ci-dessus si les coordonnées
              remplissent les conditions.
        Cela donne donc les valeurs suivantes :
            -11 -> coin A19 (0,0)
            -10 -> ligne 19 (0,_)
            -9 -> coin T19 (0,18)
            -1 -> colonne A (_,0)
            0 -> pas sur le bord
            +1 -> colonne T (_,18)
            +9 -> coin A1 (18,0)
            +10 -> ligne 1 (18,_)
            +11 -> coin T1 (18,18)

        Les valeurs de retour de neighbors_ejection dépendent de la liste neighbors définie 
        dans la méthode count_liberties.

        ARGUMENTS --
        mat_pos -> (int,int) : coordonnées matricielles de la case à tester
        neighbors_eject -> bool : ajoute la liste des indices de suppression, voir count_liberties.
        SORTIE --
        | bound_indicator -> int : indicateur de bord
        | neigbors_ejection -> list : liste des indices à supprimer pour count_liberties.
        """

        bound_indicator = 0
        bound_indicator += -10 if mat_pos[0] == 0 else 0
        bound_indicator += 10 if mat_pos[0] == self.length-1 else 0
        bound_indicator += -1 if mat_pos[1] == 0 else 0
        bound_indicator += 1 if mat_pos[1] == self.length-1 else 0

        if not neighbors_eject:
            return bound_indicator
        else:
            if bound_indicator >= 10:
                neighbors_ejection = [0] if bound_indicator == 10 else [0,1]

            elif bound_indicator > 0:
                neighbors_ejection = [1] if bound_indicator == 1 else [0,3]

            elif bound_indicator <= -10:
                neighbors_ejection = [2] if bound_indicator == -10 else [2,3]

            elif bound_indicator < 0:
                neighbors_ejection = [3] if bound_indicator == -1 else [1,2]

            else:
                neighbors_ejection = []

            return neighbors_ejection

    def _matrix_coordinates(self, sp):
        """
        Méthode de conversion : nom de case vers coordonnées matricielles.
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
        Méthode de conversion : coordonnées matricielles vers coordonnées graphiques.
        (pour l'affichage des pierres)
        ARGUMENTS --
        sp -> str : deux ou trois caractères caractérisant une case.
        SORTIE --
        (X, Y) -> (int,int) : coordonnées graphiques de l'intersection.
        """

        offset_x,offset_y = self.GRAPHIC_OFFSET
        i,j = sp

        return (offset_x + i*self.SQ_LENGTH, offset_y + j*self.SQ_LENGTH)

    def _detect_nearest_intersection(self,pos, distance_table=False):
        """
        Détection de l'intersection la plus proche.
        ARGUMENTS --
        pos -> (int,int) : représente la position du clic
        distance_table -> bool : ajoute la liste des distances au retour
        SORTIE --
        closest_space,(dist_table) -> (int,int),(list) : case la plus proche, avec la liste des distances (optionnel) 
        """

        x,y = (pos[0]-9, pos[1]-9)
        offset_x,offset_y = self.GRAPHIC_OFFSET

        # Intersection la plus proche par défaut (Closest Default Intersection) en coord. matricielles
        cdi_x, cdi_y = ((x - offset_x)//self.SQ_LENGTH, (y - offset_y)//self.SQ_LENGTH)
        nearby_spaces = [(cdi_x,cdi_y),(cdi_x+1,cdi_y),(cdi_x,cdi_y+1),(cdi_x+1,cdi_y+1)] #Intersections proches
        graphic_ns = [self._graphic_coordinates(nearby_spaces[i]) for i in range(4)] #Conversion en coordonnées graphiques

        #Table des distances
        dist_table = [np.sqrt(((x-self._graphic_coordinates(nearby_spaces[i])[0])**2)+((y-self._graphic_coordinates(nearby_spaces[i])[1])**2)) for i in range(4)]
        closest_space = nearby_spaces[dist_table.index(min(dist_table))]

        if distance_table:
            return closest_space,dist_table
        else:
            return closest_space

    def calc_GS(self):
        """
        Méthode de calcul de l'état du goban.
        Pour éviter de devoir stocker des matrices entières et de réaliser des comparaisons dessus
        (complexité en O(n**3)), on va plutôt stocker des entiers représentant les états du goban.
        Cet valeur (appelée GS, pour Goban State) est définie par la formule suivante, 
        que l'on doit à notre cher Kaznad <3 : 
        GS = somme(3**(i-1+19*(j-1))*board[i-1,j-1]) pour (i,j) dans [1,19]²
        Ce dernier a fait remarquer qu'une matrice à valeurs dans {0,1,2} pouvait 
        s'écrire comme un 361-uplet représentant un unique nombre en base 3.
        """
       
        return sum([3**(i-1+self.length*(j-1))*(self.board[i-1][j-1]) for i in range(1,self.length+1) for j in range(1,self.length+1)])

    def add_stone(self,pos,turn):
        """
        Méthode d'ajout d'une pierre sur le goban. Ne l'ajoute pas si l'intersection est déjà occupée
        Modifie la matrice, et renvoie le couple (pierre, coordonnées graphiques) pour l'affichage.
        ARGUMENTS --
        pos -> (int,int) : représente la position du clic
        turn -> 'b' ou 'w' : couleur du tour actuel
        SORTIE --
        stone_object -> BLACK_STONE ou WHITE_STONE : image à afficher
        stone_graphic_coordinates -> (int,int) : coordonnées graphiques
        """

        tolerance = 10
        closest_space,dist_table = self._detect_nearest_intersection(pos,distance_table=True)

        #Test de tolérance du clic et de l'occupation de l'intersection
        if min(dist_table) <= tolerance and not self.board[closest_space[1]][closest_space[0]]: 

            stone_graphic_coordinates = self._graphic_coordinates((closest_space[0], closest_space[1]))
            stone_object = BLACK_STONE if turn == 'b' else WHITE_STONE

            self.board[closest_space[1]][closest_space[0]] = stone_code(turn)

            return (stone_object,stone_graphic_coordinates)

        elif min(dist_table) <= tolerance and self.board[closest_space[1]][closest_space[0]]:
            raise UserStoneOverwriteError

        else:
            raise TooFarFromIntersectionWarning

    def remove_stone(self, goban_image, mat_pos):
        """
        Méthode de retrait d'une pierre sur le goban. 
        Modifie la matrice et renvoie les coordonnées graphiques pour l'affichage.
        ARGUMENTS --
        mat_pos -> (int,int) : représente la position matricielle de la pierre à enlever
        SORTIE --
        (X,Y,Z) -> tuple : tuple de paramètres pour pygame.Surface.blit
        """

        self.board[mat_pos[0]][mat_pos[1]] = 0
        redraw_graphic_coordinates = (self._graphic_coordinates(mat_pos)[0], self._graphic_coordinates(mat_pos)[1])
        area_redraw = pygame.Rect(redraw_graphic_coordinates[0],redraw_graphic_coordinates[1],20,20)

        return (goban_image,redraw_graphic_coordinates,area_redraw)

    def count_liberties(self,mat_pos):
        """
        Compte les libertés d'une pierre.
        ARGUMENTS --
        mat_pos -> (int,int) : position matricielle de la pierre
        SORTIE --
        p -> int(0,4) : nombre de libertés
        """

        neighbors = [(mat_pos[0]+1,mat_pos[1]),(mat_pos[0],mat_pos[1]+1),(mat_pos[0]-1,mat_pos[1]),(mat_pos[0],mat_pos[1]-1)]
        neighbors_index_ejection = self.is_boundary(mat_pos,neighbors_eject=True)
        delete_items(neighbors,neighbors_index_ejection)

        return len([v for v in neighbors if self.board[v[0]][v[1]] == 0])

    def get_line(self, i):
        """
        Convertit une colonne du goban en chaîne de caractères.
        ARGUMENTS --
        i -> int : numéro de la ligne
        SORTIE --
        line -> str : chaîne de caractères représentant la ligne
        """

        return "".join([str(x) for x in self.board[i]])

    def get_col(self, j):
        """
        Convertit une ligne du goban en chaîne de caractères.
        ARGUMENTS --
        i -> int : numéro de la colonne
        SORTIE --
        line -> str : chaîne de caractères représentant la colonne
        """

        return "".join([str(self.board[i][j]) for i in range(self.length)])

    def add_group(self,g):
        """
        Ajoute un groupe à l'ensemble des groupes. (oui, c'est tout.)
        (y a qu'une ligne, et ce n'est pas un return, on sait.)

        (pourquoi faire ça ? parce qu'écrire master.add_group(g) 
        c'est mieux, point final.)

        (si vous n'êtes pas satisfaits, sachez que le BRC - Bureau 
        des Réclamations de Code - est actuellement fermé pour 
        cause de pandémie mondiale.)

        ARGUMENTS --
        g -> StoneGroup : le groupe à ajouter.
        SORTIE --
        None
        """

        self.groups.add(g)


    def update_groups(self,pos,turn):
        """
        Mise à jour des groupes
        """
        
        closest_intersect = self._detect_nearest_intersection(pos)

        raise CreateNewStoneGroupSignal(closest_intersect)


class StoneGroup(Goban):
    """Classe modélisant un groupe de pierres."""

    def __init__(self,c,memberlist):
        """
        Constructeur du groupe de pierres.
        ATTRIBUTS --
        color : couleur du groupe.
        members : liste contenant les pierres membres du groupe.
        stoneliberties : dictionnaire reliant chaque pierrre à sa liberté.
        groupliberty : liberté du groupe, déduite des libertés individuelles.
        """

        super().__init__(19) #à modifier quand on offrira des gobans de plusieurs tailles
        self.color = c #'b' ou 'w'
        self.members = memberlist
        self.stoneliberties = {stone:self.count_liberties(stone) for stone in self.members}
        self.groupliberty = sum(self.stoneliberties.values())

    def __repr__(self):
        """Représentation d'un groupe."""
        return "<StoneGroup color = {}, members = {}, GLib = {}>".format(self.color,self.members,self.groupliberty)

    def __add__(self,g):
        """Union de deux groupes de même couleur"""

        return StoneGroup(self.length, self.color, self.members + g.members)

    def __and__(self,g):
        """Intersection ensembliste de deux groupes"""

        return [s for s in self.members for t in g.members if s == t]

    def is_member(self,mat_pos):
        """
        Vérifie si une pierre se trouve dans un groupe.
        On suppose que Goban.board[mat_pos] n'est pas nul.
        ARGUMENTS --
        mat_pos -> (int,int) : coordonnées matricielles de la pierre.
        SORTIE --
        X -> bool : évaluation de "mat_pos in self.members."
        """

        return (mat_pos[0],mat_pos[1]) in self.members

    def add_new_member(self,stone):
        """
        Ajoute une pierre au groupe, si elle n'y appartient pas déjà.
        Modifie les attributs de l'objet.
        ARGUMENTS --
        stone -> (int,int) : coordonnées matricielles de la pierre.
        SORTIE --
        None
        """

        if not self.is_member(stone):
            new_stone_liberty = self.count_liberties(stone)
            self.members.append(stone)
            self.liberties[stone] = new_stone_liberty
            self.groupliberty += new_stone_liberty
        else:
            return None