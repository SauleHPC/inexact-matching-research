from Levenshtein import distance, ratio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

method = ['theAdvisor', 'PostgreSQL','MongoDB','ElasticSearch']

file_paths = ['../data/the-advisor-match-all-1.csv', 
              '../postreSQL/matching_results_postresql.csv',
              '../mongoDB/matching_results_mongodb.csv',
              '../elasticSearch/elasticsearch_matching_results.csv']

output_file_paths = ['../graphs/the-advisor','../graphs/postgresql', '../graphs/mongodb', '../graphs/elasticsearch']

for i in range(len(file_paths)):
    data = pd.read_csv(file_paths[i])

    #print(data.head())
    
    data['Randomized_String'] = data['Randomized_String'].astype(str).fillna('')
    data['Original_String'] = data['Original_String'].astype(str).fillna('')

    #---------------------Levenshtein Ratio-----------------------------------


    data['Levenshtein_Ratio'] = data.apply(
        #lambda row: distance(row['Randomized_String'], row['Original_String']),
        lambda row: ratio(row['Randomized_String'], row['Original_String']),
        axis=1
    )

    data_sorted = data.sort_values(by='Levenshtein_Ratio').reset_index(drop=True)

    plt.figure(figsize=(10, 6))
    plt.plot(data_sorted.index, data_sorted['Levenshtein_Ratio'], marker='o', linestyle='-', color='b')
    plt.title('Levenshtein Ratio Over Sorted Dataset '+method[i])
    plt.xlabel('Index')
    plt.ylabel('Levenshtein Ratio')
    plt.grid(True)
    plt.savefig(output_file_paths[i]+'-levenshtein-ratio.png')

#---------------------Levenshtein Distance-----------------------------------

    data['Levenshtein_Distance'] = data.apply(
        lambda row: distance(row['Randomized_String'], row['Original_String']),
        #lambda row: ratio(row['Randomized_String'], row['Original_String']),
        axis=1
    )

    data_sorted = data.sort_values(by='Levenshtein_Distance').reset_index(drop=True)

    #print(data_sorted[['Randomized_String', 'Original_String', 'Levenshtein_Distance']])

    plt.figure(figsize=(10, 6))
    plt.plot(data_sorted.index, data_sorted['Levenshtein_Distance'], marker='o', linestyle='-', color='b')
    plt.title('Levenshtein Distance Over Sorted Dataset '+method[i])
    plt.xlabel('Index')
    plt.ylabel('Levenshtein Distance')
    plt.grid(True)
    plt.savefig(output_file_paths[i]+'-levenshtein-distance.png')
    print("Done")
