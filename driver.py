import networkx as nx
import pickle
import os
from threading import Thread
import networkx as nx

# DATA_PATH = '/data/split_name_hr/'
# DATA_PATH = '/data/backpage_only/'

# asexyservice.com
# eroticmugshots.com
# escortsincollege.com
# hoxnif.com
# liveescortreviews.com

DATA_PATH = 'asexyservice.com/'
# ENDING = '_backpage'
ENDING = '_degree'

# city, name, phone
VARIABLE = 'name'
# hp or hr
TYPE = 'hr'

NUMBER_OF_THREADS = 1

def batch_get_degree(list_of_files, batch_num):
    print("Spawned:", batch_num)
    # Process these files serially
    os.system('python get_degree_subscript.py ' + ' '.join(list_of_files))

all_files = set()
to_remove = set()
pattern = VARIABLE + '_' + TYPE
for (dirpath, dirnames, filenames) in os.walk(DATA_PATH):
    print(filenames)
    if(dirpath == DATA_PATH):
        for file in filenames:
            if file.startswith(VARIABLE+'_'+TYPE) and file != VARIABLE+'_'+TYPE:
                if file.endswith(ENDING):
                    print("To Remove:", dirpath+"/"+file[:-len(ENDING)])
                    to_remove.add(dirpath+"/"+file[:-len(ENDING)])
                else:
                    print(dirpath+"/"+file)
                    all_files.add(dirpath+"/"+file)
        break

all_files = all_files - to_remove
all_files = list(all_files)

print(all_files)

# exit()
length = len(all_files)
length_per_thread = length//NUMBER_OF_THREADS
curr = 0

all_threads = list()
while curr*length_per_thread < length:
    curr += 1
    start = (curr-1)*length_per_thread
    end = curr*length_per_thread
    print("Processing:", ((curr-1)*length_per_thread), ":", (curr*length_per_thread))
    list_of_files = all_files[((curr-1)*length_per_thread):(curr*length_per_thread)]
    thread_instance = Thread(target=batch_get_degree, args=(list_of_files, curr))
    all_threads.append(thread_instance)

for thread_instance in all_threads:
    thread_instance.start()

for thread_instance in all_threads:
    thread_instance.join()

print("All Threads Complete")
print("Starting Combining Degrees")

os.system('python combine_degrees_subscript.py '+DATA_PATH+' '+VARIABLE+' '+TYPE)