import numpy as np
from csv import DictReader
import csv
import networkx as nx
import matplotlib.pyplot as plt
from numpy import linalg as LA
from collections import defaultdict
import math
import pandas as pd


def pagerank(G, alpha, personalization=None,max_iter=100, tol=1.0e-6, nstart=None, weight='weight',dangling=None):

    if len(G) == 0:
        return {}

    if not G.is_directed():
        D = G.to_directed()
    else:
        D = G

    # Create a copy in (right) stochastic form
    W = nx.stochastic_graph(D, weight=weight)
    N = W.number_of_nodes()

    # Choose fixed starting vector if not given
    if nstart is None:
        x = dict.fromkeys(W, 1.0 / N)
    else:
        # Normalized nstart vector
        s = float(sum(nstart.values()))
        x = dict((k, v / s) for k, v in nstart.items())

    if personalization is None:

        # Assign uniform personalization vector if not given
        p = dict.fromkeys(W, 1.0 / N)

    else:
        missing = set(G) - set(personalization)
        if missing:
            raise nx.NetworkXError('Personalization dictionary '
                                'must have a value for every node. '
                                'Missing nodes %s' % missing)
        s = float(sum(personalization.values()))
        p = dict((k, v / s) for k, v in personalization.items())


    if dangling is None:

        # Use personalization vector if dangling vector not specified
        dangling_weights = p
    else:
        missing = set(G) - set(dangling)
        if missing:
            raise nx.NetworkXError('Dangling node dictionary '
                                'must have a value for every node. '
                                'Missing nodes %s' % missing)
        s = float(sum(dangling.values()))
        dangling_weights = dict((k, v / s) for k, v in dangling.items())
    dangling_nodes = [n for n in W if W.out_degree(n, weight=weight) == 0.0]

    # power iteration: make up to max_iter iterations

    for _ in range(max_iter):
        xlast = x
        x = dict.fromkeys(xlast.keys(), 0)
        danglesum = alpha * sum(xlast[n] for n in dangling_nodes)
        for n in x:

            # this matrix multiply looks odd because it is
            # doing a left multiply x^T=xlast^T*W
            for nbr in W[n]:
                x[nbr] += alpha * xlast[n] * W[n][nbr][weight]
            x[n] += danglesum * dangling_weights[n] + (1.0 - alpha) * p[n]

        # check convergence, l1 norm
        err = sum([abs(x[n] - xlast[n]) for n in x])
        if err < N * tol:
            return x
    raise nx.NetworkXError('pagerank: power iteration failed to converge '
                        'in %d iterations.' % max_iter)


G = nx.DiGraph()
read_obj2=open("F:\Thesis Work\DATA\PaperToPaper.csv","r",encoding="utf8")
PaperToAuthor = open("F:\Thesis Work\DATA\PaperToAuthor.csv","r",encoding="utf8")
csv_dict_reader2 = DictReader(read_obj2)
column_names2 = csv_dict_reader2.fieldnames


for row in csv_dict_reader2:
        id=row['id']
        refer=row['references']
        G.add_edge(id, refer)



#G.add_edges_from(y)



x=nx.pagerank(G,0.85)


#print(x)

csv_file = open("New PageRank Author_Rank.csv", "w",encoding="utf-8")
writer = csv.writer(csv_file)
for key, value in x.items():
    writer.writerow([key, value])
csv_file.close()



#print(pr)