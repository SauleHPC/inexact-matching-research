import pandas as pd
from pymongo import MongoClient

# Load CSV file into a DataFrame
df = pd.read_csv('../data/inexact-matching-dataset.csv')

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["inexact-database"]
collection = db["inex"]
# Convert DataFrame to dictionary
data = df.to_dict(orient='records')
print("Converted to dictionary")
# Insert data into MongoDB
collection.insert_many(data)

print("CSV data has been uploaded to MongoDB")
