import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Levenshtein import distance, ratio

file_path = '../postreSQL/matching_results_postresql.csv' 
data = pd.read_csv(file_path)

#print(data.head())

data['Levenshtein_Distance'] = data.apply(
    #lambda row: distance(row['Randomized_String'], row['Original_String']),
    lambda row: ratio(row['Randomized_String'], row['Original_String']),
    axis=1
)

data_sorted = data.sort_values(by='Levenshtein_Distance').reset_index(drop=True)

#print(data_sorted[['Randomized_String', 'Original_String', 'Levenshtein_Distance']])

plt.figure(figsize=(10, 6))
plt.plot(data_sorted.index, data_sorted['Levenshtein_Distance'], marker='o', linestyle='-', color='b')
plt.title('Levenshtein Distance Over Sorted Dataset')
plt.xlabel('Index')
plt.ylabel('Levenshtein Distance')
plt.grid(True)
plt.savefig('levenshtein_distance_plot_postgreSQL.png')
print("Done")
