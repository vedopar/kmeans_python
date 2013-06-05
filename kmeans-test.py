'''
Created on 2012-2-6

@author: vedopar
'''

import random
from numpy import array
from scipy.cluster.vq import vq,kmeans

def distortion(node1,node2):
    sum=0
    for i in range(F):
        dis=node1[i]-node2[i]
        sum=sum+dis*dis
    return sum

def assignCode(code_book,node):
    final_dis=-1
    code=-1
    
    for i in range(K):
        temp_dis=distortion(node,code_book[i])
        if final_dis is -1:
            final_dis=temp_dis
            code=i
            continue
        if final_dis >= temp_dis:
            final_dis=temp_dis
            code=i
    return code    

def isEnd(codes,code_book,data):
    new_E=0
    
    for n in range(N):
        new_E=new_E+distortion(data[n],code_book[codes[n]])
    if E[0] is -1:
        E[0]=new_E
        return False
    else:
        if E[0] == new_E:
            return True
        else:
            E[0]=new_E
            return False
        
def updateCodebook(codes,code_book,data):
    count=[0 for x in range(K)]
    new_book=[[0 for x in range(F)] for y in range(N)]
    
    for n in range(N):
        count[codes[n]]=count[codes[n]]+1
        for f in range(F):
            new_book[codes[n]][f]=new_book[codes[n]][f]+data[n][f]
            
    for k in range(K):
        if count[k] is 0:
            continue
        for f in range(F):
                code_book[k][f]=new_book[k][f]/count[k]

def k_means(code_book,data):
    global E
    E=[-1]
    global F
    F=len(code_book[0])
    global N
    N=len(data)
    global K
    K=len(code_book)
    codes=[-1 for x in range(N)]
    
    while not isEnd(codes,code_book,data):
        
        for n in range(N):
            codes[n]=assignCode(code_book,data[n])
        updateCodebook(codes,code_book,data)
    updateCodebook(codes,code_book,data)
        
    return code_book,codes
    
if __name__ == '__main__':
    
    random.seed()
    F=random.randint(1,10)
    N=random.randint(5,50)
    K=int((N+9)/10)
    data=[]
    code_book=[]
    for n in range(N):
        data.append([random.random() for f in range(F)])
    for k in range(K):
        code_book.append([random.random() for f in range(F)])
    
    print "sample code_book:"
    print kmeans(array(data),array(code_book))[0] 
    code_book,codes=k_means(code_book,data)
    print "generated code_book:"
    for i in range(K):
        print code_book[i]
    print "generated codes:"
    for i in range(N/K):
        print codes[i:i+N/K]
    