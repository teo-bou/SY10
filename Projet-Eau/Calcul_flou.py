from matching import optimisation_score
from Astar import *
import matplotlib.pyplot as plt
import seaborn as sns

def faisabilite(carte, liste_village, liste_sources, show = False, defuz = False):
    """
    Calcul de la faisabilité globale du projet
    """
    scoreh_fav = sum([ village.score_hum["favorable"] for village in liste_village ])/len(liste_village) # Calcul la moyenne des scores-humain favorables de chaque village
    scoreh_neut = sum([village.score_hum["neutre"] for village in liste_village]) / len(liste_village)  # Calcul la moyenne des scores-humain neutre de chaque village
    scoreh_defav = sum([village.score_hum["defavorable"] for village in liste_village]) / len(liste_village)  # Calcul la moyenne des scores-humain défavorables de chaque village
    scoreh = score_humain.v(scoreh_defav, scoreh_neut,  scoreh_fav) # Rentre ces données dans l'entrée floue score-humain

    access = carte.accessibilite
    practicab = carte.praticabilite

    # Initialise les différentes variables pour le calcul de moyenne

    diff_dist = 0
    diff_alt = 0
    alt_cum = 0


    somme_besoin = IFT(0,0,0,0,1,"somme besoin village")

    # Moyenne des differences d'altitudes, de distance, d'altitudes cumulées, et de la somme des besoins de tous les villages

    for village in liste_village:
        somme_besoin = somme_besoin + village.besoin
        for source in liste_sources:
            diff_dist += carte.distance(village, source)
            diff_alt +=carte.dist_alt(village, source)
            alt_cum += carte.alt_cum(village, source)

    somme_besoin = somme_besoin / len(liste_village)

    diff_dist/=len(liste_village)*len(liste_sources)
    diff_alt /= len(liste_village) * len(liste_sources)
    alt_cum /= len(liste_village) * len(liste_sources)

    diff_dist = difference_distance.v(diff_dist)
    diff_alt = difference_altitude.v(diff_alt)
    alt_cum = altitude_cumulee.v(alt_cum)


    somme_src =  IFT(0,0,0,0,1,"somme besoin source")
    for source in liste_sources:
        somme_src = somme_src + source.debit * 86400 # Le débit étant donné par seconde il faut le reconvertir
    somme_src = somme_src / len(liste_sources) # On prend la moyenne
    prop_src_besoin = somme_src /somme_besoin # Calcul de la proportion débits total des sources / somme des besoins des villages

    prop_src_besoin = proportion_sources_besoins.possibilite(prop_src_besoin.poly()) # Évaluation de cette proportion dans l'entrée correspondante par calcul de possibilité
    if show:
        print("Proportion entre le débit et le besoin", prop_src_besoin)
    conditions_geologiques = SIF1.inference(practicab, diff_alt, alt_cum, tnorme=T_probabiliste,  show = show) # Calcul des conditions géologiques
    score_terrain = SIF2.inference(access, conditions_geologiques, diff_dist, tnorme=T_probabiliste, show = show) # du score terrain
    faisable = SIF3.inference(scoreh, prop_src_besoin, score_terrain,tnorme=T_probabiliste, show = True) # et enfin de la faisabilité

    if defuz: # si volonté de défuzzifier
        index = round(sum([i*faisable[key] for i, key in enumerate(faisable.keys())])/sum(list(faisable.values()))) # calcul le barycentre discret
        result_defuz = list(faisable.keys())[index]
        if show:
            print(f"Faisabilité : {result_defuz}")
            if index <= 2:
                print("Soyez sage au sens de Socrate, admettez l'impuissance et ne continuez pas forcément dans cette voie")
        return (defuz, faisable)

    return faisable



def scores_villages_sources(carte, liste_village, liste_sources, show=False):
    """
    Calcule pour chaque couple village source le score associé, pour pouvoir plus tard associer des villages et des sources
    """
    dico = {}
    for village in liste_village:
        for source in liste_sources:
            if show:
                print(village, source)
            score = calculer_score(carte, village, source, show) # pour chaque couple possible, calculer le score
            dico[(village, source)] = score[0] # On ne prend que la première composante, défuzzifiée, la 2ème correspondant au score fuzzifé
            if show:
                print()
    return dico
def matching_score_village(carte, liste_village, liste_sources, show = False):
    """
    Association des sources aux villages
    """
    score_dico = scores_villages_sources(carte, liste_village, liste_sources, show=show) # récupère les scores associés à chauqe couple village source
    matching = optimisation_score(score_dico) # réalise l'association, un village pour chaque source
    return matching
def tracer_carte(carte, liste_village, liste_sources, show = False):
    """
    Tracer des villages, sources et chemins sur la carte
    """
    palette = sns.color_palette("inferno", len(liste_village)).as_hex() # initialisation d'une palette de couleur
    palette = [[tuple(int(color.lstrip("#")[i:i+2], 16) for i in (4, 2, 0))][0] for color in palette] # conversion de cette dernière en BGR pour OpenCV
    colors = {village: palette[i]for i, village in enumerate(liste_village)} # associe à chaque village une couleur
    matching = matching_score_village(carte, liste_village, liste_sources, show= False) # récupère les associations village : [sources]
    th = round(carte.l /100) #thickness des élements du dessin
    carte_globale = carte.carte_color.copy() # crée une carte globale sur laquelle afficher les chemins
    for village, sources in matching.items(): # pour chaque village :
        if show:
            print(village, ": ", end="")
        color = colors[village] # récupère la couleur du village
        carte_globale = cv2.circle(carte_globale, (village.x, village.y), 3*th, color, -1) # affiche un cercle sur le village sur la carte
        carte_village = carte.carte_color.copy() # carte vierge pour chaque village
        carte_village = cv2.circle(carte_village, (village.x, village.y), 4*th, color, -1) # affiche un cercle sur le village sur la carte
        for source in sources: # pour chaque source associée
            if show:
                print(source, end=", ")
            start = (source.x, source.y)
            goal = (village.x, village.y)
            path = search_map(carte, start, goal) #r écupère le chemin optimal trouvé
            carte_globale = tracer(carte, carte_globale, path, color,round(2/3*th)) # trace le chemin sur les cartes
            carte_village = tracer(carte, carte_village, path, color, th)
            carte_globale = croix(carte_globale, start, color, th, th) # trace une croix à l'endroit de la source
            carte_village = croix(carte_village, start, color, th, 2*th)
        if show:
            plt.imshow(carte_village)
            plt.show()
            print()
    print("Carte globale : ")
    plt.imshow(carte_globale) # affiche la carte
    plt.show()

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
    score = SIF8.inference(score_geo, score_eau,tnorme=T_probabiliste,  show=show) # combine les deux scores pour obtenir le score final
    score_defuzz = score_village_src.eval(score) # le défuzzifie pour réaliser le matching
    return (score_defuzz, score) # renvoie quand même le score fuzzifié pour logs






