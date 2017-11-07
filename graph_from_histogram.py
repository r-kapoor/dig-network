import pickle
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

num_nodes = 89692

with open("histogram", "rb") as fp:
    histogram = pickle.load(fp)

num_nodes_non_zero = sum(histogram)
# num_nodes_zero = num_nodes - num_nodes_non_zero
print("Num nodes zero:", num_nodes_non_zero)
# histogram[0] = num_nodes_zero
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