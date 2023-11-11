def permRows(t):
    i=0
    j=len(t)-1
    p=[]
    while i<j:
        p.append(t[i])
        p.append(t[j])
        i+=1
        j-=1
    if i==j:
        p.append(t[i])
    return p

def revPermRows(t):
    i=0
    p=[]
    while i<len(t):
        p.append(t[i])
        i+=2
    i=len(t)-1
    if len(t)%2!=0:
        i-=1
    while i>0:
        p.append(t[i])
        i-=2
    return p

def sf(t):
    p=[]
    n=0
    for i in t:
        p.append(i[n:]+i[:n])
        n+=1
        if n>=len(i):
            n=0
    return p

def isf(t):
    p=[]
    n=0
    x=len(t[0])
    for i in t:
        p.append(i[x-n:]+i[:x-n])
        n+=1
        if n>=len(i):
            n=0
    return p

        

