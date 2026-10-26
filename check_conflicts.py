
import pandas as pd

# Load the dataset
df = pd.read_csv("phishing_site_urls.csv")

# Count how many distinct labels each URL has
label_counts = df.groupby("URL")["Label"].nunique()

# Keep URLs that have more than one label
conflicting_urls = label_counts[label_counts > 1]

# Display the results
print("Total URL rows:", len(df))
print("Conflicting URL groups:", len(conflicting_urls))

print("\nFirst 10 conflicting URL groups:")
print(conflicting_urls.head(10))

# Show the actual rows for those conflicts
if len(conflicting_urls) > 0:
    conflict_examples = df[df["URL"].isin(conflicting_urls.index)]

    print("\nExample conflicting records:")
    print(conflict_examples.head(20).to_string(index=False))
else:
    print("\nNo conflicting labels found.")
