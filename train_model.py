import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

import pickle

# Load dataset
df = pd.read_csv("training_data.csv")

# Input and output
X = df["description"]
y = df["category"]

# Convert text into numbers
vectorizer = CountVectorizer()

X_vectorized = vectorizer.fit_transform(X)

# Train model
model = MultinomialNB()

model.fit(X_vectorized, y)

# Save model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model Trained Successfully!")
