from matplotlib import pyplot as plt

class IFT():
    def __init__(self, a, b, c, d, h, label=""):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.h = h
        self.label = label

        
    def v(self, x):
        if x < self.a:
            return 0
        if x >= self.a and x <= self.b:
            return self.h * ((x - self.a)/(self.b - self.a))
        if x >= self.b and x <= self.c:
            return self.h
        if x >= self.c and x <= self.d:
            return self.h * ((self.d - x)/(self.d - self.c))
        if x > self.d:
            return 0

    def __str__(self):
        return f" {self.label} : ({self.a}, {self.b}, {self.c}, {self.d})"

if __name__ == "__main__":
    vieux = IFT(35, 40, 47, 53, 0.93)
    Valeurs = [*range (20, 100, 1)]

    New = [ vieux.v(i) for i in Valeurs]
    plt.plot(Valeurs, New)
    plt.show()


