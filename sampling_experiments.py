import json
import codecs
import tldextract
import pickle
import random
import copy
import matplotlib.pyplot as plt

# One of 'city', 'name', 'phone'
VARIABLE = 'phone'

with open('backpage.com/nebraska.json', "rb") as fp:
    urls = pickle.load(fp)

count = 0

def preprocess(urls):
    ad_to_extraction = dict()
    extraction_to_ad = dict()
    ad_extraction_pairs = list()
    ad_extraction_pairs_true = set()

    ad_id = 0

    for key, value in urls.items():
        if VARIABLE in value['ground_truth']:
            set_t = value['ground_truth'][VARIABLE]

        if VARIABLE in value['high_precision']:
            set_hr = value['high_precision'][VARIABLE]
        else:
            continue

        if len(set_hr) == 0:
            continue

        ad_to_extraction[ad_id] = set_hr

        for extraction in set_hr:
            if extraction in extraction_to_ad:
                extraction_to_ad[extraction].append(ad_id)
            else:
                extraction_to_ad[extraction] = [ad_id]

            ad_extraction_pairs.append((ad_id, extraction))

        for extraction in set_t:
            ad_extraction_pairs_true.add((ad_id, extraction))

        ad_id += 1

    return ad_to_extraction, extraction_to_ad, ad_extraction_pairs, ad_extraction_pairs_true

def sample_edges_directly(ad_extraction_pairs, num):
    return random.sample(ad_extraction_pairs, num)

def check_if_zero(dictionary):
    for key, values in dictionary.items():
        if len(values) == 0:
            print(key,":",values," EMPTY")
            exit()

def sample_edges_from_ads(ad_to_extraction, num):
    sampled_edges = list()
    ads_list = list(ad_to_extraction)
    if(num < len(ad_to_extraction)):
        # Need to sample just num ads and then 1 from each
        sampled_ads = random.sample(ads_list, num)
        for sampled_ad in sampled_ads:
            samples_extraction = random.choice(list(ad_to_extraction[sampled_ad]))
            sampled_edges.append((sampled_ad, samples_extraction))
    else:
        print("Num Out of Bounds Ads:", num)
        dict_copy = copy.deepcopy(ad_to_extraction)
        # check_if_zero(dict_copy)
        removal_list = list()
        # Sample 1 from each extraction without replacement
        for sampled_ad, extractions in dict_copy.items():
            # if len(dict_copy[sampled_ad]) == 0:
                # print(sampled_ad)
            sampled_extraction = random.choice(list(dict_copy[sampled_ad]))
            sampled_edges.append((sampled_ad, sampled_extraction))
            dict_copy[sampled_ad].remove(sampled_extraction)
            if len(dict_copy[sampled_ad]) == 0:
                removal_list.append(sampled_ad)

        for value in removal_list:
            del dict_copy[value]

        # check_if_zero(dict_copy)

        # Repeatedly sample
        while len(sampled_edges) < num:
            sampled_ad = random.choice(list(dict_copy))
            # if len(dict_copy[sampled_ad]) == 0:
                # print(sampled_ad)
            sampled_extraction = random.choice(list(dict_copy[sampled_ad]))
            sampled_edges.append((sampled_ad, sampled_extraction))
            dict_copy[sampled_ad].remove(sampled_extraction)
            if len(dict_copy[sampled_ad]) == 0:
                del dict_copy[sampled_ad]
    return sampled_edges

def sample_edges_from_extractions(extraction_to_ad, num):
    sampled_edges = list()
    extractions_list = list(extraction_to_ad)
    if num < len(extraction_to_ad):
        sampled_extractions = random.sample(extractions_list, num)
        for sampled_extraction in sampled_extractions:
            sampled_ad = random.choice(list(extraction_to_ad[sampled_extraction]))
            sampled_edges.append((sampled_ad, sampled_extraction))
    else:
        print("Num Out of Bounds Extrac:", num)
        dict_copy = copy.deepcopy(extraction_to_ad)
        removal_list = list()
        # Sample 1 from each extraction without replacement
        for sampled_extraction, ads in dict_copy.items():
            sampled_ad = random.choice(list(dict_copy[sampled_extraction]))
            sampled_edges.append((sampled_ad, sampled_extraction))
            dict_copy[sampled_extraction].remove(sampled_ad)
            if len(dict_copy[sampled_extraction]) == 0:
                removal_list.append(sampled_extraction)

        for value in removal_list:
            del dict_copy[value]

        # Repeatedly sample 
        while len(sampled_edges) < num:
            sampled_extraction = random.choice(list(dict_copy))
            sampled_ad = random.choice(list(dict_copy[sampled_extraction]))
            sampled_edges.append((sampled_ad, sampled_extraction))
            dict_copy[sampled_extraction].remove(sampled_ad)
            if len(dict_copy[sampled_extraction]) == 0:
                del dict_copy[sampled_extraction]

    return sampled_edges

def get_accuracy(ad_extraction_pairs_true, sampled_edges):
    correct_count = 0
    incorrect_count = 0
    for sampled_edge in sampled_edges:
        if sampled_edge in ad_extraction_pairs_true:
            correct_count += 1
        else:
            incorrect_count += 1

    return correct_count/(correct_count+incorrect_count)

ad_to_extraction, extraction_to_ad, ad_extraction_pairs, ad_extraction_pairs_true = preprocess(urls)

print("Num Ads:", len(ad_to_extraction))
print("Num Extr:", len(extraction_to_ad))
print("Number of True Ad Extraction pairs:", len(ad_extraction_pairs_true))
print("Number of HR Ad Extraction pairs:", len(ad_extraction_pairs))

SAMPLING_RATES = [0.01, 0.02, 0.05, 0.08, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
directly_accuracy = list()
extractions_accuracy = list()
ad_accuracy = list()

total_values = len(ad_extraction_pairs)
for rate in SAMPLING_RATES:
    num_to_sample = (int)(rate*total_values)
    print("Sampling ", num_to_sample, "at ", rate,  " rate")
    directly_accuracy_samples = list()
    extractions_accuracy_samples = list()
    ad_accuracy_samples = list()

    for iteration in range(5):
        print("Iteration:", iteration)
        directly_sampled_edges = sample_edges_directly(ad_extraction_pairs, num_to_sample)
        extractions_sampled_edges = sample_edges_from_extractions(extraction_to_ad, num_to_sample)
        ad_sampled_edges = sample_edges_from_ads(ad_to_extraction, num_to_sample)

        directly_accuracy_samples.append(get_accuracy(ad_extraction_pairs_true, directly_sampled_edges))
        extractions_accuracy_samples.append(get_accuracy(ad_extraction_pairs_true, extractions_sampled_edges))
        ad_accuracy_samples.append(get_accuracy(ad_extraction_pairs_true, ad_sampled_edges))

    directly_accuracy.append(sum(directly_accuracy_samples)/len(directly_accuracy_samples))
    extractions_accuracy.append(sum(extractions_accuracy_samples)/len(extractions_accuracy_samples))
    ad_accuracy.append(sum(ad_accuracy_samples)/len(ad_accuracy_samples))

print(directly_accuracy)
print(extractions_accuracy)
print(ad_accuracy)

true_accuracy = [directly_accuracy[len(directly_accuracy)-1]] * len(directly_accuracy)
plt.plot(SAMPLING_RATES, directly_accuracy, 'b-', label='Sample Edges Directly')
plt.plot(SAMPLING_RATES, extractions_accuracy, 'g-', label='Sample Extraction Nodes')
plt.plot(SAMPLING_RATES, ad_accuracy, 'r-', label='Sample from Ad Nodes')
plt.plot(SAMPLING_RATES, true_accuracy, 'k-', label='True')
plt.ylabel('Accuracy')
plt.xlabel('Sampling Rate')
plt.legend()
plt.show()


