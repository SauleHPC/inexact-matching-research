import pymongo
import pandas as pd

#Setup MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["inexact-database"]
collection = db["inex"]

#Create index original_string to hold the original string
collection.create_index([("original_string", "text")])

def find_best_match(randomized_string):
    #Query mongodb for textScore and take the highest textScore available 
    results = collection.find({"$text": {"$search": randomized_string}},{"original_string": 1, "_id": 0, "score": {"$meta": "textScore"}}
                                ).sort([("score", {"$meta": "textScore"})]).limit(1)

    #Convert the cursor to a list to check if any documents are present
    results_list = list(results)

    #If result_list is not empty return it else return None and 0
    if results_list:
        match = results_list[0]["original_string"]
        score = results_list[0]["score"]
        return match, score
    
    return None, 0

csv_file_path = "../data/the-advisor-match-10000.csv"
df = pd.read_csv(csv_file_path)

#Load original_string into MongoDB collection
def load_original_strings(original_strings):
    for original_string in original_strings:
        collection.update_one(
            {"original_string": original_string},
            {"$set": {"original_string": original_string}},
            upsert=True
        )

load_original_strings(df['Original_String'].unique())

#Iterate over randomzied strings to find matches
results = []
for randomized_string in df['Randomized_String'][0:10000]:
    match, score = find_best_match(randomized_string)
    results.append({
        "Randomized_String": randomized_string,
        "Matched_Original_String": match,
        "TextScore": score
    })

results_df = pd.DataFrame(results)
output_csv_path = "matching_results_mongodb.csv"
results_df.to_csv(output_csv_path, index=False)

print(f"Results saved to {output_csv_path}")

client.close()