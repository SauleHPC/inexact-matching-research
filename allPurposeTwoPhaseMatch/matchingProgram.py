import random
from Parse import parse_file
from Kmer import query_selector,mer_hashtable, remove_top_k_mers, mer_builder,top_candidates_levenshtein, paper_details_population,repeating_kmer_study,matched_dblp_id_filter
import os, psutil
process = psutil.Process()
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import csv
from pathlib import Path

'''
@brief: used to build hashtable and then begin candidate process through function calls to k-mer
'''

'''
builds hashtable to hour dblp k-mer value and then ids with that k-mer

@param: k - k-mer value being used for hashing

@param: paper_limit - paper value that we want to go up to in building our hashmap around

@param: repeating_mers_remove - number of most frequently repeating k-mers we want removed

@param: top_mers_remove - removes the most frequent k-mer values in hashmap

@param: filter_out_matched - true/false as to whether the already matched papers should be filtered out

*note paramter is optional so that if the matched_file_path is not included the program will just skip over this
@param: matched_file_path - file path for the already matched MAG-DBLP papers
'''
def build_hash_table(k, file1, file1_key, top_mers_remove=10, file1_associated_attributes=None):
    #Create DBLP hashmap
    mer_hash = {}
    paper_details = {}

    arr_builder = lambda obj: mer_builder(obj, file1_key, k, False, False)

    #Build the mer_hash table for DBLP
    dblp_callbacks = [
        lambda current_obj: mer_hashtable(current_obj, mer_hash, arr_builder,[]),
        lambda current_obj: paper_details_population(current_obj, file1_key, paper_details),
    ]
    #Note by passing in 1000000000000 it assures the full size of the hashmap is created
    #to index from
    parse_file(file1, file1_key, dblp_callbacks,100000000000000,file1_associated_attributes)

    mer_hash = remove_top_k_mers(mer_hash, top_mers_remove)

    return mer_hash, paper_details




'''
the candidate matching process taking place

*note* many of these parameters are for field values for filling in the trial_results array

@param: k_value - the k-value we use to query

@param: dblp_hash_map - hashmap containing k-mer values and the ids associated with them

@param: num_removed_kmers - value of k-mers removed

@param: levenshtein_candidates - candidates used to move on to be evaluated in levenshtein process

@param: paper_details - details containing a papers ID - paper Title

@param: hashmap_build_time - build time of how long it took to build DBLP hashmap

@param: candidateTitle - title of the paper going through the matching process

@param: levenshteinThreshold - threshold that is the perctage of candidate with the most k-mers divided by length of the paper being queried. ie. should be a float b/t 0 and 1

@param: ratioThreshold - threshold that is the levenshtein ratio in order for there to be a match between a candidate and the paper being queried. ie. should be a float b/t 0 and 1
#
'''
successful_candidates= 0
total_candidates = 0

#k_value, mer_hash,levenshtein_candidates, paper_details, obj, levenshteinThreshold, ratioThreshold
def matching_process(k_value, mer_hash, levenshtein_candidates, paper_details,candidate,candidate_key, levenshteinThreshold, ratioThreshold):

    global successful_candidates, total_candidates
    trial_results = []

    query_result = query_selector(mer_hash, mer_builder(candidate, candidate_key, k_value, False, False))

    #extract the highest int value from the values part of the dictionary to give us the highest frequency match
    if(query_result.values()):
        highest_frequency = max(query_result.values())
    else:
        highest_frequency = 0


    #if highest frequency k-mer hashing candidate is 60% of the length of the candidate title we will go ahead with levenshtein

    if(len(getattr(candidate, candidate_key))>0 and (highest_frequency/len(getattr(candidate, candidate_key)))>levenshteinThreshold):
        top_matches = top_candidates_levenshtein(query_result, levenshtein_candidates, getattr(candidate, candidate_key), paper_details)

    else:
        #need to at least initialize the value so we don't throw an error below when checking the len of top_matches
        top_matches=[]

    correctMatch = None

    match = False
    #here we make sure that we have two candidates to compare and our best candidate has a levenshtein ratio
    #in the 2d array the indexes are as follows [id, frequency, levenshtein ratio, paper title]
    if top_matches and len(top_matches) > 0 and top_matches[0][2] > ratioThreshold:
        best_match_title = top_matches[0][3]
        match = True
    else:
        best_match_title = "None"

    if (match):
        #File 1
        trial_results.append((best_match_title))
        #File 2
        trial_results.append((getattr(candidate, candidate_key)))
        successful_candidates +=1

        

    return trial_results



def write_to_csv(data, filename):
    """
    Writes data to a CSV file with 'Randomized String' in the left column and 'Original String' in the right column.

    Parameters:
    - data: List of lists where each sub-list contains two elements [randomized_string, original_string].
    - filename: The name of the CSV file to write to.
    """
    header = ['Randomized_String', 'Original_String']

    directory = os.path.join('..', 'data') 

    os.makedirs(directory, exist_ok=True)

    file_path = os.path.join(directory, filename)

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)


