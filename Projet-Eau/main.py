from flou_import import *
from Classes import *
from Rules import *
from Objets import *
from generator_data import *

print(generate_village(Carte("test_elevation.png"), 5))
carte = "test_elevation.png"
villages = [Village(110,215,NFT(3500,40000,42000,1,"nb_hab 1"), ressenti.v(0.7, 0.3),{"hopital": 1, "ecole":2})]
Score = {}
carte = Carte("test_elevation.png")




ZZ = Village(223,396,NFT(10000,20000,30000,1,'hab'),ressenti.v(0.2,1),{"hopital":2, "ecole":3,"gouvernement":1})
print("Le village ZZ",ZZ)
print(ZZ.besoin)

S = Source(20,30,couleur_eau.v(0.2,1),NFT(1,2,3,1,'debit')*30, odeur_eau.v(0,0,0.2))
print("dist", carte.distance((10,1), ZZ))
carte.alt(ZZ)
result = CAF2(ZZ, S)
print()
result1 = SIF5.inference(S.couleur, S.odeur)
print(result1)
score = SIF7.inference(result, result1)
print(score)
print(carte)