from parser import parse_DBLP_file
from callback import get_papers, totalPapers
from mixer import mix_characters
import csv


parse_DBLP_file([get_papers],0,200000000)

character_swap_dictionary1={'s':'t',
                           'a':'c',
                           'S':'T',
                           'A':'C'}

character_swap_dictionary2={'t':'s',
                           'e':'a',
                           'T':'S',
                           'E':'A'}

character_swap_dictionary3={'m':'i',
                           'n':'a',
                           'M':'I',
                           'N':'a'}

character_swap_dictionary_arr = [character_swap_dictionary1, character_swap_dictionary2, character_swap_dictionary3]

matched_dictionary = mix_characters(totalPapers, character_swap_dictionary_arr, 1.0)



def write_matched_dictionary_to_csv(matched_dictionary, filename='inexact-matching-dataset.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Randomized_String', 'Original_String']) 
        for key, value in matched_dictionary.items():
            writer.writerow([key, value])

write_matched_dictionary_to_csv(matched_dictionary)

