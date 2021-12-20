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


for row in csv_dict_reader2:
        id=row['id']
        refer=row['references']
        G.add_edge(refer, id)







W = nx.stochastic_graph(G, weight="weight")


N = W.number_of_nodes()
alpha=0.85




inDegree=G.in_degree
outDegree=G.out_degree
x = dict.fromkeys(W, 1)
dangling_weights = x
dangling_nodes = [n for n in W if W.in_degree(n, weight='weight') == 0.0]
p = dict.fromkeys(W, 1.0 / N)



xlast=dict.fromkeys(W,0)
dif=0
final=dict.fromkeys(W,0)
for i in x:
    dif=dif+abs(xlast[i]-x[i])
eps=.0000001
while (dif>eps):
    for i in x:
        xlast[i] = x[i]
    sum=0
    for n in x:
        for i in W[n]:
            if(inDegree[i]>0):
                x[n]+=(xlast[i]/inDegree[i])
        sum=sum+x[n]
    dif = 0
    for n in x:
        if(sum>0):
            x[n]=(x[n]/sum)*N
        dif = dif + abs(xlast[n] - x[n])


csv_file = open("New Normal Author_Rank.csv", "w",encoding="utf-8")
writer = csv.writer(csv_file)
for key, value in x.items():
    writer.writerow([key, value])
csv_file.close()
