# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 01:09:29 2017

@author: yanbaliang
"""
import sys
verifytext=sys.argv[1]

import math
"""import the model file"""
nbModel={}
prior_T=1
prior_D=1
prior_P=1
prior_N=1
with open("nbmodel.txt") as input_model:
    input_line=input_model.readlines()
    prior_Prob=input_line[0].split()
    prior_T=math.log10(float(prior_Prob[1]))
    prior_D=math.log10(float(prior_Prob[2]))
    prior_P=math.log10(float(prior_Prob[3]))
    prior_N=math.log10(float(prior_Prob[4]))
    for line in input_line[1:]:
        elements=line.split()
        nbModel[elements[0]]=elements[1:]
        #print(elements[0]+str(nbModel[elements[0]]))

"""classifier the test file"""
test={} #dict store all test reviews
with open(verifytext) as input_test:  # read all test reviews
    test_input=input_test.readlines()
    for single_test in test_input:
        key=single_test[0:20]
        comment=single_test[21:]
        test[key]=comment

"""process the reviews one by one, and store in a dict"""
output={}
for reviewKey in test.keys():
    review=test[reviewKey]
    reviewWords=review.split()
    Prob_T=prior_T
    Prob_D=prior_D
    Prob_P=prior_P
    Prob_N=prior_N
    for word in reviewWords:
        word=word.lower()
        if word in nbModel:
            Prob_T+=math.log10(float(nbModel.get(word)[0]))
            Prob_D+=math.log10(float(nbModel.get(word)[1]))
            Prob_P+=math.log10(float(nbModel.get(word)[2]))
            Prob_N+=math.log10(float(nbModel.get(word)[3]))
    if Prob_T>=Prob_D:
        output[reviewKey]="truthful"
    else:
        output[reviewKey]="deceptive"
    if Prob_P>=Prob_N:
        output[reviewKey]+=" positive"
    else:
        output[reviewKey]+=" negative"

nboutput=open("nboutput.txt","w")
for key in output.keys():
    nboutput.write(key+" "+output[key]+'\n')
nboutput.close()