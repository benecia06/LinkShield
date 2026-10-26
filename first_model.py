print("LinkShield script started!")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Tiny practice dataset — examples for learning only
urls = [
    "https://www.wikipedia.org",
    "https://www.python.org",
    "https://www.openai.com",
    "https://github.com",
    "http://secure-login-account-verify.example.com",
    "http://free-prize-winner.example.com",
    "http://account-password-confirm.example.com",
    "http://urgent-bank-security.example.com",
]

# 0 = legitimate, 1 = phishing-like
labels = [0, 0, 0, 0, 1, 1, 1, 1]

model = Pipeline([
    ("tfidf", TfidfVectorizer(analyzer="char", ngram_range=(3, 5))),
    ("classifier", LogisticRegression()),
])

model.fit(urls, labels)

test_url = "http://urgent-account-verify.example.com"
prediction = model.predict([test_url])[0]

if prediction == 1:
    print("Prediction: Phishing-like URL")
else:
    print("Prediction: Legitimate-like URL")

print("Practice prediction complete!")
