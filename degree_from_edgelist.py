import networkx as nx
import pickle
from string import ascii_lowercase

for c in ascii_lowercase:
    filename = '/dev/data/degreec'+c
    G = nx.read_edgelist(filename)
    print("Read",filename)
    degree = nx.degree(G)

    with open('DictDegreec'+c, 'wb') as f:
        pickle.dump(degree, f)