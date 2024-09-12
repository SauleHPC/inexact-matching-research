from elasticsearch import Elasticsearch
import pandas as pd


#Connect to ElasticSearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

#Set name of the Elasticsearch index where documents will be kept
index_name = "original_strings"

#Create index
try:
    es.indices.create(index=index_name, ignore=400)
    print(f"Index '{index_name}' created.")
except Exception as e:
    print(f"Error creating index: {e}")

csv_file_path = "../data/the-advisor-match-10000.csv"
df = pd.read_csv(csv_file_path)

#Loop through strings that are the original strings in the data
for original_string in df['Original_String']:
    doc = {"original_string": original_string}
    try:
        es.index(index=index_name, body=doc)
    except Exception as e:
        print(f"Error indexing document: {e}")

#Fuzzy match to find best match in data.
def find_best_match(randomized_string):
    query = {
        "query": {
            "fuzzy": {
                "original_string": {
                    "value": randomized_string,
                    #AUTO: Automatically adjusts fuzziness based on length of search term
                    #"fuzziness": 1
                    "fuzziness": "AUTO" 
                }
            }
        }
    }
    #Search utilizing elastic search with the query through the original string column (index_name)
    try:
        result = es.search(index=index_name, body=query, size=1)
        #If we get a hit reurn the original string the random one matched with and the score with it
        if result['hits']['hits']:
            return result['hits']['hits'][0]['_source']['original_string'], result['hits']['hits'][0]['_score']
        else:
            return None, 0
    except Exception as e:
        print(f"Error searching for match: {e}")
        return None, 0

#Iterate over and find_best_match for the randomzied strings and apped all resutls
results = []
for randomized_string in df['Randomized_String'][0:10000]:
    match, score = find_best_match(randomized_string)
    results.append({
        "Randomized_String": randomized_string,
        "Matched_Original_String": match,
        "Score": score
    })

#Write results
results_df = pd.DataFrame(results)
output_csv_path = "matching_results_elasticsearch.csv"
results_df.to_csv(output_csv_path, index=False)

print(f"Results saved to {output_csv_path}")



