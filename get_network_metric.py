import networkx as nx
import collections
import math
import pickle

def get_graph():
    print("Get Graph")
    # G=nx.Graph()
    # G.add_edge(1,2)
    # G.add_edge(1,3)
    # G.add_edge(1,4)
    # G.add_edge(2,3)
    # G.add_edge(5,6)
    # G.add_edge(6,7)
    with open('/data/Paper_Data/high_recall_name_adj.pkl', 'rb') as f:
        G = pickle.load(f)
    return G

def clustering_coefficient(G):
    print("Clustering Coefficient")
    # print(nx.clustering(G))
    return nx.average_clustering(G)

def connected_components(G):
    print("Connected Components")
    return nx.number_connected_components(G)

def gamma_estimation(G):
    print("Gamma")
    degrees = nx.degree(G).values()
    # print(degrees)
    total_nodes = len(degrees)
    counter=collections.Counter(degrees)
    # print(counter)
    gamma_dict = dict()
    for k, count in counter.items():
        # print(k, count/total_nodes)
        if k!=1:
            gamma_dict[k] = -math.log(count/total_nodes)/math.log(k)

    return gamma_dict

def centrality(G):
    degree = nx.degree_centrality(G)
    closeness = nx.closeness_centrality(G)
    betweenness = nx.betweenness_centrality(G)
    return degree, closeness, betweenness

def basic_metrics_of_largest_cc(G):
    largest_cc = max(nx.connected_component_subgraphs(G), key=len)
    order = largest_cc.order()
    diameter = nx.diameter(largest_cc)
    av_path_length = nx.average_shortest_path_length(largest_cc)
    return order, diameter, av_path_length, connectivity(largest_cc)

def connectivity(G):
    algebraic_connectivity = nx.algebraic_connectivity(G)
    edge_connectivity = nx.edge_connectivity(G)
    node_connectivity = nx.node_connectivity(G)
    return algebraic_connectivity, edge_connectivity, node_connectivity

def degree_correlation(G):
    degree_correlation = nx.degree_pearson_correlation_coefficient(G)
    return degree_correlation

G = get_graph()
print("Read")
print(clustering_coefficient(G))
print(connected_components(G))
# print(gamma_estimation(G))
# print("Centrality:",centrality(G))
print("Order:", G.order())
print("Basic Metrics:", basic_metrics_of_largest_cc(G))
print("Connectivity:", connectivity(G))
print("Degree Correlation:", degree_correlation(G)) 