import Lambda
LT = Lambda.LambdaTerm

def Int2Church(n):
    """n is een int
    Zet een int om in een Church Numeral
    Deze methode is recursief geimplementeerd"""
    
    a = LT("(#f.(#x.x))")
    for i in range(n):
      a.BruijnIndex[1].insert(1,2)

    return a

def Church2Int(n):
    """Zet een Church Numeral om in een int"""
    res = 0
    i = 1
    while n.BruijnIndex[1][i]==2:
        res+=1
        i+=1
    return res

zero = LT("(#f.(#x.x))") #Church Numeral 0
succ = LT("(#f.(#x.(#n.xfxn))") #De successor functie
add = LT("(#n.(#m.(#f.(#x.mfnfx)))))") #Optellen van n en m
mul = LT("(#n.(#m.(#f.(#x.nmfx)))))") #Vermenigvuldigen van n en m 

b = Int2Church(5)
c = Int2Church(1)
print(b)
print(c)
d = add|b|c
print(d)
e = mul|b|c
print(e)
