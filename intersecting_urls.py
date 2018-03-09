import json
import codecs
import tldextract

urls = dict()
duplicates = list()
with codecs.open('/home/rkapoor/Documents/ISI/data/Network/intersecting-urls.jsonl', 'r', 'utf-8') as f:
    for line in f:
        doc = json.loads(line)
        url = doc['url']
        if url in urls:
            urls[url] += 1
        else:
            urls[url] = 1

        # if url == 'http://flint.backpage.com/FemaleEscorts/unforgettable-new-staff-new-attitude/17626747':
            # duplicates.append(doc['name'])


# for key, value in sorted(urls.items(), key=lambda x:x[1]):
#     if value > 10:
#         print("%s: %s" % (key, value))

# print("SIZE:",len(urls))

# # for key, value in urls.items():
#     # if(value > 1):
#         # print(key,":",value)

# print(duplicates)

DATA_FILE = "/home/rkapoor/Documents/ISI/data/DIG-Nov-Eval/gt-v02-all.jl"

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

    safe_copy_simple(json_document, extracted_document, 'url')
    if 'high_precision' in json_document:
        safe_copy(json_document['high_precision'], extracted_document['high_precision'], 'city')
        safe_copy(json_document['high_precision'], extracted_document['high_precision'], 'name')
        safe_copy(json_document['high_precision'], extracted_document['high_precision'], 'phone')


    if 'high_recall' in json_document:
        safe_copy(json_document['high_recall'], extracted_document['high_recall'], 'city')
        safe_copy(json_document['high_recall'], extracted_document['high_recall'], 'name')
        safe_copy(json_document['high_recall'], extracted_document['high_recall'], 'phone')

    outfile.write(json.dumps(extracted_document))
    outfile.write('\n')
    
output_file_base = "intersecting.jl"
count = 0
domain = 'backpage.com'

outfile = codecs.open(domain+'/'+output_file_base, 'w', 'utf-8')

with codecs.open(DATA_FILE, 'r', 'utf-8') as infile:
    for line in infile:
        count += 1
        json_document = json.loads(line)
        if json_document['url'] in urls:    
            extract_data(json_document, outfile)
        if(count % 100 == 0):
            print(count)
            
            
outfile.close()
