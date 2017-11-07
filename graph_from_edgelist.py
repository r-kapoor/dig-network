import networkx as nx
from collections import Counter
import codecs
import json
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from string import ascii_lowercase
num_nodes = 89692

# G = nx.read_edgelist('test_edgelist.txt')
# degree = nx.degree(G)
# print(degree)
# A = Counter(degree)
# B = Counter(degree)
# print(A+B)


for c in ascii_lowercase:
    filename = '/dev/shm/output_filea'+c
    G = nx.read_edgelist(filename)
    # G = nx.read_edgelist('test_edgelist.txt')
    print("Read",filename)
    # print(nx.degree(G))
    degree = nx.degree(G)

    with open('degreea'+c, 'wb') as f:
        pickle.dump(histogram, f)

exit()
# print(histogram)
# print(sorted(nx.degree(G).values(),reverse=True))
print("Got histogram")
num_nodes_non_zero = sum(histogram)
num_nodes_zero = num_nodes - num_nodes_non_zero
print("Num nodes zero:", num_nodes_zero)
histogram[0] = num_nodes_zero
pk = [x / num_nodes for x in histogram]

print("Got pk")

plt.plot(pk)
plt.title("Degree Distribution plot")
plt.ylabel("pk")
plt.xlabel("k")
# plt.show()
plt.savefig("degdist.png")

print("Plotted 1")
plt.loglog(pk)
plt.title("Degree Distribution plot")
plt.ylabel("pk")
plt.xlabel("k")
# plt.show()
plt.savefig("loglog.png")

print("Plotted 2")