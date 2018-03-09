import random
import numpy
from scipy.stats import truncnorm
import matplotlib.pyplot as plt
import copy
import sys
# Example number of cities in the world
NUMBER_OF_POSSIBLE_EXTRACTIONS = 10000

NUMBER_OF_PAGES = 1000

NUMBER_OF_TRUE_EXTRACTIONS = 2000

print(numpy.random.normal(loc=0.0, scale=1.0, size=10))
print(random.normalvariate(0, 2))

# scale = 20.
# range = 100
# size = 100

lower, upper = 0, NUMBER_OF_POSSIBLE_EXTRACTIONS
mu, sigma = NUMBER_OF_POSSIBLE_EXTRACTIONS/2, NUMBER_OF_POSSIBLE_EXTRACTIONS/8
X = truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma).rvs(size=NUMBER_OF_TRUE_EXTRACTIONS)

# X = truncnorm(a=0, b=range, loc=range/2., scale=scale).rvs(size=size)
X = X.round().astype(int)

print("Distribution:",X)

# bins = 100
# plt.hist(X, bins)
# plt.show()
# plt.hist(X)
# plt.show()

print("Mean:",numpy.mean(X))
print("SD:",numpy.std(X))

X = sorted(X)

print("Num of True Extractions:", NUMBER_OF_TRUE_EXTRACTIONS)
true_extractions = list()
extractions = list()
for i in range(NUMBER_OF_PAGES):
    true_extractions.append([])
    extractions.append([])

for i in X:
    while(True):
        index = random.randint(0,NUMBER_OF_PAGES-1)
        if i in true_extractions[index]:
            continue
        else:
            true_extractions[index].append(i)
            break

# print("True Extractions:",true_extractions)

def simulate_extractions(precision, recall):
    # Get other values
    number_of_extractions = recall * NUMBER_OF_TRUE_EXTRACTIONS / precision
    number_of_extractions = int(round(number_of_extractions))
    tp = int(round(precision*number_of_extractions))
    fn = NUMBER_OF_TRUE_EXTRACTIONS - tp
    fp = number_of_extractions - tp

    print("Number of extractions:",number_of_extractions)
    print("TP:",tp)
    print("FN:",fn)
    print("FP:",fp)

    true_extractions_copy = copy.deepcopy(true_extractions)

    # Sample tp extractions without replacement
    num = 0
    while(num < tp):
        index = random.randint(0,NUMBER_OF_PAGES-1)
        values = true_extractions_copy[index]
        if len(values) > 0:
            ind = random.randint(0, len(values) - 1)
            extractions[index].append(values[ind])
            del values[ind]
            num += 1
        else:
            continue

    # Add fp extractions
    num = 0
    while(num < fp):
        index = random.randint(0,NUMBER_OF_PAGES-1)
        while(True):
            possible_fp = random.randint(0,NUMBER_OF_POSSIBLE_EXTRACTIONS-1)
            if possible_fp not in extractions[index]:
                extractions[index].append(possible_fp)
                num += 1
                break
            else:
                continue

    # print("Extractions:",extractions)
    return extractions

def convert_to_adj_list(extractions):
    adjacency_list = dict()
    for page in extractions:
        for extraction1 in page:
            for extraction2 in page:
                if extraction1 != extraction2:
                    if extraction1 in adjacency_list:
                        adjacency_list[extraction1].add(extraction2)
                    else:
                        adjacency_list[extraction1] = set()
                        adjacency_list[extraction1].add(extraction2)

    return adjacency_list

def get_degree_from_adj_list(adjacency_list):
    degree_dict = dict()
    max_degree = 0
    for key, value in adjacency_list.items():
        degree_dict[key] = len(value)
        if max_degree < degree_dict[key]:
            max_degree = degree_dict[key]

    return degree_dict, max_degree

def degree_distribution(degree_dict, max_degree, BIN_SIZE):
    total_nodes = len(degree_dict)
    max_degree = max_degree//BIN_SIZE
    degree_dist = [0]*(max_degree+1)
    for key, value in degree_dict.items():
        degree_dist[value//BIN_SIZE] += 1

    return degree_dist, total_nodes

def plot_degree_dist(degree_dist, total_nodes, name):
    # Calculating pk = Nk/N
    pk = [x / total_nodes for x in degree_dist]

    x = list()
    y = list()
    for i in range(len(pk)):
        if(pk[i] > 0):
            x.append(i)
            y.append(pk[i])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.loglog(x, y, markersize=3, linewidth=0, marker='o')
    plt.title("Degree Distribution:"+str(name))
    ax.set_ylabel("pk")
    ax.set_xlabel("k")
    # plt.show()
    fig.savefig("simulation/"+name+".png")
    fig.clf()
    plt.cla()
    plt.close() 
    # exit()


def process_extractions_to_graph(extractions, name):
    adjacency_list = convert_to_adj_list(extractions)
    # print("Adjacency List:",adjacency_list)
    degree_dict, max_degree = get_degree_from_adj_list(adjacency_list)
    # print("Degree:",degree_dict)
    degree_dist, total_nodes = degree_distribution(degree_dict, max_degree, 1)
    # print("Degree Histogram:",degree_dist)
    print("Total Nodes:",total_nodes)
    plot_degree_dist(degree_dist, total_nodes, name)

process_extractions_to_graph(true_extractions, "Extractions_True")

# for precision in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
# for precision in [0.1]:
    # for recall in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    # for recall in [0.7]:
precision = float(sys.argv[1])
recall = float(sys.argv[2])
print("Precision:", precision)
print("Recall:", recall)
extractions = simulate_extractions(precision, recall)
process_extractions_to_graph(extractions, "Extractions_P:" + str(precision) + "_R:"+str(recall))






