import psycopg2
import pandas as pd

conn = psycopg2.connect(
    dbname="inexacttest",
    user="postgres",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

#Enable trigram matching used by fuzzy algorithm
cur.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

#Create table if it doesn't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS original_strings (
    id SERIAL PRIMARY KEY,
    original_string TEXT UNIQUE
);
""")
conn.commit()

#Load original string values into PostgreSQL
def load_original_strings(original_strings):
    for original_string in original_strings:
        cur.execute("INSERT INTO original_strings (original_string) VALUES (%s) ON CONFLICT DO NOTHING;", (original_string,))
    conn.commit()

#Function to find the fuzzy match of random string to its original
def find_best_match(randomized_string):
    #In our query we will use SIMILARITY(postgreSQL fuzzy key word) 
    # and fetch all matches >= 0 and then sort them and pick the top 1 (LIMIT 1)
    query = """
    SELECT original_string, SIMILARITY(original_string, %s) AS similarity
    FROM original_strings
    WHERE SIMILARITY(original_string, %s) >= 0
    ORDER BY similarity DESC
    LIMIT 1;
    """
    cur.execute(query, (randomized_string, randomized_string))
    result = cur.fetchone()
    return result if result else (None, 0)

csv_file_path = "../data/the-advisor-match-10000.csv"
df = pd.read_csv(csv_file_path)

load_original_strings(df['Original_String'].unique())

#Iterate over Randomized_String and find matches
results = []
for randomized_string in df['Randomized_String'][0:10000]:
    match, similarity = find_best_match(randomized_string)
    results.append({
        "Randomized_String": randomized_string,
        "Matched_Original_String": match,
        "Similarity": similarity
    })

results_df = pd.DataFrame(results)

output_csv_path = "matching_results_postresql.csv"
results_df.to_csv(output_csv_path, index=False)
print(f"Results saved to {output_csv_path}")

cur.close()
conn.close()
