import pickle
import matplotlib.pyplot as plt

total_nodes = 6803
with open('extraction_as_node/name_hr_adjacency_list', "rb") as fp:
    adjacency_list = pickle.load(fp)

with open('extraction_as_node/index_to_name_hr', "rb") as fp:
    index_to_city = pickle.load(fp)

specials = list()

total_nodes_non_zero = len(adjacency_list)
max_degree = 0
min_degree = 100
for node, adj_list in adjacency_list.items():
    degree = len(adj_list)
    if degree == 1528:
        specials.append(index_to_city[node])
    if(max_degree < degree):
        max_degree = degree
    if min_degree > degree:
        min_degree = degree

print("Max Degree:",max_degree)
print("Min Degree:",min_degree)
print("Total Nodes:", total_nodes)
print("Total Nodes Non Zero:", total_nodes_non_zero)
print("Specials:", specials)
print(len(specials))
exit()
degree_hist = [0]*(max_degree+1)

for node, adj_list in adjacency_list.items():
    degree = len(adj_list)
    degree_hist[degree] += 1

degree_hist[0] = total_nodes - total_nodes_non_zero
# Calculating pk = Nk/N
print("Degrees with freq > 100")
for degree, freq in enumerate(degree_hist):
    if freq > 100:
        print(degree,":",freq)

print(degree_hist)

pk = [x / total_nodes for x in degree_hist]

print("Got pk")

x = list()
y = list()
for i in range(len(pk)):
    if(pk[i] > 0):
        x.append(i)
        y.append(pk[i])

plt.loglog(x, y, markersize=3, linewidth=0, marker='o')
plt.title("Degree Distribution plot")
plt.ylabel("pk")
plt.xlabel("k")
plt.show()
# plt.savefig("city_hr_scatterdegree_loglog100.png")