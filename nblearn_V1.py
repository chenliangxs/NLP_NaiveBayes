# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 17:05:22 2017

@author: yanbaliang
"""
reviewDict={}
labelDict={}

with open("train-text.txt") as reviewFile:
    reviews=reviewFile.readlines()
    for review in reviews:
        key=review[0:20]
        comment=review[21:]
        reviewDict[key]=comment

with open("train-labels.txt") as labelFile:
    labels=labelFile.readlines()
    for label in labels:
        key=label[0:20]
        comment=label[21:]
        labelDict[key]=comment

class Classifier:
    def __init__(self):
        self.T_vocabulary={}
        self.D_vocabulary={}
        self.P_vocabulary={}
        self.N_vocabulary={}

    def addWord(self, dic, word, weight):
        if word in self.dic:
            self.dic[word]=self.dic[word]+weight
        else:
            self.dic[word]=weight

T_vocabulary={}
D_vocabulary={}
P_vocabulary={}
N_vocabulary={}

vocabulary={}
keylist=reviewDict.keys()
for key in keylist:
    review=reviewDict[key]
    wordlist=review.split( )
    T=labelDict[key].find("truthful")
    P=labelDict[key].find("positive")
    for word in wordlist:
        word=word.lower()
        if word.endswith("n't"):
            if T==True:
                self.addWord(T_vocabulary,word,2)
            else:
                self.addWord(D_vocabulary, word, 2)
            if P==True:
                self.addWord(P_vocabulary, word, 2)
            else:
                self.addWord(N_vocabulary, word, 2)
            
        else:
            if word.endswith(".") or word.endswith(",") or word.endswith(";"):
                self.word=word[0:len(word)-1]
            if T==True:
                self.addWord(T_vocabulary, word, 1)
            else:
                self.addWord(D_vocabulary, word, 1)
            if P==True:
                self.addWord(P_vocabulary, word, 1)
            else:
                self.addWord(N_vocabulary, word, 1)
            
output=open("output.txt","w")
outlist=vocabulary.keys()
for key in outlist:
    output.write(key+" ")
    output.write((str)(vocabulary[key]))
    output.write("\n")
#output.write(()reviewDict.items())
output.close()