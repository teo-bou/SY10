from Rules import *
import math
import cv2


class Point():
    """
    Convertit un Tuple en un Point ayant un x et un y
    """
    def __init__(self, point):
        self.x = point[0]
        self.y = point[1]
    def __str__(self):
        return f"({self.x}, {self.y})"
def line(x0, y0, x1, y1):
    """Récupère toutes les coordonnées des pixels sur une ligne entre deux points"""
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
    """"
    Objet de type carte
    """
    def __init__(self, carte, accessibilite =None, type_terrain = None, resize_x = 200, resize_y = 200):
        self.l = 400 # largeur et longueur  la carte
        self.L = 400
        self.resize_x = resize_x # taille de la carte redimensionnée
        self.resize_y = resize_y
        self.carte_color = None
        self.carte = None
        self.lire_carte(carte) # instancie et lit les cartes (une en couleur, une en noir et blanc)
        self.carte_resized = cv2.resize(self.carte, (self.resize_x, self.resize_y)) # carte redimensionnée aux dimensions données
        self.alt_min = 0 # altitude varie entre 0 et le max spécifié dans l'entrée floue difference altitude
        self.alt_max = difference_altitude.range.b
        self.x_max = difference_distance.range.b / math.sqrt(2) # comme x_max**2 + ymax**2 = difference_distance_max**2, on en déduit x_max et y_max étant donné que la carte est carrée et toutes les valuers positives
        self.y_max = difference_distance.range.b / math.sqrt(2)
        self.accessibilite = accessibilite # Stocke la valeur d'accéssibilité du terrain
        self.type_terrain = type_terrain # Stocke l'escarpement du terrain


    def __str__(self):
        """
        Affiche la carte
        """
        plt.imshow(self.carte_color)
        plt.show()
        return f"Carte allant de x=[0;{self.x_max}], y = [0; {self.y_max}], alt = [{self.alt_min}; {self.alt_max}]"
    def lire_carte(self, carte):
        """
        Récupère l'image associée et update les cartes
        """
        image_elevation = cv2.imread("./cartes/"+carte)
        self.carte_color = image_elevation
        image_gray = cv2.cvtColor(image_elevation, cv2.COLOR_BGR2GRAY)
        self.carte = np.array(image_gray,  dtype=np.float64)
        self.L, self.l = image_gray.shape[0], image_gray.shape[1]




    def distance(self, a, b):
        """
        Renvoie la distance entre deux points
        """
        if isinstance(a, tuple):
            x1, y1 = a
        else:
            x1, y1 = a.x, a.y
        if isinstance(b, tuple):
            x2, y2 = b
        else:
            x2, y2 = b.x, b.y
        dist = math.dist((x1, y1), (x2, y2))
        dist = map_range(dist, 0, math.sqrt((self.l)**2 + (self.L)**2), 0, difference_distance.range.b) # Remappe la distance sur la carte en pixel à sa valeur réelle
        return dist
    def line_alt(self, obj1, obj2, pas = 1):
        """
        Calcul et affiche l'altitude sur tous les points d'une ligne
        """
        if isinstance(obj1, tuple):
            x1,y1 = obj1
        else:
            x1,y1 = obj1.x,obj1.y
        if isinstance(obj2, tuple):
            x2,y2 = obj2
        else:
            x2,y2 = obj2.x,obj2.y

        x1, y1, x2, y2 = int(map_range(x1, 0, self.x_max, 0, self.l)), int(map_range(y1, 0, self.y_max, 0, self.L)), int(map_range(x2, 0, self.x_max, 0, self.l)), int(map_range(y2, 0, self.y_max, 0, self.L)) # Remappe les valeurs à la bonne échelle
        ligne = line(x1, y1, x2, y2) # récupere la ligne
        ligne = [self.alt(ligne[i]) for i in range(0,len(ligne), pas)] # calcule l'altitude
        plt.plot(list(range(len(ligne))),ligne) # plot sur un graphique l'altitude
        plt.show()
        carte = cv2.line(self.carte_color.copy(), (x1, y1), (x2, y2), (255, 0, 0), 2) # trace une ligne sur la carte aux points traités
        plt.imshow(carte)
        plt.show()

    def alt(self, objet, res=False):
        """
        Calcule l'altitude d'un point. Cela est fait en regardant la valeur de gris sur la carte au poit associé
        """
        if isinstance(objet, tuple):
            x,y = objet
        else:
            x,y = objet.x,objet.y
        if res:
            return self.carte_resized[y][x] # Si la carte plus petite est utilisée
        alt = self.carte[y][x]
        return alt
    def alt_cum(self, a, b):
        """
        Récupère l'altitude cumulée sur une ligne entre deux point (à chaque fois on additionne la différence d'altitude absolue entre deux points
        """
        ligne = line(a.x, a.y, b.x, b.y) # récupère les coordonnées des points sur la ligne
        alt_cum = sum([abs(self.alt(ligne[i-1])- self.alt(ligne[i])) for i in range(1, len(ligne)) ]) #Fait la somme des altitudes cumulées
        return alt_cum

    def dist_alt(self, a, b):
        """
        Retourne la différence d'altitude absolue entre deux points
        """
        return abs(self.alt(a) -  self.alt(b))


class Village():
    """
    Objet de type village
    """
    def __init__(self, carte, x, y, nb_habitants, ressenti, infrastructure, lb=""):
        self.lb = lb # nom du village
        self.carte = carte # carte associée
        x, y = int(map_range(x, 0, carte.x_max, 0, carte.l)), int(map_range(y, 0, carte.y_max, 0, carte.L)) # coordonnées du villages mappées à la carte
        self.x = x
        self.y = y
        self.nb_habitants = nb_habitants
        self.ressenti = ressenti
        self.infrastructure = infrastructure # infrastructures que le village a, nécessitants des besoins plus importants
        self.besoin = self.eval_besoin() # Calcul le besoin en eau par jour du village

    def eval_besoin_infra(self):
        """
        Évalue le besoin en haut hebdomadaire du village
        """
        infrastructure_dico_fixe = {"hopital":NFT(1625, 2500, 3000, 1, "hopital"), "gouvernement": IFT(325, 500, 1000, 1300, 1, "gouvernement")} # infrastructures au besoins fixes peu importe le nombre d'habitants (valeurs tirées du Handbook)
        infrastructure_dico_variable = {"hopital": NFT(325, 500, 750, 1, "hopital"), "ecole": NFT(6.5,10, 15, 1, "ecole")} # infrastructures au besoin variant selon le nombre d'habitan,t du village
        infrastructure_besoin = IFT(0,0, 0,0,1,"besoin")  # initialisation du besoin vide
        for key, value in self.infrastructure.items(): # pour chaque infrastructure du village :
            if key in infrastructure_dico_fixe: # si le besoin est fixe, on regarde ce dernier, on le multiplie par le nombre d'instances de l'infrastrucure et on l'ajoute au besoin
                infrastructure_besoin = infrastructure_besoin + infrastructure_dico_fixe[key]*value
            if key in infrastructure_dico_variable: # s'il est variable, on ajoute le besoin variable correspondant multiplié par un quart du nombre d'habitant
                infrastructure_besoin = infrastructure_besoin + (infrastructure_dico_variable[key]*self.nb_habitants/4)
        return infrastructure_besoin

    def eval_besoin(self):
        """
        évalue le besoin en eau hebdomadaire du village
        """
        self.besoin = self.nb_habitants * 30 # Chaque habitant consomme 30L par jour
        self.besoin_infra = self.eval_besoin_infra() # besoin lié aux infrastructures
        resultat = (self.besoin + self.besoin_infra) # besoin total
        resultat.label = "besoin"
        return resultat



    def __str__(self):
        if self.lb != "":
            return self.lb
        return f"[{self.x, self.y}],  nb hab ≈ {(self.nb_habitants.b + self.nb_habitants.c)/2} | {self.ressenti} {self.infrastructure}| besoin : {self.besoin} "



class Source():
    """
    Objet de type source
    """
    def __init__(self, carte,  x, y, couleur, debit, odeur, lb=""):
        self.carte = carte # carte associée
        x, y = int(map_range(x, 0, carte.x_max, 0, carte.l)), int(map_range(y, 0, carte.y_max, 0, carte.L)) # x et y remappés à la carte
        self.lb = lb # nom de la source
        self.x = x
        self.y = y
        self.couleur = couleur # couleur de l'eau (entrée floue)
        self.debit = debit # débit de la source L/s (IFT)
        self.odeur = odeur # odeur (entrée floue)

    def __str__(self):
        if self.lb != "":
            return self.lb
        else:
            return self
def CAF2(village, source):
    """
    Module de calcul d'arithmétique flou permettant de déterminer la proportion de débit de la source par rapport au besoin
    """
    besoin = village.besoin
    debit = source.debit
    ift = debit*86400/besoin # comme le débit est en litres par seconde, il faut le reconvertir en litres/jour
    ift.label = "prop debit/besoin"
    return prop_debit_besoin.possibilite(ift.poly()) # évalue l'appartenance aux différentes classes de l'entrée floue proportion entre le débit et le besoin


def calculer_score(carte, village, source, show = True):
    """
    Permet de calculer un score de correspondance à un couple (village, source)
    """
    proportion_debit_besoin = CAF2(village, source) # calcul la qualification de la proportion débit/besoin entre le village et le source
    qualite_eau = SIF5.inference(source.couleur, source.odeur, show=show ) # déduit la qualité de l'eau de la source grâce à sa couleur et son odeur
    score_eau = SIF7.inference( proportion_debit_besoin, qualite_eau, show=show) # calcul un score lié à l'eau
    diff_altitude = difference_altitude.v(abs(carte.alt(village)-carte.alt(source))) # qualifie la différence d'altitude
    altitude_cum = altitude_cumulee.v(abs(carte.alt_cum(village, source))) # qualifie l'altitude cumulée
    difficulte_geo = SIF4.inference(altitude_cum, diff_altitude, show=show) # déduit la difficulté géographique associée
    diff_dist = difference_distance.v(carte.distance(village, source)) # qualifie la différence de distance
    score_geo = SIF6.inference( diff_dist, difficulte_geo, show=show) # en déduit un score géographique associé
    score = SIF8.inference(score_geo, score_eau, show=show) # combine les deux scores pour obtenir le score final
    score_defuzz = score_village_src.eval(score) # le défuzzifie pour réaliser le matching
    return (score_defuzz, score) # renvoie quand même le score fuzzifié pour logs
