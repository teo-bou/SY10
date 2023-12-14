from heapq import heappop, heappush
from Objets import *


Colors = [(255,0,0), (0,255,0), (0,0,255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (120, 0, 0)]

class Node:
    """
    Représente un point géographique sur la carte
    """

    def __init__(self, position):

        self.position = position
        self.g = 0 # Ceci sont les différentes composants pour évaluer plus tard le coût d'un certain chemin, dans le but de le minimiser
        self.h = 0
        self.f = 0
        self.parent = None # de quelle point vient-on ?

    def __lt__(self, other):
        """
        Permet de faire la comparaison entre deux points ( A < B ) == True ou False ?
        La réalise en fonction du coût du point
        """

        return self.f < other.f


def calculate_heuristic(map, neighbour, current, goal) :
    """
    Calcule à quel point emprunter le point voisin est coûteux
    """
    # Pour cela on retourne la distance de Manhattan (abs(X2-X1) + abs(Y2-Y1)) par rapport à la destination (si on s'éloigne coût plus important) sommée à la différence d'altitude absolue entre les deux points, différence calculée sur la carte mise à l'échelle (d'où le res=True)

    return   abs(current[0] - goal[0]) + abs(current[1] - goal[1]) + 2* abs(map.alt(Point(neighbour), res=True)- map.alt(Point(current), res = True))


def get_neighbors(current, map_size):
    """
    Renvoie les différents voisins du point actuel (points que l'on peut atteindre depuis le point actuel)
    """

    neighbors = []
    x, y = current

    # On regarde tous les pixels adjacents
    if x > 0:
        neighbors.append((x - 1, y))
    if x < map_size[0] - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < map_size[1] - 1:
        neighbors.append((x, y + 1))

    return neighbors


def search_map(map, start, goal):
    """
    Calcul du chemin à emprunter
    """
    # Vérifie que les points de départ et d'arriver sont bien sur la carte
    if start[0] < 0 or start[0] >= map.l or start[1] < 0 or start[1] >= map.L:
        raise ValueError("Départ est en dehors de la carte")
    if goal[0] < 0 or goal[0] >= map.l or goal[1] < 0 or goal[1] >= map.L:
        raise ValueError("Arrivée est en dehors de la carte")

    # Récupère et remet à l'échelle (on utilise une carte mise à l'échelle pour moins de temps de calcul) les coordonnées des points de départ et d'arrivée

    start = (int(map_range(start[0], 0, map.l, 0, map.resize_x)), int(map_range(start[1], 0, map.L, 0, map.resize_y)))
    goal = (int(map_range(goal[0], 0, map.l, 0, map.resize_x)), int(map_range(goal[1], 0, map.L, 0, map.resize_y)))




    # Initialise la liste des points à traité et visité
    open_list = []
    closed_list = set()

    start_node = Node(start)

    # Commence à traiter le point de départ
    heappush(open_list, start_node) # les heaps sont des listes avec indicateur de priorité. Cela permet de prioriser les points ayant le coût le moins élevé

    # Commence l'algorithme A*
    while open_list:
        # récupere le point avec le coût le plus bas, c'est celui là qu'on traitera
        current_node = heappop(open_list)

        # si on a atteint notre destination
        if current_node.position == goal:
            # On refait le chemin en retournant à l'envers d'où on vient
            path = []
            while current_node:  # tant qu'on trouve un parent à notre point (tant qu'on vient d'un autre point)
                path.append(current_node.position) #on ajoute ce point
                current_node = current_node.parent  # et ainsi de suite
            return path[::-1]  # Pour récupérer le chemin dans le bon ordre, on l'inverse

        # On a traité ce point et on peut donc l'ajouter dans notre liste des visités
        closed_list.add(current_node.position)

        # On récupère les voisins de notre points pour calculer leur coût
        neighbors = get_neighbors(current_node.position, (map.resize_x, map.resize_y))

        for neighbor in neighbors:
            # Si on a déjà visité ce voisin, on le passe
            if neighbor in closed_list:
                continue

            neighbor_node = Node(neighbor)

            # Comme on change de point, on rajoute 1 au h (qui compte la distance déjà parcourue et ainsi pousse l'algorithme à aller le plus vite possible à la destination)
            neighbor_node.g = current_node.g + 1

            # On calcule le coût pour passer à ce voisin là
            neighbor_node.h = calculate_heuristic(map,current_node.position, neighbor, goal)

            # Le coût total est la somme des coûts associés au chemin déjà parcourus et au passage vers ce voisin
            neighbor_node.f = neighbor_node.g + neighbor_node.h

            # Indique à ce voisin que l'on vient du point actuel
            neighbor_node.parent = current_node

            # Rajoute ce voisin dans la liste des points à traiter pour la suite
            heappush(open_list, neighbor_node)

    # Si pas de chemin trouvé
    return []

def tracer(map, img, path,color, th):
    """
    Affiche sur la carte le chemin
    """

    pts = np.array([[int(map_range(point[0], 0, map.resize_x, 0, map.l)), int(map_range(point[1], 0, map.resize_y, 0, map.L))]for point in path],
                   dtype=np.int32) # remets à l'échelle les points trouvés sur la carte plus petite à la taille de la carte originelle
    pts = pts.reshape((-1, 1, 2)) #formattage pour OpenCV

    img = cv2.polylines(img.copy(), pts, True, color, th) # Trace le trait sur l'image donnée
    return img

def croix(img, pts, color, thickness, space):
    """
    Trace une croix à la position donnée
    """
    x,y = pts
    img = cv2.line(img.copy(), (x-space, y+space), (x+space, y-space), color, thickness) # ligne du coin gauche bas vers le haut droit
    img = cv2.line(img.copy(), (x-space, y-space), (x+space, y+space), color, thickness) # ligne du coin gauche haut vers le bas droit
    return img
def show_map(map, start, goal):
    """
    Utilise les fonctions définies précedemment pour afficher la carte annotée
    """


    start = (start.x, start.y)
    goal = (goal.x, goal.y)

    path = search_map(map, start, goal)
    img = tracer(map, map.carte_color, path)
    plt.imshow(img)
    plt.show()


