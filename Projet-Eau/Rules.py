from flou_import import *
from Classes import *

SIF1_1 = Table("SIF 1.csv")
SIF1_2 = Table("SIF 1.2.csv")

SIF1 = Table_mult(type_terrain, SIF1_1, SIF1_2, label="conditions geologiques")

print(SIF1)
val1 = {"faible":0, "moyenne":0.4 , "elevee":0 }
val2 = {"faible":0.8, "moyenne": 0.3, "elevee":0 }
print(SIF1.inference(type_terrain.v(0.2, 0.5), val1, val2 ))

SIF2_1 = Table("SIF 2.1.csv")
SIF2_2 = Table("SIF 2.2.csv")
SIF2_3 = Table("SIF 2.3.csv")

SIF2 = Table_mult(accessibilite, SIF2_1, SIF2_2, SIF2_3, label="score terrain")

SIF3_1 = Table("SIF 3.1.csv")
SIF3_2 = Table("SIF 3.2.csv")

SIF3 = Table_mult(ressenti, SIF3_1, SIF3_2, label="faisabilite")

SIF4 = Table("SIF 4.csv")

SIF5 = Table("SIF 5.csv")

SIF6 = Table("SIF 6.csv")

SIF7 = Table("SIF 7.csv")

SIF8 = Table("SIF 8.csv")


