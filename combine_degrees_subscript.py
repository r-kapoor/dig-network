import networkx as nx
import pickle
import os
import networkx as nx
from collections import Counter
import sys

print(sys.argv)
# DATA_PATH = '/data/split_name_hr/'
DATA_PATH = sys.argv[1]

# city, name, phone
# VARIABLE = 'city'
VARIABLE = sys.argv[2]
# hp or hr
# TYPE = 'hp'
TYPE = sys.argv[3]

total_degree = None
for (dirpath, dirnames, filenames) in os.walk(DATA_PATH):
    if(dirpath == DATA_PATH):
        for file in filenames:
            if file.startswith(VARIABLE+'_'+TYPE) and file.endswith('_degree'):
                filename = dirpath+file
                print("Reading:",filename)
                with open(filename, "rb") as fp:
                    degree = pickle.load(fp)
                    degree = Counter(degree)
                    if total_degree is None:
                        total_degree = degree
                    else:
                        total_degree = total_degree + degree

print("Writing Complete Degree")
with open(DATA_PATH + '/CompleteDegree'+'_'+VARIABLE+'_'+TYPE, 'wb') as f:
    pickle.dump(total_degree, f)