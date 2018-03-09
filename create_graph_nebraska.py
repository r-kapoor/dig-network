import json
import codecs
import tldextract
import pickle
import matplotlib.pyplot as plt

TYPE_OF_EXTRACTION = 'high_recall'
EXTRACTION_VARIABLE = 'name'

with open('backpage.com/nebraska.json', "rb") as fp:
    urls = pickle.load(fp)

def get_extractions(urls, section, field):
    all_extractions = list()
    for key, value in urls.items():
        extractions = list()
        if field in value[section]:
            extractions = list(value[section][field])

        all_extractions.append(extractions)

    return all_extractions

def get_dict_extraction_to_pageid(extractions):
    extraction_to_pageid = dict()
    node_id = 0
    for page in extractions:
        for extraction in page:
            if extraction in extraction_to_pageid:
                extraction_to_pageid[extraction].append(node_id)
            else:
                extraction_to_pageid[extraction] = [node_id]
        node_id += 1

    return extraction_to_pageid

def convert_to_ads_adj_list(extraction_to_pageid):
    adjacency_list = dict()
    for key, value in extraction_to_pageid.items():
        for page1 in value:
            for page2 in value: 
                if page1 != page2:
                    if page1 in adjacency_list:
                        adjacency_list[page1].add(page2)
                    else:
                        adjacency_list[page1] = set()
                        adjacency_list[page1].add(page2)

    return adjacency_list

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

    print(x)
    print(y)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    # Log Log Scale
    ax.loglog(x, y, markersize=3, linewidth=0, marker='o')
    # Linear Scale
    # ax.scatter(x, y, linewidth=0, marker='o')
    plt.title("Degree Distribution:"+str(name))
    ax.set_ylabel("pk")
    ax.set_xlabel("k")
    plt.show() 
    exit()


def process_extractions_to_graph(extractions, name):
    adjacency_list = convert_to_adj_list(extractions)
    # print("Adjacency List:",adjacency_list)
    # exit()
    degree_dict, max_degree = get_degree_from_adj_list(adjacency_list)
    # print("Degree:",degree_dict)
    degree_dist, total_nodes = degree_distribution(degree_dict, max_degree, 1)
    # print("Degree Histogram:",degree_dist)
    print("Total Nodes:",total_nodes)
    plot_degree_dist(degree_dist, total_nodes, name)

def process_extractions_to_ad_graph(extractions, name):
    extraction_to_pageid = get_dict_extraction_to_pageid(extractions)
    # print("Extraction to pageid:", extraction_to_pageid)
    # exit()
    adjacency_list = convert_to_ads_adj_list(extraction_to_pageid)
    # print("Adjacency List:",adjacency_list)
    write_adj_list_to_file(adjacency_list, name)
    exit()
    degree_dict, max_degree = get_degree_from_adj_list(adjacency_list)
    # print("Degree:",degree_dict)
    degree_dist, total_nodes = degree_distribution(degree_dict, max_degree, 1)
    # print("Degree Histogram:",degree_dist)
    print("Total Nodes:",total_nodes)
    plot_degree_dist(degree_dist, total_nodes, name)

def write_adj_list_to_file(adjacency_list, name):
    print("Writing "+name+'_adj')
    with open(name+'_adj', 'w') as f:
        for key, values in adjacency_list.items():
            f.write(str(key)+" ")
            for value in values:
                f.write(str(value)+" ")
            f.write("\n")

all_extractions = get_extractions(urls, TYPE_OF_EXTRACTION, EXTRACTION_VARIABLE)
process_extractions_to_ad_graph(all_extractions, TYPE_OF_EXTRACTION + '_' + EXTRACTION_VARIABLE)
# process_extractions_to_graph(all_extractions, 'high_recall_phone')
