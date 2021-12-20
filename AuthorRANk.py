import pandas as pd
import csv
import networkx as nx

G = nx.DiGraph()
PaperToAuthor = pd.read_csv("F:\Thesis Work\DATA\PaperToAuthor.csv",low_memory=False)
PaperRank = pd.read_csv(r"F:\Thesis Work\New PageRank Author_Rank.csv")
inDegree=G.in_degree
outDegree=G.out_degree

csv_file = open("AuthorRankForWalcom_Pagerank2.csv", "w",encoding="utf-8")
writer = csv.writer(csv_file)

for i in PaperToAuthor.index:
  id=PaperToAuthor['id'][i]
  author=PaperToAuthor['authors'][i]
  G.add_edge(author,id)
W = nx.stochastic_graph(G, weight="weight")
N = W.number_of_nodes()
print("Total nodes",N)

PR={}
Authors = {}


for i in PaperRank.index:
    id=PaperRank['id'][i]
    value=PaperRank['value'][i]
    PR[id]=value
print(len(PR))

for j in PaperToAuthor.index:
    AuthorName = PaperToAuthor["authors"][j]
    Authors[AuthorName] = 0
print(len(Authors))


Ac=0
for n in Authors:
    Ac+=1
    for i in W[n]:
        Authors[n]+=PR[i]/inDegree[i]
    print(Ac,n,Authors[n])
    writer.writerow([n, Authors[n]])
csv_file.close()










