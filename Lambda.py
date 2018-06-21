

GlobalAlphabet = [  chr(955),'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

def FindAlphabet(string):
  result=[] 

  # Hier vind de functie de gebonden variablen 
  for i in range(len(string)):
    if string[i]=='#':
      result += string[i+1]
  
  # Hier halen we alles uit de string behalve dus de vrije variablen.
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
  
  result2 = [chr(955)] # Dit is de eerste letter van het alphabet, meestal de lambda
  
  for i in result:
    result2 += i

  #Het alphabet wat wordt gegeven bestaat dus uit eerst het "lambda" symbol, dan alle 
  #gebonden variablen en dan alle vrije variablen. 
  
  return result2

def Replace(target,goal,data):
  #Deze functie pakt 
  
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
  #print(data)
  #print("printing")
  global lambdaC 
  lambdaC = 1

  def Text2(data,alphabet,scope=[]):
    string = ''
    global lambdaC 
    #print(data)


    for i in data:
      #print(i)

      #print(scope)
      #print(lambdaC)
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

def FindNumber2(target,route,data,depth=0):
  number = 0 
  #print(depth)
  #print(route)
  #print(len(route))

  if depth>=len(route):
    return 1 


  for i in range(route[depth]-1):
    #print(i)
    if isinstance(data[i],list):
      number += FindNumber(target,data[i])
    elif data[i]==target:
      number += 1

  #print(number)    
  return number + FindNumber2(target,route,data,depth+1)
  
def DeepCopy(data,target):
  
  for i in range(len(data)):
    #print(target)
    if isinstance(data[i],list):
      target.append([])
      DeepCopy(data[i],target[i])
    else:
      target.append(data[i])
  
def pop(Route,data):
  temp = data
  for i in range(len(Route)-1):
    temp = temp[Route[i]] 
  temp.pop([Route[-1]])   

def Replace3(Route,Goal,data):
  temp = data
  for i in range(len(Route)-1):
    temp = temp[Route[i]] 
  temp[Route[-1]]=Goal       
        
def Replace2(lowerlimit,upperlimit,add,data):
  #Deze functie pakt 
  
  for i in range(len(data)):
    #print(data[i])
    if isinstance(data[i],list):
      Replace2(lowerlimit,upperlimit,add,data[i])
    else:
      if upperlimit==-1:
        if lowerlimit<data[i]:
          data[i] = data[i] + add
      else:
        if lowerlimit<data[i]<upperlimit:
          data[i] = data[i] + add         

def FindReduce(data,route):
  #print(route)
  
  for i in range(0,len(data)-1):
    if isinstance(data[i],list):
      if i<len(data)-1:
        route.append(i)
        return True
      else:
        route.append(i)
        if FindReduce(data,route):
          return True
        else:
          route.pop()
  
  return False

def FindFirstVariable(first,routes=[],depth=0,scope=[]):
  
  
  #print(routes)
  #print("Fag")

  for i in range(len(first)):
    
    #print(isinstance(i,list))
    scope.append(i)
    #print(scope)

    if isinstance(first[i],list):
      #print("Deepre")
      FindFirstVariable(first[i],routes,depth,scope)

    else:
      if first[i]==0:
        depth += 1
      #print(first[i])
      #print(depth)
      if first[i]==depth:
        routes.append(scope.copy())
    
    scope.pop()
  
  return routes

def DeepCompare(data1,data2):
  Same = True
  #print(data1)
  #print(data2)
  if len(data1)==len(data2):
    for i in range(len(data1)):
      #print(data1[i])
      #print(data2[i])
      if isinstance(data1[i],list):
        if isinstance(data2[i],list):
          Same = DeepCompare(data1[i],data2[i])
        else:
          return False
      else:
        if isinstance(data2[i],list):
          return False
        elif data1[i]!=data2[i]:
          return False
  else:
    return False
  #print("Made it")
  #print(Same)
  return Same        



class LambdaTerm:
    """Abstract Base Class for lambda terms."""
    BruijnIndex = None
    PreferedAlphabet = None


    def __init__(self,data1=None,data2=None):
      if isinstance(data1,str):
        self.fromstring(data1)
      if isinstance(data1,type(self)):
        self.BruijnIndex = []
        DeepCopy(data1.BruijnIndex,self.BruijnIndex)
        self.PreferedAlphabet = data1.PreferedAlphabet.copy()

      if isinstance(data1,list):
        if isinstance(data2,list):
          #print(data1)
          #print(data2)
          self.BruijnIndex = []
          DeepCopy(data1,self.BruijnIndex)
          self.PreferedAlphabet = data2.copy()


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
            
            LambdaCount.append(LambdaCount[Depth-1])
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
      
      #print(self.BruijnIndex)
      #print(self.PreferedAlphabet)

    def __str__(self): 
      #print("printing")
      #print(self.BruijnIndex)

      string = '('
      if self.PreferedAlphabet==None:
        string += Text(self.BruijnIndex,GlobalAlphabet)
      else:
        string += Text(self.BruijnIndex,self.PreferedAlphabet)
      
      
      
      string += ')'

      
      return string 

    def __call__(self, target, goal):
      Replace(target,goal,self.PreferedAlphabet)

    def getAlphabet(self):
      out = self.PreferedAlphabet.copy()
      return out

    def resolveConflict(self):
      CurrentAlphabet = []
      
      for i in range(len(self.PreferedAlphabet)):
        found = False
        for j in CurrentAlphabet:
          if self.PreferedAlphabet[i]==j:
            found = True
        if found:
          j=0
          while GlobalAlphabet[j] in CurrentAlphabet:
            j += 1  
          self.PreferedAlphabet[i]=GlobalAlphabet[j]
        CurrentAlphabet += self.PreferedAlphabet[i]

    def reduce(self):
      #print(self.BruijnIndex)
      stop=0
      while self.reduceStep()==False:
        stop += 1
        if stop>20:
          break
        #print(self)
        #print(self.BruijnIndex)
        None

    def __invert__(self):
      new = LambdaTerm(self)
      new.reduce()
      return new

    def __or__(self,other):
      #print(self)
      #print(other)
      
      if isinstance(other,type(self)):

        one = []
        DeepCopy(self.BruijnIndex,one)
        oneAlphabet = self.PreferedAlphabet.copy()

        two = []
        DeepCopy(other.BruijnIndex,two)
        twoAlphabet = other.PreferedAlphabet.copy()

        oneFree = FindNumber(0,one)
        twoFree = FindNumber(0,two)

        #print(oneAlphabet)
        #print(twoAlphabet)
        newAlphabet = oneAlphabet[:oneFree+1].copy()
        #print(newAlphabet)
        newAlphabet.extend(twoAlphabet[1:twoFree+1])
        #print(newAlphabet)
        newAlphabet.extend(oneAlphabet[oneFree+1:])
        #print(newAlphabet)
        newAlphabet.extend(twoAlphabet[twoFree+1:])
        #print(newAlphabet)
        
        for i in range(len(newAlphabet[:oneFree+twoFree+1])):
          for j in range(len(newAlphabet[i+1:])):
            
            if newAlphabet[i]==newAlphabet[j+i+1]:
              q=0
              while GlobalAlphabet[q] in newAlphabet:
                q += 1
              if j+i+1<(oneFree+twoFree+1):  
                newAlphabet[j+i+1]=GlobalAlphabet[q]
              else:
                newAlphabet[i]=GlobalAlphabet[q]
        #print(newAlphabet)

        Replace2(oneFree,-1,twoFree,one)
        
        new = []

        if one[0]==0:
          new.append(one)
        else:
          new.extend(one)

        #print(one)
        #print(two)
        Replace2(twoFree,-1,len(oneAlphabet)-1,two)
        #print(two)

        if two[0]==0:
          new.append(two)
        else:
          new.extend(two)
        #print(new)
  
        pop = []
        for i in range(1,len(newAlphabet[oneFree+twoFree+1:])):
          for j in range(i+1,len(newAlphabet[oneFree+twoFree+1:])+1):
            #print(newAlphabet[oneFree+twoFree+i])

            if newAlphabet[oneFree+twoFree+i]==newAlphabet[oneFree+twoFree+j]:
              
              Replace(j+oneFree+twoFree,i+oneFree+twoFree,new)
              #Replace2(j+oneFree+twoFree,-1,-1,new)
              pop += [j+oneFree+twoFree]
              #print(new)

        pop.reverse()
        #print(pop)
        #print(new)
        #Replace2(4,-1,-1,one)
        
        for i in pop:
          #print(i)
          newAlphabet.pop(i)
          Replace2(i,-1,-1,new)
        
        #print(new)
        #print(newAlphabet)

        return LambdaTerm(new,newAlphabet)

    
      else:
        raise NotImplementedError  

    def __eq__(self,other):
      if isinstance(other,type(self)):
        #print(DeepCompare(self.BruijnIndex,other.BruijnIndex))
        if DeepCompare(self.BruijnIndex,other.BruijnIndex):
          Free = FindNumber(0,self.BruijnIndex)
          #print(self.PreferedAlphabet[Free+1:])
          #print(other.PreferedAlphabet[Free+1:])
          for i in range(len(self.PreferedAlphabet[Free+1:])):
            if self.PreferedAlphabet[Free+1+i]!=other.PreferedAlphabet[Free+1+i]:
              return False
          return True
        else:
          return False
      else:
        return False




    def reduceStep(self):
        """Beta-reduce."""
        route = []
        first = []
        second = []
        upper = []
        Free3 = FindNumber(0,self.BruijnIndex)

        #print(self.BruijnIndex)
        #print(self.PreferedAlphabet)

        #print(Free3)
        if FindReduce(self.BruijnIndex,route):
          #print(route)

          #print(upper)
          DeepCopy(self.BruijnIndex,upper)
          #print(upper)



          for i in range(len(route)-1):
            #print(upper)
            upper = upper[i]
          
          
          second = upper[route[-1]+1]
          first = upper[route[-1]]
          
          if isinstance(second,int):
            second = [second]

          #print(self.BruijnIndex)
          #print(first)
          #print(second)
        else:
          #print("Already reduced")
          return True
        

        #print(self.BruijnIndex)

        Replacable = [] 
        FindFirstVariable(first.copy(),Replacable)
        #print("Replacables")
        #print(Replacable)
        

        #print(self.BruijnIndex)

        Free = FindNumber(0,first)

        new = first.copy()
        #print(new)
        
        
        Replace2(Free,Free3,-1,new)
        #print(new)



        Free2 = FindNumber(0,second)
        

        for i in Replacable:
          Buffer = second.copy()
          Replace2(Free2,Free3,len(i)-1,Buffer)
          #print(Buffer)
          if len(Buffer)==1:
            Replace3(i,Buffer[0],new)
          else:
            Replace3(i,Buffer,new)
        #print(new)

        new.pop(0)
        #print(new)

        letter = FindNumber2(0,route,self.BruijnIndex)


        upper=self.BruijnIndex
        for i in range(len(route)-1):
          #print(upper)
          upper = upper[i]

        parathesis = True
        
        if new[0]!=0:
          parathesis = False
        #print(self.BruijnIndex)
        #print("_______")

        upper.pop(route[-1]+1)
        upper.pop(route[-1])
        
        #if len(upper)>=route[-1]+1:
        #  parathesis=True
        #else:
        #  parathesis=False
        #upper[route[-1]]=new
       # print(self.BruijnIndex)
        #print(new)

        if parathesis:
          upper.insert(route[-1],new)
        else:
          for i in range(len(new)):
            upper.insert(route[-1]+i,new[i])

        #self.PreferedAlphabet.pop(letter)

        #Replace2(Free3,-1,self.BruijnIndex)
        Free4 = FindNumber(0,self.BruijnIndex)
        #print(Free4)

        if Free4>Free3:
          for i in range(Free4-Free3):
            q=0
            while GlobalAlphabet[q] in self.PreferedAlphabet:
              q += 1
            self.PreferedAlphabet.insert(Free3+i+1,GlobalAlphabet[q])
            Replace2(Free3+i,-1,1,self.BruijnIndex)




        #print(self.BruijnIndex)
        #print(self.PreferedAlphabet)
        return False


