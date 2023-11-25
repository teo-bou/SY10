from flou_import import *
from Classes import *
from Rules import *
import math
class Carte():
    def __init__(self, carte, l = 500, L = 500):
        self.carte = self.lire_carte(carte)
        self.alt_min = 0
        self.alt_max = difference_altitude.range.b
        self.l = l
        self.L = L
        self.x_max = difference_distance.range.b / math.sqrt(2)
        self.y_max = difference_distance.range.b / math.sqrt(2)


    def __str__(self):
        return f"Carte allant de x=[0;{self.x_max}], y = [0; {self.y_max}], alt = [{self.alt_min}; {self.alt_max}]"
    def lire_carte(self, carte):

        carte_matrice = []# Fonction open-cv à implémenter pour toi, Ellen

        return carte_matrice


    def distance(self, a, b):
        dist = math.dist((a.x, a.y), (b.x, b.y))
        dist = map_range(dist, 0, math.sqrt((self.l)**2 + (self.L)**2), 0, difference_distance.range.b)
        print(dist)
        return dist

    def alt(self, objet=None, x=None, y=None):
        if objet == None and (x == None or y == None):
            raise ValueError("Entrez des valeurs pour le point")
        elif (x == None or y == None):
            x, y = objet.x, objet.y
        x,y = int(map_range(x, 0, self.x_max, 0, self.l)), int(map_range(y, 0, self.y_max, 0, self.L))
        print(x,y)
        alt = 0 #mettre la fonction open-cv qui calcule avec x et y l'altitude
        map_range(alt, 0, 255, self.alt_min, self.alt_max)
        return alt
    def alt_cum(self):
        pass

    def dist_alt(self, a, b):
        return math.dist(self.alt(a), self.alt(b))
class Village():
    def __init__(self, x, y, nb_habitants, ressenti, infrastructure):
        self.x = x
        self.y = y
        self.nb_habitants = nb_habitants
        self.ressenti = ressenti
        self.infrastructure = infrastructure
        self.besoin = self.eval_besoin()
    def eval_besoin_infra(self):
        infrastructure_dico_fixe = {"hopital":NFT(1625, 2500, 3000, 1, "hopital"), "gouvernement": IFT(325, 500, 1000, 1300, 1, "gouvernement")}
        infrastructure_dico_variable = {"hopital": NFT(325, 500, 750, 1, "hopital"), "ecole": NFT(6.5,10, 15, 1, "ecole")}
        infrastructure_besoin = NFT(0,0,0,1,"besoin")
        for key, value in self.infrastructure.items():
            if key in infrastructure_dico_fixe:
                infrastructure_besoin = infrastructure_besoin + infrastructure_dico_fixe[key]*value
            if key in infrastructure_dico_variable:
                infrastructure_besoin = infrastructure_besoin + (infrastructure_dico_variable[key]*self.nb_habitants/4)*value
        return infrastructure_besoin

    def eval_besoin(self):
        self.besoin = self.nb_habitants * 30
        self.besoin_infra = self.eval_besoin_infra()
        resultat = (self.besoin + self.besoin_infra)
        resultat.label = "besoin"
        return resultat



    def __str__(self):
        return f" nb hab ≈ {(self.nb_habitants.b + self.nb_habitants.c)/2} | {self.ressenti} {self.infrastructure}| besoin : {self.besoin} "



class Source():
    def __init__(self, x, y, couleur, debit, odeur):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.debit = debit
        self.odeur = odeur


def CAF2(village, source):
    besoin = village.besoin
    debit = source.debit
    ift = debit*86400*0.6/besoin # on calcule 0.4 de perte
    ift.label = "prop debit/besoin"
    return prop_debit_besoin.possibilite(ift.poly())


def calculer_score(village, source):
    proportion_debit_besoin = CAF2(village, source)
    qualite_eau = SIF5.inference(source.couleur, source.odeur)
    score_eau = SIF7.inference(proportion_debit_besoin, qualite_eau)


def prop_sources_besoins(villages, sources):
    debit = sum([source.debit for source in sources])
    besoin = sum([village.besoin for village in villages])
    ift = debit * 86400 * 0.6 / besoin  # on calcule 0.4 de perte
    ift.label = "prop debit/besoin total"
    return prop_debit_besoin.possibilite(ift.poly())

