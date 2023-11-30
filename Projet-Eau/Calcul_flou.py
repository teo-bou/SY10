from flou_import import *
from Classes import *
from Rules import *
from generator_data import *


def faisabilite(carte, liste_village, liste_sources):
    pass


def scores_villages_sources(carte, liste_village, liste_sources):
    dico = {}
    for village in liste_village:
        for source in liste_sources:
            score = calculer_score(carte, village, source)
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
