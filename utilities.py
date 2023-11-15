class IFT():
    def __init__(self, a, b, c, d, h, label):
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
            return self.h
        
    def __str__(self):
        return f" {label} : ({a}, {b}, {c}, {d})"
    
        
        
        
        
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
        for ift in valeurs:
            appartenance[ift.label] = ift.v(x)
        return appartenance

            
            
            