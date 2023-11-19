import pandas as pd
import numpy as np
import shapely as sp
import geopandas as gpd

class intervalle():
    """
    Cette classe définit un intervalle net et continu. 
    (car il ne prend en compte que 2 valeurs)
    """


    def __init__(self, a=None, b=None):
        self.a = a
        self.b = b

    def __str__(self):
        if self.a == None:
            return "Intervalle vide"
        else:
            return f"[{self.a},{self.b}]"
    
    def __str__(self) :
        return "[" + str(self.a1) + ", " + str(self.a2) + "]"

    def __add__(self, other) :
        """
        addition de 2 intervalles
        """
        return intervalle(self.a1 + other.a1, self.a2 + other.a2)

    def __neg__(self) :
        """
        donne l'opposé d'un intervalle
        -A = A.__neg__()
        """
        return intervalle(-self.a2, -self.a1)

    def __sub__(self, other) :
        return self + (-other)

    def __mul__(self, other) :
        return intervalle(max([self.a1 * other.b1, self.a1 * other.b2, self.a2 * other.b1, self.a2 * other.b2]), 
                              max([self.b1 * other.a1, self.b1 * other.a2, self.b2 * other.a1, self.b2 * other.a2]))

    def __pow__(self, value) :
        """
        sert uniquement à donner l'inverse d'un intervalle : A^1
        peut s'utiliser ainsi : 
        inverse = A ** -1
        """
        if value != -1 : 
            raise ValueError("Only -1 is supported")
        if self.a1 == 0 or self.a2 == 0 : 
            raise ValueError("Only non-zero intervals are supported")
        if self.a1 <= 0 <= self.a2 : 
            raise ValueError("Only  strictly positive or strictly négative intervals are supported by this operation.")
        return intervalle(1/self.a2, 1/self.a1)

    def __div__(self, other) :
        """
        Divisions de deux intervalles : A / B
        """
        return self * (other**-1)

    def union(self, other) :
        if self.a2 < other.a1 or other.a2 < self.a1 :
            raise ValueError("The intervals must be joined")

        return intervalle(min(self.a1, other.a1), max(self.a2, other.a2))


class IFT():
    """
    Classe qui définit un intervalle flou trapézoidal 
    """
    def __init__(self, a, b, c, d, h, label):

        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.h = h
        self.label = label

    def alpha_coupe(self, alpha):
        if alpha > 0 and alpha <= self.h:
            A1 = ((self.b - self.a) * (alpha / self.h) + self.a)
            A2 = (-(self.d - self.c) * (alpha / self.h) + self.d)
            return intervalle(A1, A2)
        else:
            return intervalle()

    def v(self, x):
        """dans la
        donne la valer d'appartenance d'un point à l'intervalle
        """
        if x < self.a:
            return 0
        if x >= self.a and x <= self.b:
            return self.h * ((x - self.a) / (self.b - self.a))
        if x >= self.b and x <= self.c:
            return self.h

        if x >= self.c and x <= self.d:
            return self.h * ((self.d - x) / (self.d - self.c))
        if x > self.d:
            return 0

    def __str__(self):
        return f" {self.label} : ({self.a}, {self.b}, {self.c}, {self.d})"

    def mul(self, alpha):
        a = alpha * self.a
        b = alpha * self.b
        c = alpha * self.c
        d = alpha * self.d
        return IFT(a,b,c,d,self.h, self.label)

    def __add__(self, ift):
        """
        Ajoute deux IFT . Peut etre appellée par l'addition : 
        ift = ift1 + ift2
        """
        if self.h > ift.h:
            ift1 = self.troncature(ift.h)
            return IFT(ift1.a + ift.a, ift1.b + ift.b, ift1.c + ift.c, ift1.d + ift.d, ift.h, self.label)
        else:
            ift1 = self
            ift = ift.tr(self.h)
            return IFT(ift1.a + ift.a, ift1.b + ift.b, ift1.c + ift.c, ift1.d + ift.d, ift.h, self.label)

    # Mult à faire et diviser
    def troncature(self, h):
        """Fait une troncature de l'ITF en h"""
        if h > self.h:
            raise ValueError("H est au dessus de la hauteur de l'intervalle")
        elif h == self.h:
            return self
        else:
            b = h*(self.b-self.a)/self.h+self.a
            c = - h*(self.d - self.c)/self.h +self.d
            return IFT(self.a,b,c,self.d, h,self.label)

class NFT(IFT):
    """
    classe qui définit un nombre flou triangulaire
    """
    def __init__(self, a, b, c, h, label):
        super().__init__(self, a, b, b, c, h, label)
 # Rajouter les autres types differents ! réimplémenter les mutilications pour intervalles flous purs


class Classe():
    def __init__(self, label, range = intervalle()):
        self.label = label
        self.classes = []
        self.valeurs = []
        self.range = intervalle

    def ajouter(self, ift):
        """
        ajoute un IFT à la classe
        """
        self.valeurs.append(ift)
        self.classes.append(ift.label)

    def v(self, x):
        """
        Renvoie la valeur d'appartenance de x à chaque IFT de la classe dans un dictionnaire.
        """
        appartenances = {}
        for ift in self.valeurs:
            appartenances[ift.label] = ift.v(x)
        return appartenances

    # rajouter une méthode pour plot la classe en fonction de son intervalle

    def possibilite(self, poly):
        """
        dessine les intersections de l'intervalle avec le polygone résultant de la deffuzzification
        """
        gpd.GeoSeries(poly).plot()
        for ift in self.valeurs:
            print(ift)
            print(poly)
            shape_IFT = sp.Polygon(list(set([(ift.a,0),(ift.b,ift.h),(ift.c,ift.h),(ift.d,0)])))
            if shape_IFT.intersects(poly):
                shape_IFT = poly.intersection(shape_IFT)
                print(max(shape_IFT.exterior.coords.xy[1]))
                gpd.GeoSeries(shape_IFT).plot()
        plt.show()

    def defuz(self, resultat):
        """
        defuzzification à partir du dictionnaire d'appartenance au classes.
        retourne un polygone  résultat de l'union des troncatures et du rectangle qui s'étend de la classe activée la plus petite à la classe activée la plus grande
        """
        minimum, maximum = min([ift.a for ift in self.valeurs if resultat[ift.label]>0]), max([ift.d for ift in self.valeurs if resultat[ift.label]>0])
        poly = sp.Polygon([(minimum,-1),(minimum, 0), (maximum, 0), (maximum, -1) ])  # Un rectangle qui s'étend de la classe activée la plus petite à la classe activée la plus grande
        for ift in self.valeurs:
            degree = resultat[ift.label]
            if degree > 0:
                ift = ift.tr(degree)

                minimum = min(minimum, ift.a)
                maximum = max(maximum, ift.d)
                poly = sp.unary_union([poly,sp.make_valid(sp.Polygon(list(set([(ift.a,0),(ift.b,ift.h),(ift.c,ift.h),(ift.d,0)]))))]) 

        return poly # Le polygone est l'ensemble des troncatures de toute les classe activée. Son barycentre est le résulta de la defuzzification
    
    def eval(self, resultat):
        """
        donne la valeur finale déffuzifié à partir du dictionnaire d'appartenance au IFTs
        """
        poly = self.defuz(resultat)
        return self.v(poly.centroid.x)

class Table():
    def __init__(self, rules, label=""):
        """
        crée un système d'inférence flou à partir d'un csv
        """
        self.label = label
        self.rules = pd.read_csv(rules)
        self.lb_classe1 = self.rules.columns.values[1:]
        self.lb_classe2 = list(self.rules["tb"])
        self.rules.set_index('tb', inplace=True, drop=True)
        self.lb_result = [ i  for i in np.unique(self.rules) if i not in self.lb_classe2]

    def inference(self,val1 : dict, val2 : dict, tconorme = max, tnorme = min):

        print(list(val1.keys()))
        if not (list(val1.keys()) == self.lb_classe1).all():
            raise ValueError(f"Classe 1 ne matche pas les valeurs {self.lb_classe1}")
        if not (list(val2.keys()) == self.lb_classe2):
            raise ValueError(f"Classe 2 ne matche pas les valeurs{self.lb_classe2}")
        resultat = {key : 0 for key in self.lb_result}
        for classe1 in [ key for key in val1.keys() if val1[key]!=0]:
            ligne = self.rules[classe1]
            for classe2 in [key for key in val2.keys() if val2[key] != 0]:
                result = ligne.loc[classe2]
                val_result = tnorme(val1[classe1], val2[classe2])
                resultat[result] = tconorme(resultat[result], val_result)

        return resultat




class Table_mult():
    def __init__(self, classe,  *tables ):
        self.lb_classe = classe.classes
        if len(tables)!=len(self.lb_classe):
            raise ValueError(f"Pas assez de tables : {len(tables)} < {len(self.lb_classe)}")
        self.table = {key  : table for key, table in zip(self.lb_classe, tables)}
        self.lb_result = []
        for item in tables:
            self.lb_result+=item.lb_result
        self.lb_result = list(set(self.lb_result))
    def inference(self, val_classe, val1, val2, tconorme = max, tnorme = min):
        resultat = {key : 0 for key in self.lb_result}
        for key in val_classe.keys():

            degre = val_classe[key]

            table = self.table[key]
            result_tmp = table.inference(val1, val2, tconorme, tnorme)
            resultat = {idx : tconorme(resultat[idx], tnorme(result_tmp[idx], degre)) for idx in resultat.keys()}

        return resultat


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    #a = Table("SIFS/SIF 1.csv")

    age = Classe("age")
    vieux = IFT(50,60,70,80,1,"faible")
    jeune = IFT(2,5,18,25,1,"moyen")
    moyen = IFT(20,25,45, 55, 1, "fort")
    age.ajouter(vieux)
    age.ajouter(jeune)
    age.ajouter(moyen)
    print(age.v(5))
    poly = age.defuz(age.v(5))

    age.possibilite(poly)
    age1 = Classe("age")
    vieux1 = IFT(50, 60, 70, 80, 1, "bas")
    jeune1 = IFT(2, 5, 18, 25, 1, "normal")
    moyen1 = IFT(20, 25, 45, 55, 1, "haut")
    age1.ajouter(vieux1)
    age1.ajouter(jeune1)
    age1.ajouter(moyen1)

    #print(a.inference(age.v(53), age1.v(53)))

    #a2 = Table_mult(age1, a,a, a)
    #print(age1.v(0), a2.inference(age1.v(0),age.v(53),age1.v(53)))
    #
    #
    #
    # vieux = NFT(35, 40,45, 0.93, "vieux")
    # vieux2 = NFT(24, 30, 37, 0.4, "jeune")
    # Valeurs = list(range(20, 100))
    #
    # New1 = [vieux.v(i) for i in Valeurs]
    # New2 = [vieux2.v(i) for i in Valeurs]
    # vieux = vieux.add(vieux2)
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
    #
