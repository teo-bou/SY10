from Classes import *

# import des différentes règles floues

SIF1_1 = Table("SIF 1.1.csv")
SIF1_2 = Table("SIF 1.2.csv")
SIF1_3 = Table("SIF 1.3.csv")
SIF1_4 = Table("SIF 1.3.csv")

# Table_mult est utilisé lorsqu'il y a plus que deux classes impliquées
SIF1 = Table_mult(praticabilite, SIF1_4, SIF1_3, SIF1_2, SIF1_1, meaning="conditions geologiques")




SIF2_1 = Table("SIF 2.1.csv")
SIF2_2 = Table("SIF 2.2.csv")
SIF2_3 = Table("SIF 2.3.csv")

SIF2 = Table_mult(accessibilite, SIF2_1, SIF2_2, SIF2_3, meaning="score terrain")

SIF3_1 = Table("SIF 3.1.csv")
SIF3_2 = Table("SIF 3.2.csv")
SIF3_3 = Table("SIF 3.3.csv")

SIF3 = Table_mult(score_humain, SIF3_2, SIF3_3, SIF3_1, meaning="faisabilite")



#### Tables normales

SIF0 = Table("SIF 0.csv", meaning="praticabilite")

SIF3bis = Table("SIF 3bis.csv", meaning="score_humain")

SIF4 = Table("SIF 4.csv", meaning="difficulte geographique")

SIF5 = Table("SIF 5.csv", meaning="qualite eau")

SIF6 = Table("SIF 6.csv", meaning="score geographique")

SIF7 = Table("SIF 7.csv", meaning="score eau")

SIF8 = Table("SIF 8.csv", meaning="score du village")


