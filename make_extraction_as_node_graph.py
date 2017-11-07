import codecs
import json
import pickle

city_to_index = {}
index_to_city = {}
adjacency_list = {}
current_index = 0

def get_index(value):
    global current_index
    if value in city_to_index:
        index = city_to_index[value]
    else:
        index = current_index
        current_index += 1
        city_to_index[value] = index
        index_to_city[index] = value

    return index

def get_list_of_extractions(doc, type_of_extraction, variable):
    list_of_extractions = []
    if(type_of_extraction in doc and variable in doc[type_of_extraction]):
        list_of_extractions = doc[type_of_extraction][variable]

    return list_of_extractions

def add_list_to_dict(list_of_extractions, adjacency_list):
    for value1 in list_of_extractions:
        index1 = get_index(value1)
        for value2 in list_of_extractions:
            index2 = get_index(value2)
            if index1 != index2:
                if index1 in adjacency_list:
                    adjacency_list[index1].add(index2)
                else:
                    adjacency_list[index1] = set([index2])


for count in range(1,11):
    print("File:",count)
    line_num = 0
    with codecs.open('graph_data/'+str(count)+'city_name_phone.jl', 'r', 'utf-8') as data_file:
        for line in data_file:
            json_document = json.loads(line)
            line_num += 1
            if line_num % 100 == 0:
                print("Line:",line_num)
            city_hp = get_list_of_extractions(json_document, 'high_precision', 'phone')
            add_list_to_dict(city_hp, adjacency_list)

print("Count of cities:", current_index)

with open('city_to_index', 'wb') as f:
    pickle.dump(city_to_index, f)

print("Written 1")

with open('index_to_city', 'wb') as f:
    pickle.dump(index_to_city, f)

print("Written 2")

with open('adjacency_list', 'wb') as f:
    pickle.dump(adjacency_list, f)

print("Written 3")
# print("*"*100)
# print(city_to_index)
# print("*"*100)
# print(index_to_city)
# print("*"*100)
# print(adjacency_list)

