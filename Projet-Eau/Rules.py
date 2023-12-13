from Classes import *

# import des différentes règles floues

SIF1_1 = Table("SIF 1.csv")
SIF1_2 = Table("SIF 1.2.csv")

# Table_mult est utilisé lorsqu'il y a plus que deux classes impliquées
SIF1 = Table_mult(type_terrain, SIF1_1, SIF1_2, meaning="conditions geologiques")




SIF2_1 = Table("SIF 2.1.csv")
SIF2_2 = Table("SIF 2.2.csv")
SIF2_3 = Table("SIF 2.3.csv")

SIF2 = Table_mult(accessibilite, SIF2_1, SIF2_2, SIF2_3, meaning="score terrain")

SIF3_1 = Table("SIF 3.1.csv")
SIF3_2 = Table("SIF 3.2.csv")

SIF3 = Table_mult(ressenti, SIF3_1, SIF3_2, meaning="faisabilite")

SIF4 = Table("SIF 4.csv", meaning="difficulte geographique")

SIF5 = Table("SIF 5.csv", meaning="qualite eau")

SIF6 = Table("SIF 6.csv", meaning="score geographique")

SIF7 = Table("SIF 7.csv", meaning="score eau")

SIF8 = Table("SIF 8.csv", meaning="score du village")


