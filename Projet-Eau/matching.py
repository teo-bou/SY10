import numpy as np
from scipy.optimize import linear_sum_assignment
import Calcul_flou
import Objets

import Astar



import networkx as nx
def optimize(dico):
    """
    Réalise le matching partiel de couples (village, source)
    """
    G = nx.Graph() # créé un graph
    # récupère les villages et les sources
    villages = set(pair[0] for pair in dico.keys())
    sources = set(pair[1] for pair in dico.keys())
    # les ajoute au graph avec les contraintes de chaque source ne peut avoir au max que 1 village
    G.add_nodes_from(villages, bipartite=0)
    G.add_nodes_from(sources, bipartite=1)

    # Rajoute les scores au graph
    for (village, source), score in dico.items():
        G.add_edge(village, source, weight=score)

    # trouve le matching maximisant les scores
    matching = nx.bipartite.matching.minimum_weight_full_matching(G, weight='weight')


    return matching

def optimisation_score(dico):
    """
    Performe le matching complet de couples (village, source)
    """
    villages = list(set([key[0] for key in dico.keys()])) # récupère les villages sans doublons
    sources = list(set([key[1] for key in dico.keys()])) # récupère les sources sans doublons
    a_attribuer = set(sources) # ensemble des sources qu'il reste à attribuer
    resultat = {village : [] for village in villages} # initialise le dictionnaire de sortie
    while len(a_attribuer) > 0: # tant qu'il reste des sources à attribuer

        tmp = optimize(dico) # trouver le matching partiel

        for village, source in {key : value for key, value in tmp.items() if isinstance(key, Objets.Village)}.items(): # récupère seulement la liste des couples (village, sources) et pour chaque:
            resultat[village].append(source) # rajoute la source au village dans le dictionnaire de sortie
            a_attribuer.remove(source) # enlève la source de l'ensemble à attribuer


        dico = {couple_village_source : score for couple_village_source, score in dico.items() if couple_village_source[1] in list(a_attribuer)} # ne garde que les couples dont la source a besoin d'être encore attribuée

    return resultat
