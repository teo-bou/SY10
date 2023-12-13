from matching import optimisation_score
from Astar import *
import matplotlib.pyplot as plt
import seaborn as sns
def faisabilite(carte, liste_village, liste_sources, show = False):
    """
    Calcul de la faisabilité globale du projet
    """
    res_total_fav = sum([ village.ressenti["favorable"] for village in liste_village ])/len(liste_village) # Calcul la moyenne des ressentis favorables de chaque village
    res_total_defav = sum([village.ressenti["defavorable"] for village in liste_village]) / len(liste_village)  # Calcul la moyenne des ressentis défavorables de chaque village
    res_total = ressenti.v(res_total_defav, res_total_fav) # Rentre ces données dans l'entrée floue ressenti

    access = carte.accessibilite
    type_terr = carte.type_terrain

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

    conditions_geologiques = SIF1.inference(type_terr, diff_alt, alt_cum, show = show) # Calcul des conditions géologiques
    score_terrain = SIF2.inference(access, conditions_geologiques, diff_dist, show = show) # du score terrain
    faisable = SIF3.inference(res_total, prop_src_besoin, score_terrain,show = True) # et enfin de la faisabilité

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

    carte_globale = carte.carte_color.copy() # crée une carte globale sur laquelle afficher les chemins
    for village, sources in matching.items(): # pour chaque village :
        if show:
            print(village, ": ", end="")
        color = colors[village] # récupère la couleur du village
        carte_globale = cv2.circle(carte_globale, (village.x, village.y), 7, color, -1) # affiche un cercle sur le village sur la carte
        carte_village = carte.carte_color.copy() # carte vierge pour chaque village
        carte_village = cv2.circle(carte_village, (village.x, village.y), 12, color, -1) # affiche un cercle sur le village sur la carte
        for source in sources: # pour chaque source associée
            if show:
                print(source, end=", ")
            start = (source.x, source.y)
            goal = (village.x, village.y)
            path = search_map(carte, start, goal) #r écupère le chemin optimal trouvé
            carte_globale = tracer(carte, carte_globale, path, color) # trace le chemin sur les cartes
            carte_village = tracer(carte, carte_village, path, color)
            carte_globale = croix(carte_globale, start, color, 4, 4) # trace une croix à l'endroit de la source
            carte_village = croix(carte_village, start, color, 4, 6)
        if show:
            plt.imshow(carte_village)
            plt.show()
            print()

    plt.imshow(carte_globale) # affiche la carte
    plt.show()

    return carte_globale






if __name__ == "__main__":
    pass

