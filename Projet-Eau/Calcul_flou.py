from flou_import import *
from Classes import *
from Rules import *
from generator_data import *


def faisabilite(carte, liste_village, liste_sources):

    res_total_fav = sum([ village.ressenti["favorable"] for village in liste_village ])/len(liste_village)
    res_total_defav = sum([village.ressenti["defavorable"] for village in liste_village]) / len(liste_village)
    res_total = ressenti.v(res_total_defav, res_total_fav)

    access = carte.accessibilite
    type_terr = carte.type_terrain

    diff_dist = 0
    diff_alt = 0
    alt_cum = 0


    somme_besoin = NFT(0,0,0,1,"somme besoin village")
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


    somme_src =  NFT(0,0,0,1,"somme besoin source")
    for source in liste_sources:
        somme_src = somme_src + source.debit * 86400
    somme_src = somme_src / len(liste_sources)

    prop_src_besoin = somme_src /somme_besoin
    prop_src_besoin = proportion_sources_besoins.possibilite(prop_src_besoin.poly())

    conditions_geologiques = SIF1.inference(type_terr, alt_cum, diff_alt)
    score_terrain = SIF2.inference(access,  conditions_geologiques, diff_dist)
    faisable = SIF3.inference(res_total, prop_src_besoin, score_terrain)
    print(faisable)
    return faisable





    print(res_total)
def scores_villages_sources(carte, liste_village, liste_sources):
    dico = {}
    for village in liste_village:
        for source in liste_sources:
            score = calculer_score(carte, village, source)
            dico[(village, source)] = score[0]
            print(score)
            print()
            dico[((village.x, village.y), (source.x, source.y))] = score[0]
    return dico









carte = Carte("test_elevation.png")
carte.carte = cv2.resize(carte.carte, (100,100))
carte.carte_color = cv2.resize(carte.carte_color, (100,100))
carte.l, carte.L = 100,100
villages = generate_village(carte, 5)
print(villages)
sources = generate_sources(carte, 5)
print(sources)
print(scores_villages_sources(carte, villages, sources))
