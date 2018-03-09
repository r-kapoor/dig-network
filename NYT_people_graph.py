import json
import os
import networkx as nx
import matplotlib.pyplot as plt
import pickle
import time
import operator
YEAR = 1987

def connectivity(G):
    # return 0, 0, 0
    algebraic_connectivity = nx.algebraic_connectivity(G)
    return algebraic_connectivity, 0, 0
    edge_connectivity = nx.edge_connectivity(G)
    node_connectivity = nx.node_connectivity(G)
    return algebraic_connectivity, edge_connectivity, node_connectivity

def basic_metrics_of_largest_cc(G):
    print("largest_cc")
    largest_cc = max(nx.connected_component_subgraphs(G), key=len)
    print("Order")
    order = largest_cc.order()
    # diameter = nx.diameter(largest_cc)
    diameter = 0
    # av_path_length = nx.average_shortest_path_length(largest_cc)
    av_path_length = 0
    print("Connectivity")
    algebraic_connectivity, edge_connectivity, node_connectivity = connectivity(largest_cc) 
    return order, diameter, av_path_length, algebraic_connectivity, edge_connectivity, node_connectivity
    # , connectivity(largest_cc)

metrics = list()
years = list()
clustering_coefficients = list()
orders = list()
connected_components = list()
order_lcc = list()
diameter_lcc = list()
av_path_length_lcc = list()
algebraic_connectivity = list()
edge_connectivity =list()
node_connectivity = list()
metrics = [orders, clustering_coefficients, connected_components, order_lcc, diameter_lcc, av_path_length_lcc, algebraic_connectivity, edge_connectivity, node_connectivity]
metric_names = ["orders", "clustering_coefficients", "connected_components", "order_lcc", "diameter_lcc", "av_path_length_lcc", "algebraic_connectivity", "edge_connectivity", "node_connectivity"]
while YEAR <= 2007:
    # directory = "/home/rkapoor/Documents/ISI/data/NYT/nyt_corpus/data/"+str(YEAR)

    # JLINES_FILENAME = 'NYT.jl'
    # ENTITY = 'People'
    # SUBS_ENTITY = 'Normalized Byline'
    # article_counter = 0
    # article_to_entity_dict = dict()
    # for subdir, dirs, files in os.walk(directory):
    #     for filename in files:
    #         if filename.endswith(JLINES_FILENAME):
    #             filepath = os.path.join(subdir, filename)
    #             print(filepath)
    #             with open(filepath, 'r') as f:
    #                 for line in f:
    #                     json_obj = json.loads(line)
    #                     if ENTITY in json_obj:
    #                         people_list = json_obj[ENTITY]
    #                         if SUBS_ENTITY in json_obj:
    #                             subs_value = json_obj[SUBS_ENTITY]
    #                             if ";" in subs_value:
    #                                 subs_value_list = subs_value.split(";")
    #                                 for subs_value in subs_value_list:
    #                                     subs_value_strip = subs_value.strip()
    #                                     if subs_value_strip in people_list:
    #                                         people_list.remove(subs_value_strip)
    #                             else:
    #                                 if subs_value in people_list:
    #                                     people_list.remove(subs_value)
    #                         if len(people_list) > 0:
    #                             article_id = article_counter
    #                             article_counter += 1
    #                             article_to_entity_dict[article_id] = people_list

    # # Convert to adjacency list
    # max_degree = 0
    # adj_dict = dict()
    # for article_id, people_list in article_to_entity_dict.items():
    #     for person1 in people_list:
    #         for person2 in people_list:
    #             if person1 != person2:
    #                 if person1 in adj_dict:
    #                     adj_dict[person1].add(person2)
    #                 else:
    #                     adj_dict[person1] = set()
    #                     adj_dict[person1].add(person2)
    #                 if max_degree < len(adj_dict[person1]):
    #                     max_degree = len(adj_dict[person1])


    # # Convert to Graph
    # G=nx.from_dict_of_lists(adj_dict)

    # Dump/Load Graph
    # Dump Graph
    # with open('NYT_processed/people_graph_rem_'+str(YEAR)+'.pkl', 'wb') as f:
    #     pickle.dump(G, f)

    # # Load Graph
    with open('NYT_processed/people_graph_rem_'+str(YEAR)+'.pkl', 'rb') as f:
        G = pickle.load(f)

    print(YEAR)
    # centrality = nx.betweenness_centrality(G)
    # sorted_cen = sorted(centrality.items(), key=operator.itemgetter(1), reverse=True)
    # print(sorted_cen[:30])

    order = G.order()
    clustering = nx.average_clustering(G)
    connected_component = nx.number_connected_components(G)
    # clustering = 0
    # connected_component = 0
    years.append(YEAR)
    metrics[0].append(order)
    metrics[1].append(clustering)
    metrics[2].append(connected_component)
    order, diameter, av_path_length, algebraic_connectivity, edge_connectivity, node_connectivity = basic_metrics_of_largest_cc(G)
    metrics[3].append(order)
    metrics[4].append(diameter)
    metrics[5].append(av_path_length)
    metrics[6].append(algebraic_connectivity)
    metrics[7].append(edge_connectivity)
    metrics[8].append(node_connectivity)

    # break

    # degree_hist_dict = dict()
    # with open('NYT_processed/NYT_people.adj', 'w') as f:
    #     for person, adj_people in adj_dict.items():
    #         degree = len(adj_people)
    #         if degree == max_degree:
    #             print(person, adj_people)
    #         if degree in degree_hist_dict:
    #             degree_hist_dict[degree] += 1
    #         else:
    #             degree_hist_dict[degree] = 1
    #         f.write(person + " ".join(adj_people) + "\n")






    # total_nodes = len(adj_dict)

    # max_node = None
    # count = 0
    # BIN_SIZE = 1

    # # print(degree)
    # # exit()

    # max_degree = max_degree//BIN_SIZE
    # degree_hist = [0]*(max_degree+1)

    # # Bin by 100
    # for degree, frequency in degree_hist_dict.items():
    #     degree_hist[degree]+=frequency

    # # print(degree_hist)

    # # Calculating pk = Nk/N
    # # pk = [x / total_nodes for x in degree_hist]
    # pk = degree_hist
    # # print(pk)



    # print("Got pk")

    # x = list()
    # y = list()
    # for i in range(len(pk)):
    #     if(pk[i] > 0):
    #         x.append(i)
    #         y.append(pk[i])

    # plt.loglog(x, y, markersize=3, linewidth=0, marker='o')
    # plt.title("Degree Distribution plot")
    # plt.ylabel("pk")
    # plt.xlabel("k")
    # # plt.show()
    # plt.savefig("NYT_processed/DegreeDistribution"+ str(YEAR)+".png")
    # plt.close()
    YEAR+=1

index = 0
for metric in metrics:
    plt.plot(years, metric)
    plt.xlabel("Years")
    plt.ylabel(metric_names[index])
    plt.show()
    plt.close()
    index += 1




