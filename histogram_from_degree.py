import pickle
# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt

total_nodes = 89692

with open('CompleteDegree_name_hp', "rb") as fp:
    degree = pickle.load(fp)

max_degree = 0
max_node = None
count = 0
for node, degree_num in degree.items():
    if(max_degree < degree_num):
        max_degree = degree_num
        max_node = node

print(max_degree, " of ", max_node)

# exit()

max_degree = 696427//1000
degree_hist = [0]*(max_degree+1)
nodes_with_non_zero_degree = len(degree)

nodes_with_zero_degree = total_nodes - nodes_with_non_zero_degree
print(nodes_with_zero_degree)
degree_hist[0] = nodes_with_zero_degree

# Bin by 100
for node, degree_num in degree.items():
    degree_hist[degree_num//1000]+=1

# Calculating pk = Nk/N
pk = [x / total_nodes for x in degree_hist]

# print(degree_hist)
# for index, value in enumerate(degree_hist):
#     if(value > 100):
#         print(index,":",value)



print("Got pk")

x = list()
y = list()
for i in range(len(pk)):
    if(pk[i] > 0):
        x.append(i)
        y.append(pk[i])

# fig = plt.figure()
# ax = plt.gca()
# ax.scatter(range(len(pk)),pk , c='blue', alpha=0.05, edgecolors='none')
# ax.set_yscale('log')
# ax.set_xscale('log')
# plt.show()
# print(x)
# print(y)
# plt.scatter(x, y, s=1)
plt.loglog(x, y, markersize=3, linewidth=0, marker='o')
# plt.yscale('log')
# plt.xscale('log')
# plt.plot(pk)
plt.title("Degree Distribution plot")
plt.ylabel("pk")
plt.xlabel("k")
plt.show()
plt.savefig("city_hr_scatterdegree_loglog100.png")

# # print("Plotted 1")
# plt.plot(pk, marker='o', linewidth=0, markersize=1)
# plt.title("Degree Distribution plot")
# plt.ylabel("pk")
# plt.xlabel("k")
# plt.show()
# plt.savefig("loglog.png")

# print("Plotted 2")