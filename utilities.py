import pandas as pd
import numpy as np
import shapely as sp
from matplotlib import pyplot as plt

cat = ["impossible", "tres difficile", "difficile", "tres mauvais", "mauvais", "vraiment pas bon", "pas bon", "pas bonne", "tres bas", "bas", "passable", "tres faible", "faible", "moyen", "bon", "tres bon", "haut", "tres haut", "facile", "tres facile", "excellent"] # Ordre des catégories à afficher
def map_range(x, in_min, in_max, out_min, out_max):
    """
    Permet de mapper une valeur à une autre échelle
    """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class intervalle():
    """
    Cette classe définit un intervalle net et continu. 
    (ne prend en compte que 2 valeurs)
    """

    def __init__(self, a=None, b=None):
        self.a = a
        self.b = b

    def __str__(self):
        if self.a == None:
            return "Intervalle vide"
        else:
            return f"[{self.a},{self.b}]"

    def __add__(self, other):
        """
        addition de 2 intervalles
        """
        return intervalle(self.a + other.a, self.b + other.b)

    def __neg__(self):
        """
        donne l'opposé d'un intervalle
        -A = A.__neg__()
        """
        return intervalle(-self.b, -self.a)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        return intervalle(max([self.a * other.a, self.a * other.b, self.b * other.a, self.b * other.b]),
                          min([self.a * other.a, self.a * other.b, self.b * other.a, self.b * other.b]))

    def __pow__(self, value):
        """
        sert uniquement à donner l'inverse d'un intervalle : A^1
        peut s'utiliser ainsi : 
        inverse = A ** -1
        """
        if value != -1:
            raise ValueError("Only -1 is supported")
        if self.a == 0 or self.b == 0:
            raise ValueError("Only non-zero intervals are supported")
        if self.a <= 0 <= self.b:
            raise ValueError("Only  strictly positive or strictly négative intervals are supported by this operation.")
        return intervalle(1 / self.b, 1 / self.a)

    def __div__(self, other):
        """
        Divisions de deux intervalles : A / B
        """
        return self * (other ** -1)

    def union(self, other):
        if self.b < other.a or other.b < self.a:
            raise ValueError("The intervals must be joined")

        return intervalle(min(self.a, other.a), max(self.b, other.b))


class IFT():
    """
    Classe qui définit un intervalle flou trapézoidal 
    """

    def __init__(self, a, b, c, d, h, label):
        """
        Définition de l'IFT selon la notation de Kaufmann
        """
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.h = h
        self.label = label

    def alpha_coupe(self, alpha):
        # renvoie l'alpha coupe
        if alpha > 0 and alpha <= self.h: # l'alpha coupe n'est pas l'intervalle vide
            A1 = ((self.b - self.a) * (alpha / self.h) + self.a)
            A2 = (-(self.d - self.c) * (alpha / self.h) + self.d)
            return intervalle(A1, A2)
        else:
            return intervalle() # rien dans l'alpha coupe

    def v(self, x):
        """
        donne la valeur d'appartenance d'un point à l'intervalle
        """
        if x == self.b: # x dans noyau
            return self.h
        if x <= self.a: # x pas dans le support
            return 0
        if x > self.a and x <= self.b:
            return self.h * ((x - self.a) / (self.b - self.a))
        if x > self.b and x <= self.c: # x dans le noyau
            return self.h

        if x > self.c and x <= self.d:
            return self.h * ((self.d - x) / (self.d - self.c))
        if x > self.d: # x pas dans support
            return 0

    def __str__(self):
        return f" {self.label} : ({self.a}, {self.b}, {self.c}, {self.d})"

    def __pow__(self, power, modulo=None):
        if power != -1:
            raise ValueError("Les autres valeurs que -1 ne sont pas supportées")
        else:
            if self.a >= 0:
                return IFT(1 / self.d, 1 / self.c, 1 / self.b, 1 / self.a, self.h, self.label)
            else:
                raise ValueError("0 dans l'IFT", self)

    def __truediv__(self, other):
        return self * (other ** (-1))

    def __mul__(self, other):
        """
        cette classe sert à multiplier l'IFT
        """
        if isinstance(other, IFT): # si l'autre élément est lui même un IFT
            ift = other
            if self.h > ift.h:
                ift1 = self.troncature(ift.h)
            else:
                ift1 = self
                ift = ift.troncature(self.h)
            return IFT(ift1.a * ift.a, ift1.b * ift.b, ift1.c * ift.c, ift1.d * ift.d, ift1.h, ift1.label)
        else: # si l'autre élément est un scalaire
            alpha = other
            a = alpha * self.a
            b = alpha * self.b
            c = alpha * self.c
            d = alpha * self.d
            return IFT(a, b, c, d, self.h, self.label)

    def __add__(self, ift):
        """
        Ajoute deux IFT . Peut être appellée par l'addition :
        ift = ift1 + ift2
        le label conservé sera celui du premier IFT (ici ift1)
        """
        if self.h > ift.h:
            ift1 = self.troncature(ift.h)
        else:
            ift1 = self
            ift = ift.troncature(self.h)
        return IFT(ift1.a + ift.a, ift1.b + ift.b, ift1.c + ift.c, ift1.d + ift.d, ift.h, self.label)

    def troncature(self, h):
        """Fait une troncature de l'ITF en h"""
        if h > self.h:
            raise ValueError("H est au dessus de la hauteur de l'intervalle")
        elif h == self.h:
            return self
        else:
            b = h * (self.b - self.a) / self.h + self.a
            c = - h * (self.d - self.c) / self.h + self.d
            return IFT(self.a, b, c, self.d, h, self.label)

    def poly(self):
        """
        Renvoie le polygone de l'IFT, sa représentation géométrique utilisée lors de calcul de min-intersection où max-unions d'IFTs
        """

        points = list({(self.a, 0), (self.b, self.h), (self.c, self.h), (self.d, 0)}) # récupère les différents points associés à l'IFT
        poly = sp.make_valid(sp.Polygon(points)) # le transforme en sp.Polygon (ou sp.MultiPolygon)
        return poly


class NFT(IFT):
    """
    classe qui définit un nombre flou triangulaire
    """

    def __init__(self, a, b, c, h, label):
        super().__init__(a, b, b, c, h, label) # dans la notation de Kaufmann


class Classe_classification():
    """
    Définit une entrée floue où les valeurs d'appartenance à chaque classe sont rentrées par l'utilisateur et non calculer à l'aide de fonctions d'appartenances
    """
    def __init__(self, label, *classes):
        self.label = label
        self.classes = list(classes) # récupère les différentes classes floues associées à la classe

    def v(self, *valeurs):
        return {key: value for key, value in zip(self.classes, valeurs)} # créé le dictionnaire associé, avec chaque classe et son degré d'appartenance

    def __str__(self):
        return f"{self.label} : {self.classes}"


class Classe():
    """
    Définit une classe floue où les valeurs d'appartenances sont calculés grâces aux IFTs
    """
    def __init__(self, label, range=None):
        self.label = label # nom de la classe
        self.classes = []
        self.valeurs = []
        self.range = range #plages de valeurs que prend la classe

    def ajouter(self, *ifts):
        """
        ajoute d'un ou plusieurs IFTs à la classe
        """
        for ift in ifts:
            self.valeurs.append(ift) # on stocke les IFTs
            self.classes.append(ift.label)
            if self.range != None: # on met à jour la plage de valeur
                self.range = intervalle(min(ift.a, self.range.a), max(ift.d, self.range.b))
            else: # on crée la plage de valeur
                self.range = intervalle(ift.a, ift.d)

    def v(self, x):
        """
        Renvoie la valeur d'appartenance de x à chaque IFT de la classe dans un dictionnaire.
        """
        x = min(x, self.range.b) # met x dans la plage de valeurs acceptées de la classe
        x = max(x, self.range.a) # met x dans la plage de valeurs acceptées de la classe
        appartenances = {} # initialise le dictionnaire renvoyé
        for ift in self.valeurs:
            appartenances[ift.label] = ift.v(x) #pour chaque IFTs, associe la valeurs d'appartenance de x
        return appartenances

    def possibilite(self, poly):
        """
       Permet d'évaluer une valeur floue (avec sa forme + calcul du degré de possibilité)
        """
        resultat = {ift.label: 0 for ift in self.valeurs} # initialise le dictionnaire renvoyé
        if isinstance(poly, sp.MultiPolygon): # si le polygone est un multipolygone, constitué de plusieurs polygones
            polys = poly.geoms
        else:
            polys = [poly]
        for poly in polys: # pour chaque polygone
            h_poly = max([coord[1] for coord in poly.exterior.coords]) # calcule la hauteur du polygone
            points_noyau_poly_x = [coordo[0] for coordo in poly.exterior.coords if coordo[1] == h_poly] # calcule le noyau du polygone
            if max(points_noyau_poly_x) < self.range.a: #si tous les points du noyau sont plus petit que l'intervalle de la classe, on les évalue comme étant la valeur la plus petite que la classe accepte
                resultat = self.v(self.range.a)
                resultat = {key: min(valeur, h_poly) for key, valeur in resultat.items()} # fait le max entre la hauteur de la min-intersection (soit la hauteur du polygone, comme valeur est considérée dans le noyau
            elif min(points_noyau_poly_x) > self.range.b: # respectivement, s'ils sont tous plus grand, on les évalue comme étant la valeur la plus que la classe accepte
                resultat = self.v(self.range.b)
                resultat = {key: min(valeur, h_poly) for key, valeur in resultat.items()} #

            for ift in self.valeurs: # pour chaque IFT dans la classe
                shape_IFT = ift.poly() # transforme l'IFT en polygone, objet géométrique
                if isinstance(shape_IFT, sp.MultiPolygon): # si c'est un Multipolygone
                    for shape in shape_IFT.geoms: # pour chaque polygone du multipolygone
                        if shape.intersects(poly): # s'il y a une intersection
                            shape = poly.intersection(shape) # récupère la forme de la min-intersection
                            if isinstance(shape, sp.MultiPolygon): # si c'est un multipolygon
                                for shape1 in shape_IFT.geoms: # pour chacun des polygones
                                    resultat[ift.label] = max(max(shape1.exterior.coords.xy[1]), resultat[ift.label]) # récupère la hauteur de la min-intersection, et si cette dernière est plus grande que la valeur déjà présente, la remplace
                            else:
                                resultat[ift.label] = max(max(shape.exterior.coords.xy[1]), resultat[ift.label]) # récupère la hauteur de la min-intersection, et si cette dernière est plus grande que la valeur déjà présente, la remplace


                elif shape_IFT.intersects(poly): #si intersection
                    shape_IFT = poly.intersection(shape_IFT) # récupère la min-intersection
                    resultat[ift.label] = max(max(shape_IFT.exterior.coords.xy[1]), resultat[ift.label]) # récupère la hauteur de la min-intersection, et si cette dernière est plus grande que la valeur déjà présente, la remplace

            return resultat

    def defuz(self, resultat):
        """
        defuzzification à partir du dictionnaire d'appartenance au classes.
        retourne un polygone  résultat de l'union des troncatures et du rectangle qui s'étend de la classe activée la plus petite à la classe activée la plus grande
        """
        minimum, maximum = min([ift.a for ift in self.valeurs if resultat[ift.label] > 0]), max([ift.d for ift in self.valeurs if resultat[ift.label] > 0])
        poly = sp.Polygon([(minimum, -1), (minimum, 0), (maximum, 0), (maximum, -1)])  # Un rectangle qui s'étend de la classe activée la plus petite à la classe activée la plus grande
        for ift in self.valeurs:
            degree = resultat[ift.label]
            if degree > 0:
                ift = ift.troncature(degree)

                minimum = min(minimum, ift.a)
                maximum = max(maximum, ift.d)
                poly = sp.unary_union([poly, sp.make_valid(sp.Polygon(list({(ift.a, 0), (ift.b, ift.h), (ift.c, ift.h), (ift.d, 0)})))])

        return poly  # Le polygone est l'ensemble des troncatures de toute les classe activée. Son barycentre est le résulta de la defuzzification

    def eval(self, resultat):
        """
        donne la valeur finale déffuzifié à partir du dictionnaire d'appartenance au IFTs
        """
        poly = self.defuz(resultat)
        return poly.centroid.x

    def __str__(self):
        return f"{self.label} : {self.classes}"

    def plot(self, pas=0):
        a = self.range.a
        b = self.range.b
        if pas == 0:
            pas = (b - a) / 1000
        X = np.arange(a, b, pas)

        for ift in self.valeurs:
            y = [ift.v(x) for x in X]
            plt.plot(X, y)

        plt.legend([ift for ift in self.valeurs])
        plt.show()


class Table():
    def __init__(self, rules, meaning=""):
        """
        crée un système d'inférence flou à partir d'un csv, le séparateur est ,
        """
        self.meaning = meaning
        try:
            self.rules = pd.read_csv("./SIFS/" + rules)
        except UnicodeError:
            self.rules = pd.read_csv("./SIFS/" + rules, encoding='latin-1')

        self.label = self.rules.columns.values[0]
        self.lb_classe1 = self.rules.columns.values[1:]
        self.lb_classe2 = list(self.rules[self.label])
        self.rules.set_index(self.label, inplace=True, drop=True)
        self.lb_result = [i for i in np.unique(self.rules)]
        categories = [res for res in cat if res in self.lb_result]
        if len(categories) != len(self.lb_result):
            categories += [res for res in self.lb_result if res not in categories]
        self.lb_result = categories

    def plot_result(self, resultat):
        fig, ax = plt.subplots()
        categories = self.lb_result
        counts = [resultat[categorie] for categorie in self.lb_result]
        colors = ["#DF2800", "#EA3C53", "#f2a134","#FFFF00",  "#f7e379","#bbdb44","#44ce1b", "#00CC00"]
        bar_colors = [colors[int(map_range(i, 0, len(categories)-1, 0, len(colors)-1))] for i, lb in enumerate(categories) ]
        ax.bar(categories, counts, color=bar_colors)

        ax.set_ylabel("Appartenance")
        ax.set_title(self.meaning)

        plt.show()
    def inference(self, val1: dict, val2: dict, tconorme=max, tnorme=min, show=True):
        if not set(list(val1.keys())) == set(self.lb_classe1):
            raise ValueError(f" {val1.keys()} ne matche pas les valeurs {self.lb_classe1}")
        if not set(list(val2.keys())) == set(self.lb_classe2):
            raise ValueError(f"{val2.keys()} ne matche pas les valeurs{self.lb_classe2}")
        resultat = {key: 0 for key in self.lb_result}
        for classe1 in [key for key in val1.keys() if val1[key] != 0]:
            ligne = self.rules[classe1]
            for classe2 in [key for key in val2.keys() if val2[key] != 0]:
                result = ligne.loc[classe2]
                val_result = tnorme(val1[classe1], val2[classe2])
                resultat[result] = tconorme(resultat[result], val_result)
        if show:
            print(f"{self.meaning} : {resultat}")
            self.plot_result(resultat)
        return resultat

    def __str__(self):
        print(self.rules)
        print()
        return f"{self.meaning, self.label} | Classe 1 : {self.lb_classe1}, Classe 2 : {self.lb_classe2}"


class Table_mult():
    def __init__(self, classe, *tables, meaning=""):
        self.meaning = meaning
        self.tables = tables
        self.lb_classe = classe.classes
        if len(tables) != len(self.lb_classe):
            raise ValueError(f"Pas assez de tables : {len(tables)} < {len(self.lb_classe)}")
        self.table = {key: table for key, table in zip(self.lb_classe, tables)}
        self.lb_result = []
        for item in tables:
            self.lb_result += item.lb_result
        self.lb_result = list(dict.fromkeys(self.lb_result))

        categories = [res for res in cat if res in self.lb_result]
        if len(categories) != len(self.lb_result):
            categories += [res for res in self.lb_result if res not in categories]
        self.lb_result = categories

    def plot_result(self, resultat):
        fig, ax = plt.subplots()
        categories = self.lb_result
        counts = [resultat[categorie] for categorie in self.lb_result]
        colors = ["#DF2800", "#EA3C53", "#f2a134","#FFFF00",  "#f7e379","#bbdb44","#44ce1b", "#00FF00"]
        bar_colors = [colors[int(map_range(i, 0, len(categories)-1, 0, len(colors)-1))] for i, lb in enumerate(categories) ]
        ax.bar(categories, counts, color=bar_colors)

        ax.set_ylabel("Appartenance")
        ax.set_title(self.meaning)

        plt.show()

    def inference(self, val_classe, val1, val2, tconorme=max, tnorme=min, show= False):
        resultat = {key: 0 for key in self.lb_result}
        for key in val_classe.keys():
            degre = val_classe[key]

            table = self.table[key]
            result_tmp = table.inference(val1, val2, tconorme, tnorme, show=False)
            for key in [key for key in self.lb_result if key not in result_tmp.keys()]:
                result_tmp[key] = 0
            resultat = {idx: tconorme(resultat[idx], tnorme(result_tmp[idx], degre)) for idx in resultat.keys()}
        if show:
            print(self.meaning, resultat)
            self.plot_result(resultat)
        return resultat

    def __str__(self):
        return f"{self.meaning} | Classe diff : {self.lb_classe}, Classe 2 : {str(self.tables[0])} , Classe 3 : {self.tables[1].meaning, self.tables[0].lb_classe2}"


if __name__ == "__main__":
    pass

    # from matplotlib import pyplot as plt
    #
    #
    # age = Classe("age")
    # vieux = IFT(50,60,70,80,1,"faible")
    # jeune = IFT(2,5,18,25,1,"moyenne")
    # moyen = IFT(20,25,45, 55, 1, "elevee")
    # age.ajouter(vieux)
    # age.ajouter(jeune)
    # age.ajouter(moyen)
    # print(age.v(53))
    # poly = age.defuz(age.v(5))
    #
    # age.possibilite(poly)
    # age1 = Classe("age")
    # vieux1 = IFT(50, 60, 70, 80, 1, "faible")
    # jeune1 = IFT(2, 5, 18, 25, 1, "moyenne")
    # moyen1 = IFT(20, 25, 45, 55, 1, "elevee")
    # age1.ajouter(vieux1)
    # age1.ajouter(jeune1)
    # age1.ajouter(moyen1)
    #
    # print(a.inference(age.v(53), age1.v(53)))
    #
    # a2 = Table_mult(age1, a,a, a)
    # print(age1.v(0), a2.inference(age1.v(0),age.v(53),age1.v(53)))
    #
    #
    #
    # vieux = NFT(35, 40,45, 0.93, "vieux")
    # vieux2 = NFT(24, 30, 37, 0.4, "jeune")
    # Valeurs = list(range(20, 100))
    #
    # New1 = [vieux.v(i) for i in Valeurs]
    # New2 = [vieux2.v(i) for i in Valeurs]
    # vieux = vieux + vieux2
    #
    #
    # New = [vieux.v(i) for i in Valeurs]
    #
    # plt.plot(Valeurs, New)
    # plt.plot(Valeurs, New1)
    # plt.plot(Valeurs, New2)
    # plt.show()
    #
    # print(vieux.alpha_coupe(0.98))
    #
    # vieux = NFT(35, 40, 50, 1, "vieuxNFT")
    # Valeurs = list(range(20, 100))
    #
    # New = [vieux.v(i) for i in Valeurs]
    # plt.plot(Valeurs, New)
    # plt.show()

    #
