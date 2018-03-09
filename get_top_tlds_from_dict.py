import codecs
import json
import pickle
from operator import itemgetter 

with open('tld_dict.pkl', 'rb') as f:
    tld_dict = pickle.load(f)

# print(tld_dict)

for key, value in sorted(tld_dict.items(), key=itemgetter(1), reverse = True):
    print(key, value)