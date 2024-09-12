from Parse import parse_file
from matchingProgram import matching_process, build_hash_table, write_to_csv

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
    mer_hash, paper_details = build_hash_table(k_value, file1, file1_key, top_mers_remove=num_removed_kmers)

    callback = [lambda obj: results.append(matching_process(k_value, mer_hash, levenshtein_candidates, paper_details, obj, file2_key, levenshteinThreshold, ratioThreshold))]
    parse_file(file2, file2_key, callback, 10000)
    
    if not all_arrays_empty(results):
        write_to_csv(results, 'the-advisor-match-10000.csv')
        return True
    return False

def all_arrays_empty(arrays):
    return all(not array for array in arrays)


k_mer = 3
file1 = "../data/inexact-matching-dataset.csv"
file1_key = "Randomized_String"
file1_path = '../data/inexact-matching-dataset.csv'

file2 = "../data/inexact-matching-dataset.csv"
file2_key = "Original_String"
file2_path ='../data/inexact-matching-dataset.csv'

num_removed_kmers = 30
fuzzy_match(k_mer, file1, file1_key, file2, file2_key, file1_path, file2_path, num_removed_kmers)