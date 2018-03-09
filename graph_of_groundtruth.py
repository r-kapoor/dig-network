import codecs
import json
import tldextract
import pickle
import networkx as nx

FILE = 'GroundTruth/manual_100_cities.jl'

cities_nodes_dict = dict()

G = nx.Graph()

node_id = 0
with codecs.open(FILE, 'r', 'utf-8') as f:
    for line in f:
        # print(line)
        json_document = json.loads(line)
        correct_cities = json_document['correct_cities']
        print(correct_cities)
        for city in correct_cities:
            if city not in cities_nodes_dict:
                cities_nodes_dict[city] = set()               
            cities_nodes_dict[city].add(node_id)
        G.add_node(node_id)
        node_id += 1

print(cities_nodes_dict)

for key, values in cities_nodes_dict.items():
    for value1 in values:
        for value2 in values:
            if value1 != value2:
                G.add_edge(value1, value2)

print(nx.degree_histogram(G))
