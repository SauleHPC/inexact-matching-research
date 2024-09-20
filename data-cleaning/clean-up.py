import csv

def process_csv(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        rows = list(reader)
        
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            
            writer.writerow(rows[0])
            
            for row in rows[1:]:
                if row[0] == '':
                    row[0] = row[1]  
                    row[1] = '' 
                writer.writerow(row)

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

for paper in file_paths:
    process_csv(paper, paper)
