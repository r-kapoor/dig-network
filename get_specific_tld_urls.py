import codecs
import json
import tldextract

DATA_FILE = "/home/rkapoor/Documents/ISI/data/DIG-Nov-Eval/gt-v02-all.jl"

DOMAIN_OF_INTEREST = 'backpage.com'

def safe_copy(json_from, json_to, field):
    if field in json_from and json_from[field] is not None:
        json_to[field] = json_from[field]

def get_domain(json_document):
    if 'url' in json_document:
        url = json_document['url']
        ext = tldextract.extract(url)
        tld = ext.registered_domain
        return tld
    
output_file_base = "all_urls.txt"
count = 0
outfile = codecs.open(DOMAIN_OF_INTEREST+'/'+output_file_base, 'w', 'utf-8')

with codecs.open(DATA_FILE, 'r', 'utf-8') as infile:
    for line in infile:
        count += 1
        json_document = json.loads(line)
        domain = get_domain(json_document)
        if domain == DOMAIN_OF_INTEREST:
            outfile.write(json_document['url'])

        if count%100 == 0:
            print(count)

outfile.close()