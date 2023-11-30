import random
from Objets import *
from flou_import import map_range
def generate_village(carte, number):
    villages = []
    for i in range(number):
        a = random.randint(0, 100000)
        b = random.randint(0,100000) + a
        c = random.randint(0, 100000) + b
        ift_pop = NFT(a,b,c,1,"habitants village "+str(i))
        x,y = random.randint(0, int(carte.x_max)), random.randint(0, int(carte.y_max))
        village = Village(carte, x,y,ift_pop, ressenti.v(random.random(), random.random()), {"hopital" : random.randint(0,int(map_range(b,0,200000, 0, 15))), "ecole":  int(map_range(b,0,200000, 0, 25)), "gouvernement": int(map_range(b,0,200000, 0, 10))})
        villages.append(village)
    return villages

def generate_sources(carte, number):
    sources = []
    for i in range(number):
        x,y = random.randint(0,int( carte.x_max)), random.randint(0, int(carte.y_max))
        a = random.randint(0, 5)
        b = random.randint(0, 10) + a
        c = random.randint(0, 5) + b
        debit = NFT(a,b,c,1,"source "+str(i))
        sources.append(Source(carte, x,y,couleur_eau.v(random.random(), random.random()),debit,  odeur_eau.v(random.random(),  random.random(), random.random()) ))
    return sources