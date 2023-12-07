import numpy as np
from scipy.optimize import linear_sum_assignment
import Calcul_flou
import Objets

import Astar



import networkx as nx
def optimize(dico):
# Create a bipartite graph
    G = nx.Graph()
    # Add nodes from types A and B
    nodes_A = set(pair[0] for pair in dico.keys())
    nodes_B = set(pair[1] for pair in dico.keys())
    G.add_nodes_from(nodes_A, bipartite=0)
    G.add_nodes_from(nodes_B, bipartite=1)

    # Add weighted edges based on the scores
    for (a, b), score in dico.items():
        G.add_edge(a, b, weight=score)

    # Find the maximum-weight matching
    matching = nx.bipartite.matching.minimum_weight_full_matching(G, weight='weight')


    return matching

def optimisation_score(dico):
    villages = list(set([key[0] for key in dico.keys()]))
    sources = list(set([key[1] for key in dico.keys()]))
    a_attribuer = set(sources)
    resultat = {village : [] for village in villages}
    dico1 = dico
    while len(a_attribuer) > 0:

        tmp = optimize(dico1)

        for village, source in {key : value for key, value in tmp.items() if isinstance(key, Objets.Village)}.items():
            resultat[village].append(source)
            a_attribuer.remove(source)


        dico1 = {couple_village_source : score for couple_village_source, score in dico1.items() if couple_village_source[1] in list(a_attribuer)}

    return resultat


if __name__ == "__main__":
    score_dict = Calcul_flou.score_dict
    matching = optimisation_score(score_dict)
    print("a",[(str(v),[str(src) for src in srcs])  for v, srcs in optimisation_score(score_dict).items()])
    for village, sources in matching.items():
        for source in sources:
            pass
