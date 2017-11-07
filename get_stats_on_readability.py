import codecs
import json
import pickle

DATA_DIR = "tokens_output/"
    
input_file_base = "tokens_output.jl"

def get_list_of_extractions(doc, type_of_extraction):
    set_of_extractions = set()
    if(type_of_extraction in doc and len(doc[type_of_extraction]) == 1):
        set_of_extractions = set(doc[type_of_extraction][0]['result'][0]['value'])

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
    
    return jaccard, similar_hp, similar_hr


jaccard_similarity = list()
intersection_by_hp = list()
intersection_by_hr = list()

for file_number in range(1, 81):
    print("File:", file_number)
    infile_name = DATA_DIR + str(file_number)+input_file_base
    print(infile_name)
    with codecs.open(infile_name, 'r', 'utf-8') as infile:
        for line in infile:
            json_document = json.loads(line)
            hp = get_list_of_extractions(json_document, 'tokens_high_precision')
            hr = get_list_of_extractions(json_document, 'tokens_high_recall')
            jaccard, similar_hp, similar_hr = get_metrics(hp, hr)
            jaccard_similarity.append(jaccard)
            intersection_by_hp.append(similar_hp)
            intersection_by_hr.append(similar_hr)

with open('readability_jaccard', 'wb') as f:
    pickle.dump(jaccard_similarity, f)
            
with open('readability_hp', 'wb') as f:
    pickle.dump(intersection_by_hp, f)

with open('readability_hr', 'wb') as f:
    pickle.dump(intersection_by_hr, f)