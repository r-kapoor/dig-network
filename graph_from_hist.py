import networkx as nx
import codecs
import json
import pickle
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from string import ascii_lowercase


histogram = None
for char in ['a', 'b', 'c', 'd']:
    for c in ascii_lowercase:
        filename = "hist"+char+c
        print("Reading:", filename)
        with open(filename, "rb") as fp:
            hist = pickle.load(fp)
            hist = np.array(hist)
            if histogram is None:
                histogram = hist
            else:
                if(histogram.shape[0] < hist.shape[0]):
                    histogram.resize(hist.shape)
                else:
                    hist.resize(histogram.shape)
                histogram = histogram + hist


with open('histogram', 'wb') as f:
    pickle.dump(histogram, f)

print(histogram)