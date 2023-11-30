
from heapq import *
import math
import main


def get_neighbours(carte, x, y):
    check_neighbour = lambda x, y: True if 0 <= x < cols and 0 <= y < rows else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
    return [(carte.alt((x,y)), (x + dx, y + dy)) for dx, dy in ways if check_neighbour(x + dx, y + dy)]




def heuristic(carte, a, b):
   return abs(a[0] - b[0]) + abs(a[1] - b[1]) + 0.1*abs(carte.alt(a)-carte.alt(b))


# def heuristic(a, b):
#    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def dijkstra(carte, start, goal, graph):
    queue = []
    heappush(queue, (0, start))
    cost_visited = {start: 0}
    visited = {start: None}

    while queue:
        cur_cost, cur_node = heappop(queue)
        if cur_node == goal:
            break

        try:
            neighbours = graph[cur_node]
            print(cur_node)
            for neighbour in neighbours:
                neigh_cost, neigh_node = neighbour
                new_cost = cost_visited[cur_node] + neigh_cost

                if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                    priority = new_cost + heuristic(carte, neigh_node, goal)
                    heappush(queue, (priority, neigh_node))
                    cost_visited[neigh_node] = new_cost
                    visited[neigh_node] = cur_node
        except:
            pass
    return visited



grid = ['22222222222222222222212',
        '22222292222911112244412',
        '22444422211112911444412',
        '24444444212777771444912',
        '24444444219777771244112',
        '92444444212777791192144',
        '22229444212777779111144',
        '11111112212777772771122',
        '27722211112777772771244',
        '27722777712222772221244',
        '22292777711144429221244',
        '22922777222144422211944',
        '22222777229111111119222']
grid = [[int(char) for char in string ] for string in grid]
# adjacency dict
rows, cols = main.carte.l, main.carte.L
graph = {}
for y, row in enumerate(main.carte.carte):
    for x, col in enumerate(row):
        graph[(x, y)] = graph.get((x, y), []) + get_neighbours(main.carte, x, y)

start = (0, 7)
goal = start
queue = []
heappush(queue, (0, start))
visited = {start: None}

# bg = pg.image.load('img/2.png').convert()
# bg = pg.transform.scale(bg, (cols * TILE, rows * TILE))
while True:
    # fill screen
    #sc.blit(bg, (0, 0))

    # bfs, get path to mouse click
    mouse_pos = (main.S.x, main.S.y)
    print(mouse_pos)
    if mouse_pos:
        visited = dijkstra(main.carte, start, mouse_pos, graph)
        goal = mouse_pos
    #print(visited)
    # draw path
    path_head, path_segment = goal, goal

    while path_segment and path_segment in visited:
       print(path_head, path_segment)
    #     pg.draw.circle(sc, pg.Color('blue'), *get_circle(*path_segment))
    #     path_segment = visited[path_segment]
    # pg.draw.circle(sc, pg.Color('green'), *get_circle(*start))
    # pg.draw.circle(sc, pg.Color('magenta'), *get_circle(*path_head))
    #
    # # pygame necessary lines
    # [exit() for event in pg.event.get() if event.type == pg.QUIT]
    # pg.display.flip()
    # clock.tick(30)