from Rules import *
import math
import cv2
def T_probabiliste(x,y):
    return x*y

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
    def __init__(self, carte, jour, accessibilite =None, type_terrain = None, resized_factor = 0.75):
        self.saison = self.eval_saison(jour)
        self.l = None # largeur et longueur la carte mis à jour automatiquement
        self.L = None
        self.carte_color = None
        self.carte = None
        self.lire_carte(carte) # instancie et lit les cartes (une en couleur, une en noir et blanc)
        self.resize_x = int(self.l * resized_factor)  # taille de la carte redimensionnée
        self.resize_y = int(self.l * resized_factor)
        self.carte_resized = cv2.resize(self.carte, (self.resize_x, self.resize_y)) # carte redimensionnée aux dimensions données
        self.alt_min = 0 # altitude varie entre 0 et le max spécifié dans l'entrée floue difference altitude
        self.alt_max = difference_altitude.range.b
        self.x_max = difference_distance.range.b / math.sqrt(2) # comme x_max**2 + ymax**2 = difference_distance_max**2, on en déduit x_max et y_max étant donné que la carte est carrée et toutes les valuers positives
        self.y_max = difference_distance.range.b / math.sqrt(2)
        self.accessibilite = accessibilite # Stocke la valeur d'accessibilité du terrain
        self.type_terrain = type_terrain  # Stocke l'escarpement du terrain
        self.praticabilite = SIF0.inference(self.type_terrain, self.saison, tnorme=T_probabiliste, show=False) # calcul la praticabilité associée au terrain


    def eval_saison(self, jour):
        jj, mm = tuple(jour.split("/"))
        jj, mm = int(jj), int(mm)
        mois = mm+jj*1/30 # converti le mois et le jour en le numéro du mois avec en décimal la progression dans le mois
        saison_result = saison.v(mois) # récupère la saison associée
        return saison_result
    def carte3D(self, angle):
        x = np.outer(np.linspace(0, min(self.l, self.L) - 1, 200), np.ones(200)) #initialise un grid de 1 pour les x, avec une résolution de 200
        y = x.copy().T #initialise un grid de 1 pour les y
        z = np.array([[max(0, self.alt(Point((int(yii), int(xii))))) for xii, yii in zip(xi, yi)] for xi, yi in zip(x, y)]) # calcule l'altitude de chaque point de la carte


        ax = plt.axes(projection='3d') # créé la figure en 3D
        my_cmap = plt.get_cmap('viridis') # récupère la color-map pour les couleurs


        ax.set_zlim([0, 1500]) # initialise la vue
        ax.view_init(angle,0,0) # initialise le point de vue
        ax.plot_surface(x, y, z, cmap=my_cmap, edgecolor='none') #trace la surface correspondante
        plt.show() # affiche la carte


    def __str__(self):
        """
        Affiche la carte
        """


        self.carte3D(90)
        self.carte3D(50)
        plt.imshow(self.carte_color)
        plt.show()
        return f"Carte allant de x=[0;{self.x_max}], y = [0; {self.y_max}], alt = [{self.alt_min}; {self.alt_max}]"
    def lire_carte(self, carte):
        """
        Récupère l'image associée et update les cartes
        """
        image_elevation = cv2.imread("./cartes/"+carte) # récupère l'image dans le dossier carte
        x,y = image_elevation.shape[0], image_elevation.shape[1]
        if x<y: # rogne l'image au plus grand  carré
            image_elevation = image_elevation[:,:x]
        else:
            image_elevation = image_elevation[:y,:]
        self.carte_color = image_elevation
        image_gray = cv2.cvtColor(image_elevation, cv2.COLOR_BGR2GRAY) # converti l'image en noir et blanc
        self.carte = np.array(image_gray,  dtype=np.float64)
        self.L, self.l = image_gray.shape[0], image_gray.shape[1] # récupère les dimensions de l'image




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
    def __init__(self, carte, x, y, nb_habitants, ressenti_ent, ressenti_conf, infrastructure, lb=""):
        self.lb = lb # nom du village
        self.carte = carte # carte associée
        x, y = int(map_range(x, 0, carte.x_max, 0, carte.l)), int(map_range(y, 0, carte.y_max, 0, carte.L)) # coordonnées du villages mappées à la carte
        self.x = x
        self.y = y
        self.nb_habitants = nb_habitants
        self.ressenti_ent = ressenti_ent #ressenti des habitants vis à vis du projet
        self.ressent_conf = ressenti_conf # ressenti sur l'apparitions de conflits dans la zone
        self.score_hum = SIF3bis.inference(ressenti_conf, ressenti_ent, show=False)
        self.infrastructure = infrastructure # infrastructures que le village a, nécessitants des besoins plus importants
        self.besoin = self.eval_besoin() # Calcul le besoin en eau par jour du village

    def eval_besoin_infra(self):
        """
        Évalue le besoin en eau hebdomadaire du village
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
