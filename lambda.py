#!/usr/bin/env python3

GlobalAlphabet = [  chr(955),'a','b','c','d','e','f']

def FindAlphabet(string):
  result=[]
  for i in range(len(string)):
    if string[i]=='#':
      result += string[i+1]
  
  for i in string:
    found = False
    if (i=='#'):
      found = True
    if (i=='('):
      found = True
    if (i==')'):
      found = True
    if (i=='.'):
      found = True
    for j in result:
      if i==j:
        found = True
    if found==False:
      result += i
  
  result2 = [chr(955)]
  for i in result:
    result2 += i

  return result2

  







def Replace(target,goal,data):
  for i in range(len(data)):
    #print(i)
    if isinstance(data[i],list):
      Replace(target,goal,data[i])
    elif data[i]==target:
      data[i] = goal

def FindNumber(target,data):
  number = 0 
  for i in data:
    #print(i)
    if isinstance(i,list):
      number += FindNumber(target,i)
    elif i==target:
      number += 1
  return number


def Text(data,alphabet):
  
  
  global lambdaC 
  lambdaC = 1

  def Text2(data,alphabet,scope=[]):
    string = ''
    global lambdaC 

    for i in data:

      #print(scope)
      scope2=scope.copy()

      if isinstance(i,list):
        string += '('
        string += Text2(i,alphabet,scope2)
        string += ')'
      elif i==0:
        string += alphabet[0]
        string += alphabet[lambdaC]
        string += '.'
        scope.append(lambdaC)
        lambdaC += 1
      elif i<=len(scope):
        string += alphabet[scope[-i]]
      elif i>len(scope):
        string += alphabet[i]
    
  
  
    return string

  return Text2(data,alphabet)


      
      


class LambdaTerm:
    """Abstract Base Class for lambda terms."""
    BruijnIndex = None
    LambdaTotal = None
    PreferedAlphabet = None
    InputString = None



    def __init__(self):
      return None
      


    def fromstring(self,string):
      self.BruijnIndex= []

      self.PreferedAlphabet = FindAlphabet(string)
      self.LambdaTotal = 0
      Depth = 0
      Temp = self.BruijnIndex
      BoundVariables = []
      FreeVariable = []
      Index = []
      LambdaCount = []
      
      i = 0
      while i<len(string):
        #print(string[i])
        #print(Depth)
        #print(Temp)
        #print(Index)
        #print(self.BruijnIndex)
        #print(BoundVariables)
        #print(FreeVariable)
        #print(LambdaCount)


        if string[i]=='(':
          if Depth==0:
            Index.append(0)
            LambdaCount.append(0)
            Depth +=1
          else:
            Index.append(0)
            
            LambdaCount.append(LambdaCount[Index[Depth]])
            Temp.append([])
            Temp = Temp[Index[Depth-1]]
            Depth +=1

        elif string[i]==')':
          if Depth==1:
            i=10000
          else:
            Index.pop(-1)
            Index[Depth-2] += 1
            Temp = self.BruijnIndex
            
            #print(Index)
            #print(Depth)
            
            for k in range(Depth-2):
              Temp = Temp[Index[k]]

            for k in range(LambdaCount[Depth-1]-LambdaCount[Depth-2]):
              BoundVariables.pop()

            LambdaCount.pop()
            Depth -=1

        elif string[i]=='#':
          Temp.append(0)
          BoundVariables.append(string[i+1])
          
          i +=2
          Index[Depth-1] += 1
          LambdaCount[Depth-1] += 1

        else:
          found = False
          
          for j in range(len(BoundVariables)):
            if BoundVariables[j]==string[i]:
              found = True
              Temp.append(LambdaCount[Depth-1]-j)
              Index[Depth-1] += 1

          for j in range(len(FreeVariable)):
            if FreeVariable[j]==string[i]:
              found = True
              Temp.append(FreeVariable[j])
              Index[Depth-1] += 1

          if found==False:
            FreeVariable.append(string[i])
            Temp.append(string[i])
            Index[Depth-1] += 1
                  
        i += 1
      
      self.LambdaTotal = FindNumber(0,self.BruijnIndex)
      Free = self.LambdaTotal+1
      for i in FreeVariable:
        Replace(i,Free,self.BruijnIndex)
        Free += 1
      
      print(self.BruijnIndex)


    def __str__(self): 
      
      
      string = '('
      if self.PreferedAlphabet==None:
        string += Text(self.BruijnIndex,GlobalAlphabet)
      else:
        string += Text(self.BruijnIndex,self.PreferedAlphabet)
      
      
      
      string += ')'

      
      return string 










    def substitute(self, target, goal):
      Replace(target,goal,self.PreferedAlphabet)

    def reduce(self):
        """Beta-reduce."""
        raise NotImplementedError


class Variable(LambdaTerm):
    """Represents a variable."""
    

    def __init__(self, symbol, ): 
      self.symbol = symbol
      self.BruijnIndex = [1]
    

    def __repr__(self): 
    
      raise NotImplementedError

    def __str__(self): 
      return '(' + self.symbol + ')'
      
    def substitute(self, newsymbol): 
      self.symbol = newsymbol
      


class Abstraction(LambdaTerm):
    """Represents a lambda term of the form (?x.M)."""

    def __init__(self, variable, body): 
      self.BruijnIndex=[]
      
      for i in variable:
        self.BruijnIndex.append(0)
      
      for j in body:
        found = False
        FreeVariable = []


        for i in range(len(variable)):
          if variable[i]==j:
            found = True
            self.BruijnIndex.append(len(variable)-i)

        for i in range(len(FreeVariable)):
          if FreeVariable[i]==j:
            found = True
            self.BruijnIndex.append(len(variable)+i)

        if found==False:
          FreeVariable += j
          self.BruijnIndex.append(len(variable)+len(FreeVariable))
          

      
    def __repr__(self): raise NotImplementedError

    def __str__(self): 
      string = '('
      lambdacount = 0
      for i in self.BruijnIndex:

        if i==0:
          string += GlobalAlphabet[i]
          lambdacount += 1
          string += GlobalAlphabet[lambdacount]
          string += '.'

        if i>lambdacount:
          string += GlobalAlphabet[i]
        elif i>0:
          string += GlobalAlphabet[lambdacount+1-i]

      string += ')'
      return string

    def __call__(self, argument): raise NotImplementedError



class Application(LambdaTerm):
    """Represents a lambda term of the form (M N)."""

    def __init__(self, function, argument): raise NotImplementedError

    def __repr__(self): raise NotImplementedError

    def __str__(self): raise NotImplementedError

    def reduce(self): raise NotImplementedError



a = Variable('x')
b = Abstraction('xy','zxyz')
c = LambdaTerm()
inp1 = input()
c.fromstring(inp1)
print(c)
c.substitute('u','&')
print(c)


(#x.#y.zx(#u.ux)(#w.wy))

