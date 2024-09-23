from Parse import parse_file
from matchingProgram import matching_process, build_hash_table, write_to_csv, make_graphs
import time
'''
script to execute matchingProgram used to paper querying
'''

#number of top candidates from k-mer matching to move on to levenhstein
#default = 5
levenshtein_candidates = 10


#parameter structure
#pip_command(file1, file2, k_value, written_file_name)

#----------------------------------------------------

'''
Have a levenshteinThreshold and ratioThreshold option.

Fro this to work take parameter name and set it equal in arguements.
'''

global results
def fuzzy_match(k_value, file1, file1_key, file2, file2_key, file1_path, file2_path, num_removed_kmers, levenshteinThreshold=0, ratioThreshold=0):
    results = []
    time1 = time.time()
    mer_hash, paper_details = build_hash_table(k_value, file1, file1_key, top_mers_remove=num_removed_kmers)
    time2 = time.time()
    print("Time to create hashmap ",time2-time1)

    callback = [lambda obj: results.append(matching_process(k_value, mer_hash, levenshtein_candidates, paper_details, obj, file2_key, levenshteinThreshold, ratioThreshold))]
    time3 = time.time()
    parse_file(file2, file2_key, callback, 10000)
    time4 = time.time()
    print("Time to peform matching",time4-time3)
    if not all_arrays_empty(results):
        write_to_csv(results, f'the-advisor-match-{k_value}-{num_removed_kmers}.csv')
        make_graphs(f'../data/the-advisor-match-{k_value}-{num_removed_kmers}.csv',f'theAdvior-k{k_value}-removedK{num_removed_kmers}')
        return True
    return False

def all_arrays_empty(arrays):
    return all(not array for array in arrays)


file2 = "../data/inexact-matching-dataset.csv"
file2_key = "Randomized_String"
file2_path = '../data/inexact-matching-dataset.csv'

file1 = "../data/inexact-matching-dataset.csv"
file1_key = "Original_String"
file1_path ='../data/inexact-matching-dataset.csv'

num_removed_kmers = [5000, 2500, 1200, 800, 400, 30]
num_kmers = [11, 9, 7, 5, 3]

for k_mer in num_kmers:
    for num_removed_kmer in num_removed_kmers:
        fuzzy_match(k_mer, file1, file1_key, file2, file2_key, file1_path, file2_path, num_removed_kmer)
