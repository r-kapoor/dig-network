import networkx as nx
import codecs
import json

# DATA_FILE = "/home/rkapoor/Documents/ISI/data/DIG-Nov-Eval/gt-v02-all.jl"
# input_file_base = "output.jl"
input_file_base = 'specific_domain.jl'
output_file_base = "specific_domain_city_name_phone.jl"

DIR_NAME = 'liveescortreviews.com'

# doc_keys = dict()

def safe_copy_simple(json_from, json_to, field):
    if field in json_from and json_from[field] is not None:
        json_to[field] = json_from[field]

def safe_copy(json_from, json_to, field):
    try:
        if field in json_from and json_from[field] is not None:
            distinct_values = set()
            for values in json_from[field]:
                results = values['result']
                if type(results) is list:
                    for result in results:
                        distinct_values.add(result['value'])
                elif 'value' in results:
                    distinct_values.add(results['value'])

            json_to[field] = list(distinct_values)
    except Exception:
        print(json_from[field])

def extract_data(json_document, outfile):
    extracted_document = {}
    extracted_document['high_precision'] = {}
    extracted_document['high_recall'] = {}

    safe_copy_simple(json_document, extracted_document, 'cdr_id')
    if 'high_precision' in json_document:
        safe_copy(json_document['high_precision'], extracted_document['high_precision'], 'city')
        safe_copy(json_document['high_precision'], extracted_document['high_precision'], 'name')
        safe_copy(json_document['high_precision'], extracted_document['high_precision'], 'phone')


    if 'high_recall' in json_document:
        safe_copy(json_document['high_recall'], extracted_document['high_recall'], 'city')
        safe_copy(json_document['high_recall'], extracted_document['high_recall'], 'name')
        safe_copy(json_document['high_recall'], extracted_document['high_recall'], 'phone')

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

# For All Files
# for count in range(1,91):
    # outfile = codecs.open(DIR_NAME +'/'+ str(count)+output_file_base, 'w', 'utf-8')
    # print(DIR_NAME +'/'+ str(count)+input_file_base)
    # with codecs.open(DIR_NAME +'/'+ str(count)+input_file_base, 'r', 'utf-8') as infile:
    #     for line in infile:
    #         count += 1
    #         json_document = json.loads(line)
    #         extract_data(json_document, outfile)

    # outfile.close()

# For Domain files
outfile = codecs.open(DIR_NAME +'/'+output_file_base, 'w', 'utf-8')
print(DIR_NAME +'/'+ input_file_base)
with codecs.open(DIR_NAME +'/'+ input_file_base, 'r', 'utf-8') as infile:
    for line in infile:
        json_document = json.loads(line)    
        extract_data(json_document, outfile)

outfile.close()
# G=nx.Graph()
# G.add_edge(1,2) # default edge data=1
# G.add_edge(2,3,weight=0.9) # specify edge data

# elist=[('a','b',5.0),('b','c',3.0),('a','c',1.0),('c','d',7.3)]
# G.add_weighted_edges_from(elist)

# nx.draw(G)


# G=nx.cubical_graph()
# nx.draw(G)