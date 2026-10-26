
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)
import joblib
# Load the dataset
df = pd.read_csv("phishing_site_urls.csv")

# Find URLs that have more than one distinct label
label_counts = df.groupby("URL")["Label"].nunique()
conflicting_urls = label_counts[label_counts > 1].index

# Exclude conflicting URLs
df = df[~df["URL"].isin(conflicting_urls)]

# Remove repeated copies of the same URL
df = df.drop_duplicates(subset="URL")

print("Rows after cleaning:", len(df))
print("\nClass distribution:")
print(df["Label"].value_counts())

X = df["URL"]      # Input: URL text
y = df["Label"]    # Answer: good or bad

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining examples:", len(X_train))
print("Testing examples:", len(X_test))


model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            analyzer="char",
            ngram_range=(3, 5),
            min_df=2,
            max_features=200_000
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        )
    )
])

print("\nTraining model...")

model.fit(X_train, y_train)

print("Training complete!")


# Predict labels for unseen test examples
y_pred = model.predict(X_test)

print("\nACCURACY")
print(round(accuracy_score(y_test, y_pred), 4))

print("\nCLASSIFICATION REPORT")
print(classification_report(y_test, y_pred, zero_division=0))

print("\nCONFUSION MATRIX")
print("Rows = actual labels; columns = predicted labels")
print("Order: good, bad")
print(confusion_matrix(y_test, y_pred, labels=["good", "bad"]))

# Save the trained pipeline for our future web app
joblib.dump(model, "linkshield_model.joblib")

print("\nSaved model to linkshield_model.joblib")
