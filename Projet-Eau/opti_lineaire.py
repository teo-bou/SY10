import numpy as np
from scipy.optimize import linear_sum_assignment
import Calcul_flou
import Objets
score_dict = Calcul_flou.score_dict
import Astar2
print(score_dict)
# Your dictionary with scores
#score_dict = {('A1', 'B1'): 10, ('A1', 'B2'): 5, ('A2', 'B1'): 8, ('A2', 'B2'): 9}
#
# # Extract unique elements of A and B
# elements_A = list(set([pair[0] for pair in score_dict.keys()]))
# elements_B = list(set([pair[1] for pair in score_dict.keys()]))
#
# # Create a cost matrix
# cost_matrix = np.zeros((len(elements_A), len(elements_B)))
#
# # Set a very high cost for multiple associations of A with B
# high_cost = 1000  # You can adjust this value based on your needs
#
# # Populate the cost matrix with scores from the dictionary
# for i, element_A in enumerate(elements_A):
#     for j, element_B in enumerate(elements_B):
#         if (element_A, element_B) in score_dict:
#             cost_matrix[i, j] = -score_dict[(element_A, element_B)]
#         else:
#             cost_matrix[i, j] = high_cost
#
# # Use the Hungarian algorithm to find the optimal assignment
# row_indices, col_indices = linear_sum_assignment(cost_matrix)
#
# # Build the optimal assignment
# optimal_assignment = {}
# for i, element_A_index in enumerate(row_indices):
#     element_A = elements_A[element_A_index]
#     element_B = elements_B[col_indices[i]]
#     if cost_matrix[element_A_index, col_indices[i]] != high_cost:
#         optimal_assignment[element_A] = element_B
#
# # Print the optimal assignment
# for element_A, element_B in optimal_assignment.items():
#     print(f"{element_A} -> {element_B}")
#
# print()
# print(len(optimal_assignment))
# print(optimal_assignment)

import networkx as nx

# Your dictionary with scores

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
matching = optimisation_score(score_dict)
print("a",[(str(v),[str(src) for src in srcs])  for v, srcs in optimisation_score(score_dict).items()])
for village, sources in matching.items():
    for source in sources:
        Astar2.show_map(Calcul_flou.carte, village, source)
