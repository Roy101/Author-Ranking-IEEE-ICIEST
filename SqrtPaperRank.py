import numpy as np
from csv import DictReader
import csv
import networkx as nx
import matplotlib.pyplot as plt
from numpy import linalg as LA
from collections import defaultdict
import math
import pandas as pd


G = nx.DiGraph()


read_obj2=open("F:\Thesis Work\DATA\PaperToPaper.csv","r",encoding="utf8")
csv_dict_reader2 = DictReader(read_obj2)
column_names2 = csv_dict_reader2.fieldnames

"""for line in lines1:
    node=line.strip().split(' ')
    t1=node[0]
    t2=node[1]
    G.add_edge(t1,t2)"""

for row in csv_dict_reader2:
        id=row['id']
        refer=row['references']
        G.add_edge(refer, id)



W = nx.stochastic_graph(G, weight="weight")

N = W.number_of_nodes()
alpha=0.85

print(N)
inDegree=G.in_degree
outDegree=G.out_degree
x = dict.fromkeys(W, 1)

xlast=dict.fromkeys(W,0)
dif=0
for i in x:
    dif=dif+abs(xlast[i]-x[i])
eps=10/N
print(eps)
c=0
while (dif>eps):
    c+=1
    dif = 0
    for i in x:
        xlast[i] = x[i]
    sum = 0
    for n in x: #set of all papers
        if outDegree[n]>0:
            #x[n]=0
            for i in W[n]: #set of papers(i) that cited paper n
                if (inDegree[i] > 0): # inDegree[i] = number of papers cited by paper 'i'
                    # temp=(xlast[i]/inDegree[i])
                    x[n] = (1/N) + (xlast[i] / inDegree[i])
            """if (n == 'p15'):
                print(x[n])"""
                    #x[n] = x[n] + (xlast[i] / inDegree[i])
                    # if(temp>x[n]):
                    # x[n]=temp
        else:
            x[n]=1/N

        if (outDegree[n] > 0):
            x[n] = (x[n] / (math.sqrt(outDegree[n]))) #outDegree[n] = number of papers that cited paper 'n'
        sum=sum+x[n]
    for n in x:
        #x[n]=(x[n]/sum)*N
        dif= dif+abs(xlast[n]-x[n])
        #print(n, x[n])
    print("Number of Iterations",c)
    print("Difference",dif)

items=sorted(x.items())

csv_file = open("New Author_Rank_modificatioin.csv", "w",encoding="utf-8")
writer = csv.writer(csv_file)
for key, value in x.items():
    writer.writerow([key, value])
csv_file.close()

