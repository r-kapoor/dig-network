import networkx as nx
import pickle

with open('backpage.com/nebraska.json', 'rb') as f:
    all_extraction_data = pickle.load(f)

extraction_to_ad_dict = dict()
EXTRACTION_TYPE = 'ground_truth'
for url , data in all_extraction_data.items():

    print(data)
    exit()
