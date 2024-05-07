class Fraction:
    def __init__(self, nume, denom):
        assert nume > 0 and denom > 0
        self.nume = nume
        self.denom = denom
        self.simplify()
    def __str__(self):
        return  f"{self.nume}/{self.denom}"
    def __repr__(self):
        return f"Fraction({self.nume},{self.denom})"
    def __mul__(self, other):
        return Fraction(self.nume * other.nume, self.denom * other.denom)
    def __add__(self, other):
        return Fraction(self.nume * other.denom + other.nume * self.denom, other.denom * self.denom)
    def simplify(self): 
        cd = gcd(self.nume, self.denom)
        self.nume = self.nume//cd
        self.denom = self.denom//cd 


def gcd(a: int, b: int) -> int:
    if b == 0:
        return abs(a)
    return gcd(b, a%b)