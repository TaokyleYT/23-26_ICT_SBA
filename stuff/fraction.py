import math


class Fraction():
    def __init__(self, numerator: int, denominator: int, 
                 *, ignore_zero_devision_err: bool = False):
        if (not isinstance(numerator, int) or 
            not isinstance(denominator, int)):
            raise TypeError("numerator and denominator must be int")
        if not isinstance(ignore_zero_devision_err, bool):
            raise TypeError("ignore_zero_devision_err must be bool")
        self.numerator: int = numerator
        self.denominator: int = denominator
        self.ignore_zero_devision_err: bool = ignore_zero_devision_err
        self.simplify()

    def simplify(self):
        if self.numerator == 0:
            self.denominator = 1
            return
        if self.denominator == 0:
            if self.ignore_zero_devision_err:
                return
            raise ZeroDivisionError("denominator cannot be 0")
        if self.denominator < 0:
            self.numerator *= -1
            self.denominator *= -1
        greatest_common_divisor = math.gcd(self.numerator, self.denominator)
        self.numerator //= greatest_common_divisor
        self.denominator //= greatest_common_divisor
        return

    def invert(self):
        return Fraction(self.denominator, self.numerator)

    def __neg__(self):
        return Fraction(-self.numerator, self.denominator)
        
    def __add__(self, other):
        if isinstance(other, int):
            return Fraction(self.numerator+self.denominator*other, self.denominator)
        if isinstance(other, Fraction):
            return Fraction((self.numerator*other.denominator
                             +self.denominator*other.numerator), 
                            (self.denominator*other.denominator),
                            ignore_zero_devision_err=(
                                self.ignore_zero_devision_err or 
                                other.ignore_zero_devision_err)
                           )
        raise TypeError("other must be in type <int> or <Fraction>")

    def __sub__(self, other):
        return self.__add__(-other)
        
    def __mul__(self, other):
        if isinstance(other, int):
            return Fraction(self.numerator*other, self.denominator)
        if isinstance(other, Fraction):
            return Fraction(self.numerator*other.numerator, 
                            self.denominator*other.denominator, 
                            ignore_zero_devision_err=(
                                self.ignore_zero_devision_err or 
                                other.ignore_zero_devision_err)
                           )        
        raise TypeError("other must be in type <int> or <Fraction>")

    def __truediv__(self, other):
        if isinstance(other, int):
            return self.__mul__(Fraction(1, other))
        if isinstance(other, Fraction):
            return self.__mul__(other.invert())
        raise TypeError("other must be in type <int> or <Fraction>")

    def __repr__(self) -> str:
        if self.denominator == 1:
            return str(self.numerator)
        return f"{self.numerator}/{self.denominator}"

    def __str__(self) -> str:
        return "<Fraction> object at " + str(id(self)) + " with value: " + str(self.numerator) + (("/" + str(self.denominator)) if self.denominator != 1 else "")

if __name__ == "__main__":
    f1 = Fraction(4, 2)
    f2 = Fraction(1, 3)
    f3 = f1 + f2
    f4 = f1 - f2
    f5 = f1 * f2
    f6 = f1 / f2
    print(f"{f1 = }\nf1: {f1}\n{f2 = }\nf2: {f2}\n\n+ {f3 = }\n  f3: {f3}\n- {f4 = }\n  f4: {f4}\n* {f5 = }\n  f5: {f5}\n/ {f6 = }\n  f6: {f6}\n")

    print("- - -")
    f0div1 = Fraction(3, 0, ignore_zero_devision_err=True)
    print("f0div1: " + str(f0div1) + "\n")
    
    f0div21 = f0div1 * Fraction(3, 0, ignore_zero_devision_err=True)
    print("f0div21 = f0div1 * Fraction(3, 0, ignore_zero_devision_err=True)" + "\n  " + f"f0div21: {f0div21}\n")
    
    try:
        f0div22 = f0div1 * 3
    except ZeroDivisionError as e:
        print("f0div22 = f0div1 * 3" + "\n>>> " + str(e) + "\n")
        
    f0div31 = f0div1 + Fraction(8, 5, ignore_zero_devision_err=True)
    print("f0div31 = f0div1 + Fraction(8, 5, ignore_zero_devision_err=True)" + "\n  " + f"f0div31: {f0div31}\n")
    try:
        f0div32 = f0div1 + 5
    except ZeroDivisionError as e:
        print("f0div32 = f0div1 + 5" + "\n>>> " + str(e) + "\n")

command = input()
if command in ("add", "plus"):
    sign = '+'
elif command in ("sub", "minus"):
    sign = '-'
elif command in ("mul", "times"):
    sign = '*'
elif command in ("div", "over"):
    sign = '/'
else:
    print("Invalid command")
    exit()
    
    
temp = input("fraction 1 (format n/d): ")
f1 = Fraction(*map(int, temp.split("/")))
temp = input("fraction 2 (format n/d): ")
f2 = Fraction(*map(int, temp.split("/")))
print(f1.__repr__(), sign, f2.__repr__(), '=', (eval("f1"+sign+"f2")).__repr__())