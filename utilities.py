import pandas as pd
import numpy as np
import shapely as sp
import geopandas as gpd
class intervalle():
    def __init__(self, a=None, b=None):
        self.a = a
        self.b = b

    def __str__(self):
        if self.a == None:
            return "Intervalle vide"
        else:
            return f"[{self.a},{self.b}]"


class IFT():
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

    def add(self, ift):
        if self.h > ift.h:
            ift1 = self.tr(ift.h)
            return IFT(ift1.a + ift.a, ift1.b + ift.b, ift1.c + ift.c, ift1.d + ift.d, ift.h, self.label)
        else:
            ift1 = self
            ift = ift.tr(self.h)
            return IFT(ift1.a + ift.a, ift1.b + ift.b, ift1.c + ift.c, ift1.d + ift.d, ift.h, self.label)

    # Mult à faire et diviser
    def tr(self, h):
        if h > self.h:
            raise ValueError("H est au dessus de la hauteur de l'intervalle")
        elif h == self.h:
            return self
        else:
            b = h*(self.b-self.a)/self.h+self.a
            c = - h*(self.d - self.c)/self.h +self.d
            return IFT(self.a,b,c,self.d, h,self.label)

class NFT(IFT):
    def __init__(self, a, b, c, h, label):
        IFT.__init__(self, a, b, b, c, h, label)
 # Rajouter les autres types differents ! réimplémenter les mutilications pour intervalles flous purs


class Classe():
    def __init__(self, label, range = intervalle()):
        self.label = label
        self.classes = []
        self.valeurs = []
        self.range = intervalle

    def add(self, ift):
        self.valeurs.append(ift)
        self.classes.append(ift.label)

    def v(self, x):
        appartenance = {}
        for ift in self.valeurs:
            appartenance[ift.label] = ift.v(x)
        return appartenance

    # rajouter une méthode pour plot la classe en fonction de son intervalle

    def possibilite(self, poly):
        resultat = {key.label : 0 for key in self.valeurs}
        for ift in self.valeurs:
            name = ift.label
            shape_IFT = sp.Polygon(list(set([(ift.a,0),(ift.b,ift.h),(ift.c,ift.h),(ift.d,0)])))
            if shape_IFT.intersects(poly):
                shape_IFT = poly.intersection(shape_IFT)
                h = max(shape_IFT.exterior.coords.xy[1])
                resultat[name] = h

        return resultat
    def union(self, resultat):
        minimum, maximum = min([ift.a for ift in self.valeurs if resultat[ift.label]>0]), max([ift.d for ift in self.valeurs if resultat[ift.label]>0])
        poly = sp.Polygon([(minimum,-1),(minimum, 0), (maximum, 0), (maximum, -1) ])
        for ift in self.valeurs:
            degree = resultat[ift.label]
            if degree > 0:
                ift = ift.tr(degree)

                a,b,c,d,h = ift.a,ift.b,ift.c,ift.d,ift.h
                minimum = min(minimum, a)
                maximum = max(maximum, d)
                poly = sp.unary_union([poly,sp.make_valid(sp.Polygon(list(set([(a,0),(b,h),(c,h),(d,0)]))))])

        return poly
    def defuz(self, resultat):
        poly = self.union(resultat)
        return poly.centroid.x

class Table():
    def __init__(self, rules):

        self.rules = pd.read_csv(rules)
        self.label = self.rules.columns.values[0]
        self.lb_classe1 = self.rules.columns.values[1:]
        self.lb_classe2 = list(self.rules[self.label])
        self.rules.set_index(self.label, inplace=True, drop=True)
        self.lb_result = [ i  for i in np.unique(self.rules) if i not in self.lb_classe2]

    def inference(self,val1, val2, tconorme = max, tnorme = min):
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
    a = Table("testcsv.csv")

    age = Classe("age")
    vieux = IFT(50,60,70,80,1,"faible")
    jeune = IFT(2,5,18,25,1,"moyen")
    moyen = IFT(20,25,45, 55, 1, "fort")
    age.add(vieux)
    age.add(jeune)
    age.add(moyen)
    print(age.v(5))
    poly = age.union(age.v(5))

    print(age.defuz(age.v(5)))
    age1 = Classe("age")
    vieux1 = IFT(50, 60, 70, 80, 1, "bas")
    jeune1 = IFT(2, 5, 18, 25, 1, "normal")
    moyen1 = IFT(20, 25, 45, 55, 1, "haut")
    age1.add(vieux1)
    age1.add(jeune1)
    age1.add(moyen1)

    print(a.inference(age.v(53), age1.v(53)))

    a2 = Table_mult(age1, a,a, a)
    print(age1.v(0), a2.inference(age1.v(0),age.v(53),age1.v(53)))
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
