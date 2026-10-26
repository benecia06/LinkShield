# LinkShield 🔐

**A machine-learning prototype for phishing URL detection.**

LinkShield analyzes URL patterns using a character-level TF-IDF vectorizer and Logistic Regression classifier to estimate whether a URL may be associated with phishing.

## Features

- Machine-learning-based URL classification
- Estimated phishing probability and configurable classification threshold
- Basic URL pattern flags
- Input validation for malformed or incomplete URLs
- FastAPI backend with interactive API documentation
- Responsive web interface
- Automated tests for API behavior and input validation

## Tech Stack

- **Language:** Python
- **Machine Learning:** scikit-learn, TF-IDF, Logistic Regression
- **Data Processing:** pandas
- **API:** FastAPI, Pydantic
- **Frontend:** HTML, CSS, JavaScript
- **Testing:** pytest, FastAPI TestClient

## Model

The training pipeline uses character-level TF-IDF features with character n-grams of lengths 3–5, followed by Logistic Regression with balanced class weights.

The dataset was cleaned by removing URLs associated with conflicting labels and deduplicating URLs before training. The data was split into training and testing sets using a stratified 80/20 split.

**Held-out test accuracy:** 94.15%

The model achieved a phishing-class recall of 92% and precision of 84% on the held-out test set.

## Run Locally

1. Clone or download this repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Ensure `linkshield_model.joblib` is present in the project root.
5. Start the application:

   ```bash
   python -m uvicorn app:app --reload
   ```

6. Open `http://127.0.0.1:8000/` in your browser.
7. Explore the API at `http://127.0.0.1:8000/docs`.

## Run Tests

```bash
python -m pytest -q
```

## Limitations

LinkShield is an educational prototype, not a production security service. It analyzes URL text and does not visit websites, verify domain reputation, or guarantee safety. Predictions may include false positives and false negatives. The displayed probability is a model estimate, not a calibrated guarantee of risk.

## Future Improvements

- Evaluate on an independent dataset to assess generalization
- Investigate false positives and false negatives
- Add more robust URL features and model comparisons
- Improve probability calibration and threshold selection
- Deploy the application with suitable model artifact and dependency limits

## Disclaimer

Do not rely on LinkShield alone to decide whether a URL is safe. Verify suspicious links using trusted security tools and sources.