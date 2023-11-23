from flou_import import *
class Village():
    def __init__(self, x, y, nb_habitants, ressenti, infrastructure):
        self.x = x
        self.y = y
        self.nb_habitants = nb_habitants
        self.ressenti = ressenti
        self.infrastructure = infrastructure
        self.besoin = self.eval_besoin()
    def eval_besoin_infra(self):
        infrastructure_dico_fixe = {"hopital":NFT(1625, 2500, 3000, 1, "hopital"), "gouvernement": IFT(325, 500, 1000, 1300, 1, "gouvernement")}
        infrastructure_dico_variable = {"hopital": NFT(325, 500, 750, 1, "hopital"), "ecole": NFT(6.5,10, 15, 1, "ecole")}
        infrastructure_besoin = NFT(0,0,0,1,"besoin")
        for key, value in self.infrastructure.items():
            if key in infrastructure_dico_fixe:
                infrastructure_besoin = infrastructure_besoin + infrastructure_dico_fixe[key]*value
            if key in infrastructure_dico_variable:
                infrastructure_besoin = infrastructure_besoin + (infrastructure_dico_variable[key]*self.nb_habitants/4)*value
        return infrastructure_besoin

    def eval_besoin(self):
        self.besoin = self.nb_habitants * 30
        self.besoin_infra = self.eval_besoin_infra()
        resultat = (self.besoin + self.besoin_infra)
        resultat.label = "besoin"
        return resultat

    def __str__(self):
        return f" nb hab ≈{(self.nb_habitants.b + self.nb_habitants.c)/2} | {self.ressenti} {self.infrastructure}| besoin : {self.besoin} "



class Source():
    def __init__(self, x, y, couleur, debit, odeur):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.odeur = odeur
        self.debit = debit


def CAF2(village, source):
    besoin = village.besoin
    debit = source.debit
    ift = debit*86400/besoin
    ift.label = "prop debit/besoin"
    print(ift)
    print(prop_debit_besoin.possibilite(ift.poly()))
    return prop_debit_besoin.possibilite(ift.poly())


ZZ = Village(23,36,NFT(1,2,3,1,'hab'),ressenti.v(0.2,1),{})
print("Le village ZZ",ZZ)
print(ZZ.besoin)

S = Source(20,30,couleur_eau.v(0.2,1),NFT(1,2,3,1,'debit')*30, odeur_eau.v(0,0,0.2))

CAF2(ZZ, S)