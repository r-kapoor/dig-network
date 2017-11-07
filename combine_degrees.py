import pickle
from string import ascii_lowercase
from collections import Counter

total_degree = None
for char in ['a', 'b', 'c', 'd']:
    for c in ascii_lowercase:
        filename = 'DictDegree'+char+c
        print("Read",filename)
        with open(filename, "rb") as fp:
            degree = pickle.load(fp)
            degree = Counter(degree)
            if total_degree is None:
                total_degree = degree
            else:
                total_degree = total_degree + degree

with open('CompleteDegree', 'wb') as f:
    pickle.dump(total_degree, f)