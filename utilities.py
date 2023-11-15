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
    
        