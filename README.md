# BGS
A project by La Branche : https://discord.gg/AD7H4jX.

The project is in progress, it is therefore normal that for the moment the
rules are not implemented on the goban.

## Project architecture
- `GobanSdl.py` : main script, managing graphical aspects ; the stone capture is
not yet functional.

- `GameMaker.py` : module providing the necessary for the SDL part and the
creation of rules (in progress)

- `GameMakerExceptions.py` : auxiliary module for `GameMaker`.

- `typetools.py` : when Python do not provide means to do a specific thing (such as removing items from a list, given a index list), we implement functions to do so.

## Documentation conventions

*Note : since only French people are working on this project, it is therefore normal that for the moment, comments and docstrings are written in French. (we will translate them into English when we'll want to.)*

If you want to contribute to the project, it is mandatory to provide documented code in order to collaborate easier. Here are the guidelines :

0. **Add comments.** We don't want to guess ourselves what your code does.

1. Script naming : do it with logic. `RandomScriptName.py` is not valid. Use Camel Case convention for game-related scripts, and small letters for more "general" scripts - that were not designed specifically for this project, such as `typetools.py`.

2. For every new script the header must begin with these lines :
```PYTHON
# BGS project by La Branche (https://discord.gg/AD7H4jX)
# Version 0.2 - <date>
# Developpers : tenukiUser, Kernel, <add your username>
# <insert script name> <type> -- <contents>
```
  - Version line is optional on module and all associated files. (they are frequently updated, so there is no need to track their version number.)
  - `<type>` means either a *main script* (which will be *effectively* run by the user or another script) or a *module* (which contents are used in a main script).
  - `<contents>` is pretty clear : for modules, this can be classes, functions, exceptions, etc. For main scripts, provide a simple description of what it is doing, such as `graphical engine`.


3. One-line functions (known as *lambda* functions) : leave single-line comments above it with the explanation. Example :
```PYTHON
# Fonction de codage des pierres pour Goban.board
# Codage : 1 -> blanc, 2 -> noir (ce sera pratique pour les détections d'atari)
stone_code = lambda s: 1 if s == 'w' else 2
```

4. "Real" functions (with a `def`) : the docstring is immediately placed under the definition line. Structure of the docstring :
  - one (or two) sentence(s) to explain what the function does.
  - complete description providing details if necessary.
  - the list of arguments, beginning with `ARGUMENTS --` and following this model for each one : `x -> <type> : <desc>` where `x` is the name of the parameter, `<type>` its type and `<desc>` the associated description.
  - the output(s) of the function, beginning with `OUTPUT --` and following the same model as above. If your return statement do not contain variable names, then use X,Y,Z, etc.

  Here is an example of a complete docstring :
```PYTHON
def add_stone(self,pos,turn):
        """
        Fonction d'ajout d'une pierre sur le goban. Ne l'ajoute pas si l'intersection est déjà occupée.
        Modifie la matrice et renvoie le couple (pierre, coordonnées graphiques) pour l'affichage.
        ARGUMENTS --
        pos -> (int,int) : représente la position du clic
        turn -> 'b' ou 'w' : couleur du tour actuel
        SORTIE --
        stone_object -> BLACK_STONE ou WHITE_STONE : image à afficher
        stone_graphic_coordinates -> (int,int) : coordonnées graphiques
        """
```

5. Class documentation : we make things simple. Below the definition line with `class`, add only one line to describe the class. For the constructor, please provide a list of attributes after `ATTRIBUTES --` with their description. Each method will be documented following rule 4, except for special methods (a simple sentence is sufficient). Example :
```PYTHON
class Goban():
    """Classe représentant un goban, ainsi que les actions qui y sont liées."""

    def __init__(self, n):
        """
        Constructeur du goban.
        ATTRIBUTS --
        length : taille du goban
        board : plateau sous forme d'une matrice carrée de taille n.
                ATTENTION (!) : les lignes de la matrice sont les colonnes du goban et inversement !!
        groups : ensemble des groupes sur le plateau.
        GRAPHIC_OFFSET : Coordonnée graphique de la première intersection, constante.
        SQ_LENGTH : Distance entre deux intersections (square length), constante.    
        """

        self.length = n
        self.board = np.zeros((n,n), dtype=int)
        self.groups = set()
        self.GRAPHIC_OFFSET = (35,31)
        self.SQ_LENGTH = 23
```
  Side note : use full capitals with underscores for constants.

#### Documentation exceptions

This section registers files that break some of the rules above. If a file needs to be added to this section, please submit a motivated pull request (laziness do not count as an argument.).  The numbers following each file name indicate which rules do not apply.
- `GameMakerExceptions.py` (5) : exceptions names are explicit.
- `typetools.py` (4,5) : if functions of this module still are documented, some sentences to explain their purpose are enough.
