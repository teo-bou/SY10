from flou_import import *
from Classes import *
from Rules import *
from Objets import *

Score = {}


#
# for village in village_liste:
#     for source in source_liste:
#         pass


ZZ = Village(223,396,NFT(10000,20000,30000,1,'hab'),ressenti.v(0.2,1),{"hopital":2, "ecole":3,"gouvernement":1})
print("Le village ZZ",ZZ)
print(ZZ.besoin)

S = Source(20,30,couleur_eau.v(0.2,1),NFT(1,2,3,1,'debit')*30, odeur_eau.v(0,0,0.2))
print(ZZ.distance(S))
result = CAF2(ZZ, S)
print()
result1 = SIF5.inference(S.couleur, S.odeur)
print(result1)
score = SIF7.inference(result, result1)
print(score)