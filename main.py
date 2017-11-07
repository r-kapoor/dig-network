import networkx as nx
import codecs
import json

DATA_FILE = "/home/rkapoor/Documents/ISI/data/DIG-Nov-Eval/gt-v02-all.jl"


doc_keys = dict()

def safe_copy(json_from, json_to, field):
    if field in json_from and json_from[field] is not None:
        json_to[field] = json_from[field]

def extract_data(json_document, doc_keys, outfile):
    extracted_document = {}

    safe_copy(json_document, extracted_document, 'cdr_id')
    safe_copy(json_document, extracted_document, 'high_precision')
    safe_copy(json_document, extracted_document, 'high_recall')
    
    # safe_copy(json_document, extracted_document, 'city')
    # safe_copy(json_document, extracted_document, 'url_extract')
    # safe_copy(json_document, extracted_document, 'tokens_title')
    # safe_copy(json_document, extracted_document, 'extractions')
    # safe_copy(json_document, extracted_document, 'age')

    # safe_copy(json_document, extracted_document, 'inferlink_posting-date')
    # safe_copy(json_document, extracted_document, 'inferlink_city')
    # safe_copy(json_document, extracted_document, 'inferlink_phone')
    # safe_copy(json_document, extracted_document, 'inferlink_price')
    # safe_copy(json_document, extracted_document, 'inferlink_name')
    # safe_copy(json_document, extracted_document, 'inferlink_nationality')
    # safe_copy(json_document, extracted_document, 'inferlink_age')
    # safe_copy(json_document, extracted_document, 'inferlink_title')
    # safe_copy(json_document, extracted_document, 'inferlink_ethnicity')
    # safe_copy(json_document, extracted_document, 'inferlink_email')
    # safe_copy(json_document, extracted_document, 'inferlink_state')
    # safe_copy(json_document, extracted_document, 'inferlink_service')
    # safe_copy(json_document, extracted_document, 'inferlink_review-id')
    # safe_copy(json_document, extracted_document, 'inferlink_eye-color')
    # safe_copy(json_document, extracted_document, 'inferlink_height')
    # safe_copy(json_document, extracted_document, 'inferlink_street-address')
    # safe_copy(json_document, extracted_document, 'inferlink_hair-color')
    # safe_copy(json_document, extracted_document, 'inferlink_weight')
    # safe_copy(json_document, extracted_document, 'inferlink_location')
    
    outfile.write(json.dumps(extracted_document))
    outfile.write('\n')
    # # Count Extractions
    # if 'extractions' in json_document:
    #     document_keys = json_document.get('extractions'].keys()
    #     for key in document_keys:
    #         if key in doc_keys:
    #             doc_keys[key] += 1
    #         else:
    #             doc_keys[key] = 1

output_file_base = "output.jl"
file_number = 1
count = 0
outfile = codecs.open(str(file_number)+output_file_base, 'w', 'utf-8')
with codecs.open(DATA_FILE, 'r', 'utf-8') as infile:
    for line in infile:
        count += 1
        json_document = json.loads(line)
        extract_data(json_document, doc_keys, outfile)
        if(count % 100 == 0):
            print count
        if(count % 1000 == 0):
            file_number += 1
            outfile.close()
            outfile_name = str(file_number)+output_file_base
            outfile = codecs.open(outfile_name, 'w', 'utf-8')
            

print doc_keys
outfile.close()
# G=nx.Graph()
# G.add_edge(1,2) # default edge data=1
# G.add_edge(2,3,weight=0.9) # specify edge data

# elist=[('a','b',5.0),('b','c',3.0),('a','c',1.0),('c','d',7.3)]
# G.add_weighted_edges_from(elist)

# nx.draw(G)


# G=nx.cubical_graph()
# nx.draw(G)