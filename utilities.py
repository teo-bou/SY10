from matplotlib import pyplot as plt


class intervalle():
    def __init__(self, a=None, b=None):
        self.a = a
        self.b = b

    def __str__(self):
        if self.a == None:
            return "Intervalle vide"
        else:
            return f"[{self.a},{self.b}]"


class IFT():
    def __init__(self, a, b, c, d, h, label):

        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.h = h
        self.label = label

    def alpha_coupe(self, alpha):
        if alpha > 0 and alpha <= self.h:
            A1 = ((self.b - self.a) * (alpha / self.h) + self.a)
            A2 = (-(self.d - self.c) * (alpha / self.h) + self.d)
            return intervalle(A1, A2)
        else:
            return intervalle()

    def v(self, x):
        if x < self.a:
            return 0
        if x >= self.a and x <= self.b:
            return self.h * ((x - self.a) / (self.b - self.a))
        if x >= self.b and x <= self.c:
            return self.h

        if x >= self.c and x <= self.d:
            return self.h * ((self.d - x) / (self.d - self.c))
        if x > self.d:
            return 0

    def __str__(self):
        return f" {self.label} : ({self.a}, {self.b}, {self.c}, {self.d})"

    def mul(self, alpha):
        a = alpha * self.a
        b = alpha * self.b
        c = alpha * self.c
        d = alpha * self.d
        return IFT(a,b,c,d,self.h, self.label)

    def add(self, ift):
        if self.h > ift.h:
            ift1 = self.tr(ift.h)
            return IFT(ift1.a + ift.a, ift1.b + ift.b, ift1.c + ift.c, ift1.d + ift.d, ift.h, self.label)
        else:
            ift1 = self
            ift = ift.tr(self.h)
            return IFT(ift1.a + ift.a, ift1.b + ift.b, ift1.c + ift.c, ift1.d + ift.d, ift.h, self.label)

    # Mult à faire et diviser
    def tr(self, h):
        if h > self.h:
            raise ValueError("H est au dessus de la hauteur de l'intervalle")
        elif h == self.h:
            return self
        else:
            b = h*(self.b-self.a)/self.h+self.a
            c = - h*(self.d - self.c)/self.h +self.d
            return IFT(self.a,b,c,self.d, h,self.label)




class Classe():
    def __init__(self, label):
        self.label = label
        self.classes = []
        self.valeurs = []

    def add(self, ift):
        self.valeurs.append[ift]
        self.classes.append[ift.label]

    def v(self, x):
        appartenance = {}
        for ift in self.valeurs:
            appartenance[ift.label] = ift.v(x)
        return appartenance


class NFT(IFT):
    def __init__(self, a, b, c, h, label):
        IFT.__init__(self, a, b, b, c, h, label)


if __name__ == "__main__":
    vieux = NFT(35, 40,45, 0.93, "vieux")
    vieux2 = NFT(24, 30, 37, 0.4, "vieux")
    Valeurs = list(range(20, 100))
    New1 = [vieux.v(i) for i in Valeurs]
    New2 = [vieux2.v(i) for i in Valeurs]
    vieux = vieux.add(vieux2)


    New = [vieux.v(i) for i in Valeurs]

    plt.plot(Valeurs, New)
    plt.plot(Valeurs, New1)
    plt.plot(Valeurs, New2)
    plt.show()

    print(vieux.alpha_coupe(0.98))

    vieux = NFT(35, 40, 50, 1, "vieuxNFT")
    Valeurs = list(range(20, 100))

    New = [vieux.v(i) for i in Valeurs]
    plt.plot(Valeurs, New)
    plt.show()


