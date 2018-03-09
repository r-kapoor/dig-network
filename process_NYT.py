from lxml import etree
import csv
import os
import tarfile
import operator
import json

# DTD_PATH="/home/rkapoor/Documents/ISI/data/NYT/nyt_corpus/dtd/nitf-3-3.dtd"
directory = "/home/rkapoor/Documents/ISI/data/NYT/nyt_corpus/data/1995"

extractor_list = list()
with open('NYT_desc.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        extractor_list.append(row)



# tar_obj = tarfile.open("/home/rkapoor/Documents/ISI/data/NYT/nyt_corpus/data/1987/01.tgz")
# # print([method_name for method_name in dir(tar_obj) if callable(getattr(tar_obj, method_name))])
# for member in tar_obj.getmembers():
#     f = tar_obj.extractfile(member)
#     if f is not None:
#         content = f.read()
#         print(content)
#         exit()

JLINES_FILENAME = 'NYT.jl'
people_dict = dict()
extractor_set = set()
for subdir, dirs, files in os.walk(directory):
    for filename in files:
        if filename.endswith(".tgz"):
            filepath = os.path.join(subdir, filename)
            # filepath = subdir + os.sep + file
            new_dir = os.path.join(subdir, filename.split('.')[0])
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            print(new_dir)
            output_jlines = open(os.path.join(new_dir, JLINES_FILENAME), 'w')
            tar_obj = tarfile.open(filepath)
            for member in tar_obj.getmembers():
                # print(member.name)
                f = tar_obj.extractfile(member)
                if f is not None:
                    output_doc = {}
                    tree = etree.parse(f)
                    for extractor in extractor_list:
                        extracted_list = tree.xpath(extractor[2])
                        if len(extracted_list) > 0:
                            extractor_set.add(extractor[0])
                            if extractor[1] == 'Multiple':
                                value = list()
                                for extracted_value in extracted_list:
                                    if isinstance(extracted_value, etree._Element):
                                        text_iter = extracted_value.itertext()
                                        value_ins = ""
                                        for text in text_iter:
                                            value_ins += text
                                        value.append(value_ins)
                                    else:
                                        value.append(str(extracted_value))
                            else:
                                value = ""
                                extracted_value = extracted_list[0]
                                if isinstance(extracted_value, etree._Element):
                                    text_iter = extracted_value.itertext()
                                    for text in text_iter:
                                        value += text
                                else:
                                    value = str(extracted_value)
                            output_doc[extractor[0]] = value
                    
                    output_jlines.write(json.dumps(output_doc)+'\n')
                            # if extractor[0] == 'People':
                            #     for val in value:
                            #         if 'Pres' in val or 'PRES' in val:
                            #             print(member.name)
                            #             if val in people_dict:
                            #                 people_dict[val] += 1
                            #             else:
                            #                 people_dict[val] = 1
            output_jlines.close()    

            # break
                    # print(output_doc)
            # print(sorted(list(extractor_set)))
# output_jlines.close()
# for key, value in sorted(people_dict.items(), key=operator.itemgetter(1),  reverse=True):
#     print(key, value)
#     if value <= 4:
#         exit()