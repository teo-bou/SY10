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
            #dico[((village.x, village.y), (source.x, source.y))] = score[0]
    return dico









carte = Carte("test_elevation.png", type_terrain=type_terrain.v(0.6,0.3), accessibilite=accessibilite.v(0.7,0.5,0))
carte.carte = cv2.resize(carte.carte, (100,100))
carte.carte_color = cv2.resize(carte.carte_color, (100,100))
carte.l, carte.L = 100,100
villages = generate_village(carte, 5)
villages = [Village(carte, 0, 0, NFT(1500, 2700, 3000, 1, 'hab'), ressenti.v(0.2, 0.8),
             {"hopital": 1, "ecole": 3, "gouvernement": 1}, "A"),
Village(carte, 1000, 1000, NFT(500, 1000, 1200, 1, 'hab'), ressenti.v(0, 0.8),
             {"hopital": 2, "ecole": 3, "gouvernement": 0}, "B"),
Village(carte, 200, 200, NFT(2100, 2200, 2300, 1, 'hab'), ressenti.v(0.2, 0.5),
             {"hopital": 3, "ecole": 1, "gouvernement": 1}, "C"),
Village(carte, 500, 700, NFT(5000, 10000, 15000, 1, 'hab'), ressenti.v(0.5, 0.7),
             {"hopital": 2, "ecole": 2, "gouvernement": 1}, "D")
            ]
#print([str(village)for village in villages])
print()
sources = generate_sources(carte, 5)
sources = [
Source(carte, 1100, 1000, couleur_eau.v(0.2, 1), NFT(10, 15, 16, 1, 'debit') , odeur_eau.v(0, 0, 0.2), "1"),
Source(carte, 125, 210, couleur_eau.v(0.1, 0.7), NFT(1, 2, 3, 1, 'debit') , odeur_eau.v(0, 0, 0.2), "2"),
Source(carte, 840, 720, couleur_eau.v(0.4, 6), NFT(1, 2, 3, 1, 'debit') , odeur_eau.v(0, 0, 0.2), "3"),
Source(carte, 499, 344, couleur_eau.v(1, 0.3), NFT(2, 3, 4, 1, 'debit'), odeur_eau.v(0, 0, 0.2), "4"),
Source(carte, 123, 456, couleur_eau.v(0.2, 1), NFT(1, 2, 3, 1, 'debit') , odeur_eau.v(0, 0, 0.2), "5"),
Source(carte, 998, 499, couleur_eau.v(1, 0.8), NFT(2, 3, 4, 1, 'debit') , odeur_eau.v(0, 0, 0.2), "6")

]
# print([str(source) for source in sources])
print()

print()
score_dict = scores_villages_sources(carte, villages, sources)
print()
print(faisabilite(carte, villages, sources))
