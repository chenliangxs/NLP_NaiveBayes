# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 17:05:22 2017

@author: yanbaliang
"""

'''
Read input files, put into two dictionary with id as key
'''
import sys
tfile=sys.argv[1]
lfile=sys.argv[2]

reviewDict={}
labelDict={}
with open(tfile) as reviewFile:
    reviews=reviewFile.readlines()
    for review in reviews:
        key=review[0:20]
        comment=review[21:]
        reviewDict[key]=comment

with open(lfile) as labelFile:
    labels=labelFile.readlines()
    for label in labels:
        key=label[0:20]
        comment=label[21:]
        labelDict[key]=comment

"""
build a class of Classifier as a model. Four dictionary to store every word. word is counted as value
"""
class Classifier:
    def __init__(self):
        self.T_vocabulary={}
        self.D_vocabulary={}
        self.P_vocabulary={}
        self.N_vocabulary={}

    def addWord(self, T, P, word, weight):
        if T>=0:
            if word in self.T_vocabulary:
                self.T_vocabulary[word]=self.T_vocabulary[word]+weight
            else:
                self.T_vocabulary[word]=weight
                self.D_vocabulary[word]=0
        else:
            if word in self.D_vocabulary:
                self.D_vocabulary[word]=self.D_vocabulary[word]+weight
            else:
                self.D_vocabulary[word]=weight
                self.T_vocabulary[word]=0
        if P>=0:
            if word in self.P_vocabulary:
                self.P_vocabulary[word]=self.P_vocabulary[word]+weight
            else:
                self.P_vocabulary[word]=weight
                self.N_vocabulary[word]=0
        else:
            if word in self.N_vocabulary:
                self.N_vocabulary[word]=self.N_vocabulary[word]+weight
            else:
                self.N_vocabulary[word]=weight
                self.P_vocabulary[word]=0

    def getT_vocab(self):
        return self.T_vocabulary
       
    def getD_vocab(self):
        return self.D_vocabulary
        
    def getP_vocab(self):
        return self.P_vocabulary
        
    def getN_vocab(self):
        return self.N_vocabulary
        
"""
build up the classifier model from the input file
"""
model=Classifier()
T_count=0 #no. of true words
D_count=0 #no. of deceptive words
P_count=0 #no. of positive words
N_count=0 #no. of negative words
keylist=reviewDict.keys()
for key in keylist:
    review=reviewDict[key]
    wordlist=review.split( )
    T=labelDict[key].find("truthful")
    P=labelDict[key].find("positive")
    if T>=0:
        T_count+=1
    else:
        D_count+=1
    if P>=0:
        P_count+=1
    else:
        N_count+=1
    for word in wordlist:
        word=word.lower()
        #if word=="the":
            #continue
        if word.endswith(",") or word.endswith(".") or word.endswith(":"):
            word=word[:len(word)-1]
        if word.endswith("n't"):
            model.addWord(T, P, word, 1)
        else:
            model.addWord(T, P, word, 1)

"""
calculate the probabilities
"""
total=(float)(len(reviewDict))
P_T=T_count/total #prior probabilities
P_D=D_count/total
P_P=P_count/total
P_N=N_count/total
print((str)(P_T))
print((str)(P_D))
print((str)(P_P))
print((str)(P_N))
vocab_T=model.getT_vocab()
vocab_D=model.getD_vocab()
vocab_P=model.getP_vocab()
vocab_N=model.getN_vocab()
count_T=0 #calculate total tokens in each class and ~class
count_D=0
count_P=0
count_N=0
for key in vocab_T.keys():
    if vocab_T[key]>0:
        count_T+=vocab_T[key]
    if vocab_D[key]>0:
        count_D+=vocab_D[key]
    if vocab_P[key]>0:
        count_P+=vocab_P[key]
    if vocab_N[key]>0:
        count_N+=vocab_N[key]
"""smoothing and calculate poster probabilities"""
B_factor=len(vocab_T)
keylist=list(vocab_T.keys())
for key in keylist:
    vocab_T[key]=1.0*(vocab_T[key]+1)/(count_T+B_factor)
    vocab_D[key]=1.0*(vocab_D[key]+1)/(count_D+B_factor)
    vocab_P[key]=1.0*(vocab_P[key]+1)/(count_P+B_factor)
    vocab_N[key]=1.0*(vocab_N[key]+1)/(count_N+B_factor)
          
output=open("nbmodel.txt","w")
prior_Prob="prior_Prob "+str(P_T)+" "+str(P_D)+" "+str(P_P)+" "+str(P_N)
output.write(prior_Prob+'\n')
for key in keylist:
    P_t=vocab_T[key]
    P_d=vocab_D[key]
    P_p=vocab_P[key]
    P_n=vocab_N[key]
    outline=key + ' '+ str(P_t) + ' '+str(P_d)+' '+str(P_p)+' '+str(P_n)
    #print(outline)
    output.write(outline+'\n')
output.close()