from flou_import import *

type_terrain = Classe_classification("type_terrain", "peu escarpe", "escarpe")
accessibilite = Classe_classification("accessibilite", "peu accessible", "moyennement accessible", "accessible")
ressenti = Classe_classification("ressenti", "favorable", "defavorable")
couleur_eau = Classe_classification("couleur de l'eau", "claire", "trouble")
odeur_eau = Classe_classification("odeur de l'eau","pas d'odeur", "odeur", "forte odeur")


difference_distance = Classe("difference distance")
diff_dist_faible = IFT(0,0,200, 900,1, "faible")
diff_dist_moyenne = IFT(300, 900, 1000, 1600, 1, "moyenne")
diff_dist_elevee = IFT(1000, 1600, 1800, 1800,1,  "elevee")
difference_distance.ajouter(diff_dist_faible, diff_dist_moyenne, diff_dist_elevee)
difference_distance.plot()
