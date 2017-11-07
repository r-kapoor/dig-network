import pickle
import matplotlib.pyplot as plt

with open('readability_jaccard', "rb") as fp:
    jaccard = pickle.load(fp)

with open('readability_hp', 'rb') as f:
    similar_hp = pickle.load(f)

with open('readability_hr', 'rb') as f:
    similar_hr = pickle.load(f)

# with open('diff_len_phone.pkl', 'rb') as f:
    # diff_len = pickle.load(f)

plt.hist(jaccard)
plt.title("Jaccard")
plt.ylabel("count")
plt.xlabel("jaccard")
plt.show()
# plt.savefig("JaccardPhone.png")
plt.hist(similar_hp)
plt.title("Intersection/HP")
plt.ylabel("count")
plt.xlabel("values")
# plt.savefig("HighPrecisionPhone.png")
plt.show()
plt.hist(similar_hr)
plt.title("Intersection/HR")
plt.ylabel("count")
plt.xlabel("values")
# plt.savefig("HighRecallPhone.png")
plt.show()
# plt.hist(diff_len)
# plt.title("n(Union - Intersection)")
# plt.ylabel("count")
# plt.xlabel("values")
# plt.show()
# plt.savefig("DifferencePhone.png")
print(sum(jaccard)/len(jaccard))
print(sum(similar_hp)/len(similar_hp))
print(sum(similar_hr)/len(similar_hr))
# print(sum(diff_len)/len(diff_len))