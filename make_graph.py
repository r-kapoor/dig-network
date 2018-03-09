import networkx as nx
import codecs
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# FILE_NAME = 'city_name_phone.jl'
FILE_NAME = 'specific_domain_city_name_phone.jl'
# DIR_NAME = 'graph_data'
DIR_NAME = 'asexyservice.com'

# asexyservice.com:
# eroticmugshots.com:
# escortsincollege.com:
# hoxnif.com:
# liveescortreviews.com:


def is_edge(doc1, doc2, type_of_extraction, variable):
    if(type_of_extraction in doc1 and type_of_extraction in doc2 and variable in doc1[type_of_extraction] and variable in doc2[type_of_extraction]):
        list1 = doc1[type_of_extraction][variable]
        list2 = doc2[type_of_extraction][variable]
        for value1 in list1:
            for value2 in list2:
                if value1 == value2:
                    return True

    return False

def get_list_of_extractions(doc, type_of_extraction, variable):
    list_of_extractions = []
    if(type_of_extraction in doc and variable in doc[type_of_extraction]):
        list_of_extractions = doc[type_of_extraction][variable]

    return list_of_extractions

def write_edge_list(dictionary, filename):
    with codecs.open(DIR_NAME+'/'+filename, 'w', 'utf-8') as f:
        for key, value_list in dictionary.items():
            for value1 in value_list:
                for value2 in value_list:
                    if(value1 != value2):
                        f.write(str(value1) + ' ' + str(value2) + '\n')

def add_list_to_dict(list_of_extractions, dictionary, node_id):
    for value in list_of_extractions:
        if value in dictionary:
            dictionary[value].append(node_id)
        else:
            dictionary[value] = [node_id]

def plot_degree_distribution(G, graph_name):
    degree_sequence=sorted(nx.degree(G).values(),reverse=True) # degree sequence

    dmax=max(degree_sequence)

    plt.loglog(degree_sequence,'b-',marker='o')
    plt.title("Degree rank plot")
    plt.ylabel("degree")
    plt.xlabel("rank")

    # draw graph in inset
    plt.axes([0.45,0.45,0.45,0.45])
    Gcc=sorted(nx.connected_component_subgraphs(G), key = len, reverse=True)[0]
    pos=nx.spring_layout(Gcc)
    plt.axis('off')
    nx.draw_networkx_nodes(Gcc,pos,node_size=20)
    nx.draw_networkx_edges(Gcc,pos,alpha=0.4)

    plt.savefig(graph_name + "_degree_histogram.png")
    # plt.show()

# G_hp_city=nx.Graph()
# G_hr_city=nx.Graph()
# G_hp_name=nx.Graph()
# G_hr_name=nx.Graph()
# G_hp_phone=nx.Graph()
# G_hr_phone=nx.Graph()

logs = open('logs.out', 'w')

# node_data = dict()
city_hp_nodes = dict()
city_hr_nodes = dict()
name_hp_nodes = dict()
name_hr_nodes = dict()
# phone_hp_nodes = dict()
# phone_hr_nodes = dict()

node_id = 0

# For ALL Files
# for count in range(1,91):
#     print("File:",count)
#     logs.write("File:"+str(count)+'\n')
#     print(DIR_NAME+'/'+str(count)+FILE_NAME)
#     with codecs.open(DIR_NAME+'/'+str(count)+FILE_NAME, 'r', 'utf-8') as data_file:
#         for line in data_file:
#             json_document = json.loads(line)
            
#             # G_hp_city.add_node(node_id)
#             # G_hp_city.add_node(node_id)
#             # G_hp_name.add_node(node_id)
#             # G_hr_name.add_node(node_id)
#             # G_hp_phone.add_node(node_id)
#             # G_hr_phone.add_node(node_id)

#             city_hp = get_list_of_extractions(json_document, 'high_precision', 'city')
#             add_list_to_dict(city_hp, city_hp_nodes, node_id)

#             city_hr = get_list_of_extractions(json_document, 'high_recall', 'city')
#             add_list_to_dict(city_hr, city_hr_nodes, node_id)

#             name_hp = get_list_of_extractions(json_document, 'high_precision', 'name')
#             add_list_to_dict(name_hp, name_hp_nodes, node_id)

#             name_hr = get_list_of_extractions(json_document, 'high_recall', 'name')
#             add_list_to_dict(name_hr, name_hr_nodes, node_id)

#             # phone_hp = get_list_of_extractions(json_document, 'high_precision', 'phone')
#             # add_list_to_dict(phone_hp, phone_hp_nodes, node_id)

#             # phone_hr = get_list_of_extractions(json_document, 'high_recall', 'phone')
#             # add_list_to_dict(phone_hr, phone_hr_nodes, node_id)

#             # node_data[node_id] = json_document
#             node_id += 1


# For Domain Files:

print(DIR_NAME+'/'+FILE_NAME)
with codecs.open(DIR_NAME+'/'+FILE_NAME, 'r', 'utf-8') as data_file:
    for line in data_file:
        json_document = json.loads(line)

        city_hp = get_list_of_extractions(json_document, 'high_precision', 'city')
        add_list_to_dict(city_hp, city_hp_nodes, node_id)

        city_hr = get_list_of_extractions(json_document, 'high_recall', 'city')
        add_list_to_dict(city_hr, city_hr_nodes, node_id)

        name_hp = get_list_of_extractions(json_document, 'high_precision', 'name')
        add_list_to_dict(name_hp, name_hp_nodes, node_id)

        name_hr = get_list_of_extractions(json_document, 'high_recall', 'name')
        add_list_to_dict(name_hr, name_hr_nodes, node_id)

        # phone_hp = get_list_of_extractions(json_document, 'high_precision', 'phone')
        # add_list_to_dict(phone_hp, phone_hp_nodes, node_id)

        # phone_hr = get_list_of_extractions(json_document, 'high_recall', 'phone')
        # add_list_to_dict(phone_hr, phone_hr_nodes, node_id)

        # node_data[node_id] = json_document
        node_id += 1


        

print("Nodes Added:",node_id)
logs.write("Nodes Added:"+str(node_id)+'\n')

# with open('city_hp.json', 'w') as outfile:
#     json.dump(city_hp_nodes, outfile)

# with open('city_hr.json', 'w') as outfile:
    # json.dump(city_hr_nodes, outfile)

# with open('name_hp.json', 'w') as outfile:
    # json.dump(name_hp_nodes, outfile)

# with open('name_hr.json', 'w') as outfile:
    # json.dump(name_hr_nodes, outfile)

# with open('phone_hp.json', 'w') as outfile:
#     json.dump(phone_hp_nodes, outfile)

# with open('phone_hr.json', 'w') as outfile:
#     json.dump(phone_hr_nodes, outfile)

print("Produces Dump")

print("Writing Edge List")
logs.write("Write Edge List\n")

write_edge_list(city_hp_nodes, 'city_hp')
write_edge_list(city_hr_nodes, 'city_hr')
# write_edge_list(city_hr_nodes, 'city_hr_10k_nodes')
write_edge_list(name_hp_nodes, 'name_hp')
write_edge_list(name_hr_nodes, 'name_hr')
exit()

write_edge_list(name_hr_nodes, 'name_hr')
write_edge_list(phone_hp_nodes, 'phone_hp')
write_edge_list(phone_hr_nodes, 'phone_hr')

exit()

for i in range(node_id):
    print("Adding Edges From:", i)
    logs.write("Adding Edges From:"+str(i)+'\n')
    for j in range(node_id):
        if(j % 10000 == 0):
            print("Adding Edges To:",j)
            logs.write("Adding Edges To:"+str(j)+'\n')
        if i != j:
            if is_edge(node_data[i], node_data[j], 'high_precision', 'city'):
                G_hp_city.add_edge(i, j)

            if is_edge(node_data[i], node_data[j], 'high_recall', 'city'):
                G_hr_city.add_edge(i, j)

            if is_edge(node_data[i], node_data[j], 'high_precision', 'name'):
                G_hp_name.add_edge(i, j)

            if is_edge(node_data[i], node_data[j], 'high_recall', 'name'):
                G_hr_name.add_edge(i, j)

            if is_edge(node_data[i], node_data[j], 'high_precision', 'phone'):
                G_hp_phone.add_edge(i, j)

            if is_edge(node_data[i], node_data[j], 'high_recall', 'phone'):
                G_hr_phone.add_edge(i, j)

print("done")
logs.write("done"+'\n')

print("Pickling")
logs.write("Pickling"+'\n')
nx.write_gpickle(G_hp_city, "G_hp_city.gpickle")
nx.write_gpickle(G_hr_city, "G_hr_city.gpickle")
nx.write_gpickle(G_hp_name, "G_hp_name.gpickle")
nx.write_gpickle(G_hp_phone, "G_hp_phone.gpickle")
nx.write_gpickle(G_hp_phone, "G_hp_phone.gpickle")
nx.write_gpickle(G_hr_phone, "G_hr_phone.gpickle")

# nx.draw(G_hp_city)
# edges_list = nx.edges(G_hp_city)

# for edge in edges_list:
    # print edge

# G = nx.gnp_random_graph(100,0.02)

print("Plotting")
logs.write("Plotting"+'\n')

plot_degree_distribution(G_hp_city, 'G_hp_city')
plot_degree_distribution(G_hr_city, 'G_hr_city')
plot_degree_distribution(G_hp_name, 'G_hp_name')
plot_degree_distribution(G_hr_name, 'G_hr_name')
plot_degree_distribution(G_hp_phone, 'G_hp_phone')
plot_degree_distribution(G_hr_phone, 'G_hr_phone')

print("End")
logs.write("End"+'\n')
logs.close()