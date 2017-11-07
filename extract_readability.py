import codecs
import json

DATA_FILE = "/home/rkapoor/Documents/ISI/data/DIG-Nov-Eval/gt-v02-all.jl"

def safe_copy(json_from, json_to, field):
    if field in json_from and json_from[field] is not None:
        json_to[field] = json_from[field]

def extract_data(json_document, outfile):
    extracted_document = {}

    safe_copy(json_document, extracted_document, 'tokens_high_precision')
    safe_copy(json_document, extracted_document, 'tokens_high_recall')
        
    outfile.write(json.dumps(extracted_document))
    outfile.write('\n')
    
output_file_base = "tokens_output.jl"
file_number = 10
count = 0
outfile = codecs.open(str(file_number)+output_file_base, 'w', 'utf-8')
with codecs.open(DATA_FILE, 'r', 'utf-8') as infile:
    for line in infile:
        count += 1
        if(count % 100 == 0):
            print(count)
        if count <= 9000:
            continue
        json_document = json.loads(line)
        extract_data(json_document, outfile)
        if(count % 100 == 0):
            print(count)
        if(count % 1000 == 0):
            file_number += 1
            outfile.close()
            outfile_name = str(file_number)+output_file_base
            print("Open FIle:",outfile_name)
            outfile = codecs.open(outfile_name, 'w', 'utf-8')
            
outfile.close()