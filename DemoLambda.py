"""Om dit te gebruiken moet je eerst lambda op je computer hebben staan"""
import Lambda
LT = Lambda.LambdaTerm

"""De beginvariabele die 0 representeert"""
zero= LT("(#f.(#x.x)))")

def Succ(n):
    """n is een lambdaterm
    De successor functie."""
    
    a = LT("(#f.(#x.f(N(f)(x))))")
    a('N',str(n))
    return ~a

def Church2Int(n):
    """n is een lambdaterm
    Zet een Church Numeral om in een int"""
    
    a = LT("(N(#x.x+1)(0)))")
    a('N',str(n))
    return ~a

def Int2Church(n):
    """n is een int
    Zet een int om in een Church Numeral
    Deze methode is recursief geimplementeerd"""
    
    a = LT("(#f.(#x.((Q)(f)(x))))")
    if n==0:
        return zero
    else:
        N = Int2Church(n-1)
        a('Q',str(N))
        return ~a

def Add(m,n):
    """m,n zijn lambdatermen.
    Optellen van twee Church Numerals"""
    
    a = LT("(#f(#x.M(N(f(x))))))")
    a('N',str(n))
    a('M',str(m))
    return ~a

one = Int2Church(1)
three = Int2Church(3)
