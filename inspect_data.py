
import pandas as pd

df = pd.read_csv("phishing_site_urls.csv")

# 1. Check the number of examples in each class
print("LABEL DISTRIBUTION")
print(df["Label"].value_counts())

print("\nLABEL DISTRIBUTION (%)")
print((df["Label"].value_counts(normalize=True) * 100).round(2))

# 2. Check duplicate URLs
print("\nDUPLICATE URLS")
print("Total duplicate rows:", df.duplicated(subset=["URL"]).sum())

# 3. Check whether labels have extra spaces or unexpected values
print("\nUNIQUE LABELS")
print(df["Label"].unique())

print("\nMISSING VALUES")
print(df[["URL", "Label"]].isnull().sum())
