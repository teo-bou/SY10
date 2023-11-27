from flou_import import *
from Classes import *
from Rules import *
import math
import cv2
def line(x0, y0, x1, y1):
    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    switched = False
    if x0 > x1:
        switched = True
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    if y0 < y1:
        ystep = 1
    else:
        ystep = -1

    deltax = x1 - x0
    deltay = abs(y1 - y0)
    error = -deltax / 2
    y = y0

    line = []
    for x in range(x0, x1 + 1):
        if steep:
            line.append((y,x))
        else:
            line.append((x,y))

        error = error + deltay
        if error > 0:
            y = y + ystep
            error = error - deltax
    if switched:
        line.reverse()
    return line
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
        cv2.imshow('Carte', self.carte)
        cv2.waitKey(0)
        return f"Carte allant de x=[0;{self.x_max}], y = [0; {self.y_max}], alt = [{self.alt_min}; {self.alt_max}]"
    def lire_carte(self, carte):
        image_elevation = cv2.imread("./cartes/"+carte)
        image_gray = cv2.cvtColor(image_elevation, cv2.COLOR_BGR2GRAY)
        self.l, self.L = image_gray.shape[0], image_gray.shape[1]
        return image_gray


    def distance(self, a, b):
        if isinstance(a, tuple):
            x1, y1 = a
        else:
            x1, y1 = a.x, a.y
        if isinstance(b, tuple):
            x2, y2 = b
        else:
            x2, y2 = b.x, b.y
        dist = math.dist((x1, y1), (x2, y2))
        dist = map_range(dist, 0, math.sqrt((self.l)**2 + (self.L)**2), 0, difference_distance.range.b)
        return dist
    def line_alt(self, obj1, obj2, pas = 1):
        if isinstance(obj1, tuple):
            x1,y1 = obj1
        else:
            x1,y1 = obj1.x,obj1.y
        if isinstance(obj2, tuple):
            x2,y2 = obj2
        else:
            x2,y2 = obj2.x,obj2.y


        ligne = line(x1, y1, x2, y2)
        ligne = [self.alt(ligne[i]) for i in range(0,len(ligne), pas)]
        print(ligne)
        plt.plot(list(range(len(ligne))),ligne)
        plt.show()
    def alt(self, objet):
        if isinstance(objet, tuple):
            x,y = objet
        else:
            x,y = objet.x,objet.y
        x,y = int(map_range(x, 0, self.x_max, 0, self.l)), int(map_range(y, 0, self.y_max, 0, self.L))
        alt = self.carte[x][y]
        map_range(alt, 0, 255, self.alt_min, self.alt_max)
        return alt
    def alt_cum(self, a, b):
        ligne = line(a.x, a.y, b.x, b.y)
        alt_cum = sum([math.dist(self.alt(ligne[i-1]), self.alt(ligne[i])) for i in range(1, len(ligne)) ])
        return alt_cum

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

def altitude_cumulee_totale(carte, villages, sources):
    altitude_cumul = 0
    for village in villages:
        for source in sources:
            altitude_cumul+=carte.alt_cum(village, source)
    return altitude_cumul