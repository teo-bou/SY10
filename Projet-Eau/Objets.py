from flou_import import *
class Village():
    def __init__(self, x, y, nb_habitants, ressenti, infrastructure):
        self.x = x
        self.y = y
        self.nb_habitants = nb_habitants
        self.ressenti = ressenti
        self.infrastructure = infrastructure



    def eval_besoin(self):
        self.besoin = self.nb_habitants*3600

class Source():
    def __init__(self, x, y, couleur, debit, odeur):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.odeur = odeur
        self.debit = debit

