from flou_import import *
from Classes import *
from Rules import *
from Objets import *
carte = Carte("test_elevation.png")
carte.carte = cv2.resize(carte.carte, (100,100))
carte.carte_color = cv2.resize(carte.carte_color, (100,100))
carte.l, carte.L = 100,100
ZZ = Village(carte, 0, 0, NFT(10000, 20000, 30000, 1, 'hab'), ressenti.v(0.2, 1),
             {"hopital": 2, "ecole": 3, "gouvernement": 1})

print(carte)
S = Source(carte, 99, 99, couleur_eau.v(0.2, 1), NFT(1, 2, 3, 1, 'debit') * 30, odeur_eau.v(0, 0, 0.2))



def main():
    print(generate_village(Carte("test_elevation.png"), 5))
    carte = "test_elevation.png"
    villages = [
        Village(110, 215, NFT(3500, 40000, 42000, 1, "nb_hab 1"), ressenti.v(0.7, 0.3), {"hopital": 1, "ecole": 2})]
    Score = {}
    carte = Carte("test_elevation.png")


    print("Le village ZZ", ZZ)
    print(ZZ.besoin)

    S = Source(20, 30, couleur_eau.v(0.2, 1), NFT(1, 2, 3, 1, 'debit') * 30, odeur_eau.v(0, 0, 0.2))
    print("dist", carte.distance((10, 1), ZZ))
    print("altc", carte.alt(ZZ))
    result = CAF2(ZZ, S)
    carte.line_alt(ZZ, S)
    print()
    result1 = SIF5.inference(S.couleur, S.odeur)
    print(result1)
    score = SIF7.inference(result, result1)
    print(score)
    print(carte)
from generator_data import *
if __name__ == "__main__":
    main()
