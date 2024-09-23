from Levenshtein import ratio
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

file_paths = [
    '../data/the-advisor-match-3-30.csv',
    '../data/the-advisor-match-3-400.csv',
    '../data/the-advisor-match-3-800.csv',
    '../data/the-advisor-match-3-1200.csv',
    '../data/the-advisor-match-3-2500.csv',
    '../data/the-advisor-match-3-5000.csv',
    '../data/the-advisor-match-5-30.csv',
    '../data/the-advisor-match-5-400.csv',
    '../data/the-advisor-match-5-800.csv',
    '../data/the-advisor-match-5-1200.csv',
    '../data/the-advisor-match-5-2500.csv',
    '../data/the-advisor-match-5-5000.csv',
    '../data/the-advisor-match-7-30.csv',
    '../data/the-advisor-match-7-400.csv',
    '../data/the-advisor-match-7-800.csv',
    '../data/the-advisor-match-7-1200.csv',
    '../data/the-advisor-match-7-2500.csv',
    '../data/the-advisor-match-7-5000.csv',
    '../data/the-advisor-match-9-30.csv',
    '../data/the-advisor-match-9-400.csv',
    '../data/the-advisor-match-9-800.csv',
    '../data/the-advisor-match-9-1200.csv',
    '../data/the-advisor-match-9-2500.csv',
    '../data/the-advisor-match-9-5000.csv',
    '../data/the-advisor-match-11-30.csv',
    '../data/the-advisor-match-11-400.csv',
    '../data/the-advisor-match-11-800.csv',
    '../data/the-advisor-match-11-1200.csv',
    '../data/the-advisor-match-11-2500.csv',
    '../data/the-advisor-match-11-5000.csv'
]

color_map = {
    '3': 'darkorange',
    '5': 'royalblue',
    '7': 'limegreen',
    '9': 'firebrick',
    '11': 'purple'
}

marker_map = {
    '30': 's',    
    '400': '^',     
    '800': 'o',     
    '1200': 'x',
    '2500': 'D',   
    '5000': '*'    
}
   
for file_path in file_paths:
    data = pd.read_csv(file_path)
    
    file_name = file_path.split('/')[-1].replace('.csv', '')
    parts = file_name.split('-')

    color = color_map.get(parts[3], 'black') 
    marker = marker_map.get(parts[4], 'o')  

    data['Randomized_String'] = data['Randomized_String'].astype(str).fillna('')
    data['Original_String'] = data['Original_String'].astype(str).fillna('')

    data['Levenshtein_Ratio'] = data.apply(
        lambda row: ratio(row['Randomized_String'], row['Original_String']),
        axis=1
    )
    data['Total_Time_Per_Query'] = data['Hash_Time_Per_Query'] + data['Leven_Time_Per_Query']
    avg_levenshtein_ratio = data['Levenshtein_Ratio'].mean()

    total_time = data['Total_Time_Per_Query'].sum()

    plt.scatter(total_time, avg_levenshtein_ratio, color=color, marker=marker, s=100)

    

plt.xlabel('Average Query Time')
plt.ylabel('Average Levenshtein Ratio')
plt.title('Levenshtein Ratio vs Time Per Query Across Parameters')

plt.xscale('log')

color_legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='3', markerfacecolor='darkorange', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='5', markerfacecolor='royalblue', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='7', markerfacecolor='limegreen', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='9', markerfacecolor='firebrick', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='11', markerfacecolor='purple', markersize=10)
]

shape_legend_elements = [
    Line2D([0], [0], marker='s', color='black', label='30', markersize=10, linestyle='None'),
    Line2D([0], [0], marker='^', color='black', label='400', markersize=10, linestyle='None'),
    Line2D([0], [0], marker='o', color='black', label='800', markersize=10, linestyle='None'),
    Line2D([0], [0], marker='x', color='black', label='1200', markersize=10, linestyle='None'),
    Line2D([0], [0], marker='D', color='black', label='2500', markersize=10, linestyle='None'),
    Line2D([0], [0], marker='*', color='black', label='5000', markersize=10, linestyle='None')
]
all_legend_elements = color_legend_elements + shape_legend_elements

plt.legend(handles=all_legend_elements, title="Legend", loc='upper center', 
           bbox_to_anchor=(0.5, -0.2), ncol=6)  

plt.tight_layout()

plt.grid(True)
plt.show()
