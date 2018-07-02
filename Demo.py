#!/usr/bin/env python3



import Lambda

LT = Lambda.LambdaTerm

"""De beginvariabele die 0 representeert"""

def Int2Church(n):
    """n is een int
    Zet een int om in een Church Numeral
    Deze methode is recursief geimplementeerd"""
    
    a = LT("(#f.(#x.x))")
    for i in range(n):
      a.BruijnIndex[1].insert(1,2)

    return a

zero = LT("(#f.(#x.x))")
succ = LT("(#f.(#x.(#n.xfxn))")
add = LT("(#n.(#m.(#f.(#x.mfnfx)))))")
mul = LT("(#n.(#m.(#f.(#x.nmfx)))))")
b = Int2Church(5)
c = Int2Church(1)
print(b)
print(c)
d = add|b|c
print(d)
e = mul|b|c
print(e)
print(Int2Church(25))
