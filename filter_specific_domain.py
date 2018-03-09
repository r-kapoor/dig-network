import codecs
import json
import tldextract

DATA_FILE = "/home/rkapoor/Documents/ISI/data/DIG-Nov-Eval/gt-v02-all.jl"

DOMAINS_OF_INTEREST = ['eroticmugshots.com','asexyservice.com','escortsincollege.com','hoxnif.com', 'liveescortreviews.com']

def safe_copy(json_from, json_to, field):
    if field in json_from and json_from[field] is not None:
        json_to[field] = json_from[field]

def get_domain(json_document):
    if 'url' in json_document:
        url = json_document['url']
        ext = tldextract.extract(url)
        tld = ext.registered_domain
        return tld

def extract_data(json_document, outfile):
    extracted_document = {}

    safe_copy(json_document, extracted_document, 'high_precision')
    safe_copy(json_document, extracted_document, 'high_recall')

    outfile.write(json.dumps(extracted_document))
    outfile.write('\n')
    
output_file_base = "specific_domain.jl"
count = 0
outfile = list()
for domain in DOMAINS_OF_INTEREST:
    outfile.append(codecs.open(domain+'/'+output_file_base, 'w', 'utf-8'))

with codecs.open(DATA_FILE, 'r', 'utf-8') as infile:
    for line in infile:
        count += 1
        json_document = json.loads(line)
        domain = get_domain(json_document)
        if domain in DOMAINS_OF_INTEREST:
            index = DOMAINS_OF_INTEREST.index(domain)    
            extract_data(json_document, outfile[index])
        if(count % 100 == 0):
            print(count)
            
outfile.close()