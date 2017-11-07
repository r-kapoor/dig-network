import networkx as nx
import pickle
import os
import networkx as nx
import sys

print("The arguments are: " , str(sys.argv))

list_of_files = sys.argv[1:]
for filename in list_of_files:
    G = nx.read_edgelist(filename)
    degree = nx.degree(G)
    print("Writing:", filename+'_degree')
    with open(filename+'_degree', 'wb') as f:
        pickle.dump(degree, f)