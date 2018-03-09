import json
import codecs
import tldextract
import pickle

# One of 'city', 'name', 'phone'
VARIABLE = 'phone'

def normalize(city):
    return city.lower().replace(' ', '')

def normalize_list(city_list):
    city_normalized = set()
    for city in city_list:
        city_normalized.add(normalize(city))

    return city_normalized

def get_tp_fp_fn(set_t, set_a):
    tp = len(set_t & set_a)
    fp = len(set_a - set_t)
    fn = len(set_t - set_a)
    return tp, fp, fn

def get_system_metrics(metrics, set_t, set_actual):
    tp, fp, fn = get_tp_fp_fn(set_t, set_actual)
    metrics[1] += tp
    metrics[2] += fp
    metrics[3] += fn
    metrics[4] |= set_actual
    metrics[5] += len(set_actual)
    if(len(set_actual) == 0):
        metrics[6] += 1
    else:
        metrics[7] += 1



########## Creating common urls document ##############
# urls = dict()
# cities = set()
# names = set()
# phones = set()
# with codecs.open('/home/rkapoor/Documents/ISI/data/Network/intersecting-urls.jsonl', 'r', 'utf-8') as f:
#     for line in f:
#         doc = json.loads(line)
#         url = doc['url']
#         if url in urls:
#             ground_truth = urls[url]['ground_truth']
#             if 'city' in doc:
#                 cities.add(doc['city'])
#                 ground_truth['city'].add(doc['city'])
#             if 'name' in doc:
#                 names |= set(doc['name'])
#                 ground_truth['name'] |= set(doc['name'])
#             if 'phone' in doc:
#                 phones |= set(doc['phone'])
#                 ground_truth['phone'] |= set(doc['phone'])
#         else:
#             ground_truth = dict()
#             if 'city' in doc:
#                 cities.add(doc['city'])
#                 ground_truth['city'] = set()
#                 ground_truth['city'].add(doc['city'])
#             if 'name' in doc:
#                 names |= set(doc['name'])
#                 ground_truth['name'] = set(doc['name'])
#             if 'phone' in doc:
#                 phones |= set(doc['phone'])
#                 ground_truth['phone'] = set(doc['phone'])
#             urls[url] = {'ground_truth' : ground_truth}

# with codecs.open('backpage.com/intersecting.jl', 'r', 'utf-8') as f:
#     for line in f:
#         doc = json.loads(line)
#         url = doc['url']
#         if 'high_precision' in doc:
#             urls[url]['high_precision'] = doc['high_precision']
#             if 'city' in doc['high_precision']:
#                 doc['high_precision']['city'] = normalize_list(doc['high_precision']['city'])

#             if 'name' in doc['high_precision']:
#                 doc['high_precision']['name'] = normalize_list(doc['high_precision']['name'])

#             if 'phone' in doc['high_precision']:
#                 doc['high_precision']['phone'] = normalize_list(doc['high_precision']['phone'])


#         if 'high_recall' in doc:
#             urls[url]['high_recall'] = doc['high_recall']
#             if 'city' in doc['high_recall']:
#                 doc['high_recall']['city'] = normalize_list(doc['high_recall']['city'])

#             if 'name' in doc['high_recall']:
#                 doc['high_recall']['name'] = normalize_list(doc['high_recall']['name'])

#             if 'phone' in doc['high_recall']:
#                 doc['high_recall']['phone'] = normalize_list(doc['high_recall']['phone'])

# with open('backpage.com/nebraska.json', 'wb') as f:
#     pickle.dump(urls, f)

with open('backpage.com/nebraska.json', "rb") as fp:
    urls = pickle.load(fp)

count = 0
# [Name, tp, fp, fn, unique extractions, total extractions, ads with no extractions, ads with atleast 1 extraction]
system_metrics = [['t', 0, 0, 0, set(), 0, 0, 0], ['hp', 0, 0, 0, set(), 0, 0, 0], ['hr', 0, 0, 0, set(), 0, 0, 0], 
['hp_inter_t', 0, 0, 0, set(), 0, 0, 0], ['hr_inter_t', 0, 0, 0, set(), 0, 0, 0], ['hp_union_t', 0, 0, 0, set(), 0, 0, 0], 
['hr_union_t', 0, 0, 0, set(), 0, 0, 0]]

for key, value in urls.items():
    set_t = set()
    set_hp = set()
    set_hr = set()
    set_hp_inter_t = set()
    set_hr_inter_t = set()
    set_hp_union_t = set()
    set_hr_union_t = set()
    set_hp_inter_hr = set()
    set_hp_union_hr = set()

    if VARIABLE in value['ground_truth']:
        set_t = value['ground_truth'][VARIABLE]

    if VARIABLE in value['high_precision']:
        set_hp = value['high_precision'][VARIABLE]

    if VARIABLE in value['high_recall']:
        set_hr = value['high_recall'][VARIABLE]

    set_hp_inter_t = set_hp & set_t
    set_hr_inter_t = set_hr & set_t
    set_hp_union_t = set_hp | set_t
    set_hr_union_t = set_hr | set_t

    get_system_metrics(system_metrics[0], set_t, set_t)

    get_system_metrics(system_metrics[1], set_t, set_hp)

    get_system_metrics(system_metrics[2], set_t, set_hr)

    get_system_metrics(system_metrics[3], set_t, set_hp_inter_t)

    get_system_metrics(system_metrics[4], set_t, set_hr_inter_t)

    get_system_metrics(system_metrics[5], set_t, set_hp_union_t)

    get_system_metrics(system_metrics[6], set_t, set_hr_union_t)
    
    count += 1
    # if count == 100:
        # exit()


for values in system_metrics:
    print("-"*10,values[0],"-"*10)
    print(values[1],":",values[2],":",values[3])
    precision = values[1]/(values[1]+values[2])
    recall = values[1]/(values[1]+values[3])
    f_score = 2*precision*recall/(precision+recall)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F-score:",f_score)
    print("No. of unique extractions:",len(values[4]))
    print("Total Extractions:", values[5])
    print("Extractions/Ad:", values[5]/count)
    print("Ads with no extractions:", values[6])
    print("Ads with atleast 1 extraction:", values[7])
