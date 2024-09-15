import pymongo
import pandas as pd
import time

#Setup MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["inexact-database-new"]
collection = db["inex-new"]

# Create the new index
collection.create_index([("Original_String", "text")])

print("connected")

def find_best_match(randomized_string):
    #Query mongodb for textScore and take the highest textScore available 
    results = collection.find({"$text": {"$search": randomized_string}},{"Original_String": 1, "_id": 0, "score": {"$meta": "textScore"}}
                                ).sort([("score", {"$meta": "textScore"})]).limit(1)
    
    #Convert the cursor to a list to check if any documents are present
    results_list = list(results)
    #If result_list is not empty return it else return None and 0
    if results_list:
        match = results_list[0]["Original_String"]
        score = results_list[0]["score"]
        return match, score
    
    return None, 0


csv_file_path = "../data/inexact-matching-dataset.csv"
df = pd.read_csv(csv_file_path)

data = df.to_dict(orient='records')
print("Converted to dictionary")
# Insert data into MongoDB
time1 = time.time()
collection.insert_many(data)
time2 = time.time()

print("Time taken to populate database ",time2-time1)

print("Database information")
databases = client.list_database_names()
print("Databases:", databases)

# Replace 'inexact-database-new' with the correct database name
database = client["inexact-database-new"]
collections = database.list_collection_names()
print("Collections:", collections)

# Replace 'inex-new' with the correct collection name
collection = database["inex-new"]

# Check for existing documents
count = collection.count_documents({})
print(f"Number of documents in collection: {count}")

# Verify field existence
for doc in collection.find({"Original_String": {"$exists": True}}, {"Original_String": 1, "_id": 0}).limit(5):
    print(doc)

#Iterate over randomzied strings to find matches
results = []
time3=time.time()
for randomized_string in df['Randomized_String'][0:10000]:
    match, score = find_best_match(randomized_string)
    results.append({
        "Randomized_String": randomized_string,
        "Matched_Original_String": match,
        "TextScore": score
    })
time4 = time.time()
print("Time to make queries ",time4-time3) 
results_df = pd.DataFrame(results)
output_csv_path = "matching_results_mongodb.csv"
results_df.to_csv(output_csv_path, index=False)

print(f"Results saved to {output_csv_path}")

client.close()
