import codecs
import pickle
import json

def get_list_of_extractions(doc, type_of_extraction, variable):
    set_of_extractions = set()
    if(type_of_extraction in doc and variable in doc[type_of_extraction]):
        set_of_extractions = set(doc[type_of_extraction][variable])

    return set_of_extractions

def get_intersection(a, b):
    return a & b

def get_union(a, b):
    return a | b

def get_metrics(hp, hr):
    intersection = get_intersection(hp, hr)
    union = get_union(hp, hr)
    if(len(union) == 0):
        jaccard = 1
    else:
        jaccard = len(intersection)/len(union)

    if(len(hp) == 0):
        similar_hp = 1
    else:
        similar_hp = len(intersection)/len(hp)

    if(len(hr) == 0):
        similar_hr = 1
    else:
        similar_hr = len(intersection)/len(hr)
    
    difference = union - intersection
    return jaccard, similar_hp, similar_hr, len(difference)

jaccard_list = []
similar_hp_list = []
similar_hr_list = []
diff_len_list = []
for count in range(1,91):
    print("File:",count)
    with codecs.open('graph_data/'+str(count)+'city_name_phone.jl', 'r', 'utf-8') as data_file:
        for line in data_file:
            json_document = json.loads(line)
            
            # G_hp_city.add_node(node_id)
            # G_hp_city.add_node(node_id)
            # G_hp_name.add_node(node_id)
            # G_hr_name.add_node(node_id)
            # G_hp_phone.add_node(node_id)
            # G_hr_phone.add_node(node_id)

            city_hp = get_list_of_extractions(json_document, 'high_precision', 'phone')
            city_hr = get_list_of_extractions(json_document, 'high_recall', 'phone')
            
            jaccard, similar_hp, similar_hr, diff_len = get_metrics(city_hp, city_hr)
            jaccard_list.append(jaccard)
            similar_hp_list.append(similar_hp)
            similar_hr_list.append(similar_hr)
            diff_len_list.append(diff_len)
            # name_hp = get_list_of_extractions(json_document, 'high_precision', 'name')
            # add_list_to_dict(name_hp, name_hp_nodes, node_id)

            # name_hr = get_list_of_extractions(json_document, 'high_recall', 'name')
            # add_list_to_dict(name_hr, name_hr_nodes, node_id)

            # phone_hp = get_list_of_extractions(json_document, 'high_precision', 'phone')
            # add_list_to_dict(phone_hp, phone_hp_nodes, node_id)

            # phone_hr = get_list_of_extractions(json_document, 'high_recall', 'phone')
            # add_list_to_dict(phone_hr, phone_hr_nodes, node_id)

            # node_data[node_id] = json_document
            # node_id += 1

with open('jaccard_phone.pkl', 'wb') as f:
    pickle.dump(jaccard_list, f)

with open('similar_hp_phone.pkl', 'wb') as f:
    pickle.dump(similar_hp_list, f)

with open('similar_hr_phone.pkl', 'wb') as f:
    pickle.dump(similar_hr_list, f)

with open('diff_len_phone.pkl', 'wb') as f:
    pickle.dump(diff_len_list, f)