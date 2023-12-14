from flou_import import *

## Définition des entrées floues où l'utilsateur évalue lui-même les degrés d'appartenance (Entrée floues)
type_terrain = Classe_classification("type_terrain", "peu escarpe", "moyen", "escarpe")
score_humain = Classe_classification("score humain", "defavorable", "neutre", "favorable")
accessibilite = Classe_classification("accessibilite", "peu accessible", "moyennement accessible", "accessible")
ressenti_enthousiasme = Classe_classification("ressenti_faisabilite", "contre", "indifferent", "pour")
ressenti_conflits = Classe_classification("ressenti_conflits", "peu probable", "moyennement probable", "probable", "tres probable" )
couleur_eau = Classe_classification("couleur de l'eau", "trouble", "claire")
odeur_eau = Classe_classification("odeur de l'eau", "pas d'odeur", "odeur", "forte odeur")
praticabilite = Classe_classification("practicabilite", "impraticable", "peu praticable", "praticable", "tres praticable")

## Classes floues ou l'entrée est soit nette (auquel cas elle est fuzzifiée) soit floues auquel cas elle est évaluée par un calcul de possibilté

saison = Classe("saison")
saison_opti0 = IFT(0,0,2,3,1, "optimale")
saison_seche = IFT(2,3,5,6,1,"seche")
saison_opti = IFT(4,5,6,7,1,"optimale")
saison_pluie = IFT(5,6,9,10, 1, "pluie")
saison_opti2 = IFT(9,10,13,13,1,"optimale")
saison.ajouter(saison_seche, saison_pluie, saison_opti, saison_opti2, saison_opti0)
#saison.plot()




difference_distance = Classe("difference distance")
diff_dist_faible = IFT(0, 0, 200, 900, 1, "faible")
diff_dist_moyenne = IFT(300, 900, 1000, 1600, 1, "moyenne")
diff_dist_elevee = IFT(1000, 1600, 1800, 1800, 1, "elevee")
difference_distance.ajouter(diff_dist_faible, diff_dist_moyenne, diff_dist_elevee)
#plt.title("Différence distance") # Permet d'afficher les différents IFTs constituants la classe floues
#difference_distance.plot()

difference_altitude = Classe("difference altitude")
diff_alt_faible = IFT(0, 0, 1000, 1500, 1, "faible")
diff_alt_moyenne = IFT(1000, 1500, 2500, 3000, 1, "moyenne")
diff_alt_elevee = IFT(2500, 3000, 4500, 4500, 1, "elevee")
difference_altitude.ajouter(diff_alt_faible, diff_alt_moyenne, diff_alt_elevee)
#plt.title("Différence altitude")
#difference_altitude.plot()

altitude_cumulee = Classe("altitude cumulee totale")
alt_cum_faible = IFT(0, 0, 5000, 7000, 1, "faible")
alt_cum_moyenne = IFT(5000, 7000, 10000, 15000, 1, "moyenne")
alt_cum_elevee = IFT(10000, 15000, 20000, 20000, 1, "elevee")
altitude_cumulee.ajouter(alt_cum_faible,alt_cum_moyenne, alt_cum_elevee)
#plt.title("Altitude cumulée")
#altitude_cumulee.plot()

proportion_sources_besoins = Classe("proportion entre les sources et les besoins")
src_besoin_trop_peu = IFT(0, 0, 0.4, 0.7, 1, "beaucoup trop peu" )
src_besoin_peu = IFT(0.4, 0.7,0.9, 1, 1, "peu" )
src_besoin_assez = IFT(0.9, 1, 1.2, 1.4, 1, "assez" )
src_besoin_trop = IFT(1.2, 1.4,4, 4, 1, "trop")
proportion_sources_besoins.ajouter(src_besoin_trop_peu, src_besoin_peu, src_besoin_assez, src_besoin_trop)
#proportion_sources_besoins.plot()

prop_debit_besoin = Classe("proportion entre le debit de la source et le besoin du village")
prop_trop_faible = IFT(0,0,  0.8, 1,1, "trop faible")
prop_satisf = IFT(0.8, 1, 1.2, 3, 1, "satisfaisant")
prop_trop_elevee = IFT(1.2, 3, 4, 4,1,  "trop elevee")
prop_debit_besoin.ajouter(prop_trop_faible, prop_satisf, prop_trop_elevee)
#plt.title("Proportion débit/besoin")
#prop_debit_besoin.plot()



score_village_src = Classe("Score Village/Source")
sc_village_tresmauvais = IFT(0, 0, 15, 18, 1, "tres mauvais")
sc_village_mauvais = IFT(15, 18,30,35, 1, "mauvais")
sc_village_passable = IFT(27, 35,47, 52, 1, "passable")
sc_village_bon = IFT(47, 52, 63,70, 1, "bon")
sc_village_tresbon = IFT(63,70,80,89, 1, "tres bon")
sc_village_excellent = IFT(80,89,100, 100, 1, "excellent")
score_village_src.ajouter(sc_village_excellent, sc_village_tresbon, sc_village_bon, sc_village_passable,sc_village_mauvais,sc_village_tresmauvais )
#plt.title("score village/source")
#score_village_src.plot()