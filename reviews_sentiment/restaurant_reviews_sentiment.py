import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# -------------------------------
# Step 3.1: Load the Dataset
# -------------------------------
# The file is tab-separated, so specify the delimiter.
df = pd.read_csv("Restaurant_Reviews.tsv", delimiter='\t')
print("First 5 rows of the dataset:")
print(df.head())

# Check the shape and basic info
print("\nDataset shape:", df.shape)
print(df.info())

# -------------------------------
# Step 3.2: Preprocess the Data
# -------------------------------
# For this simple example, we assume the dataset has two columns: 'Review' and 'Liked'
# 'Liked' is assumed to be 0 or 1 (0: Negative, 1: Positive)
# You could add further text cleaning here if needed (e.g., lowercasing, punctuation removal)
# For now, we'll keep it simple.

# -------------------------------
# Step 3.3: Split the Data into Training and Testing Sets
# -------------------------------
X = df['Review']         # Feature: review text
y = df['Liked']          # Label: sentiment (0 or 1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -------------------------------
# Step 3.4: Convert Text To Numerical Features
# -------------------------------
# Using TF-IDF Vectorizer to transform the text data
tfidf = TfidfVectorizer(stop_words='english', max_features=1500)
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

# -------------------------------
# Step 3.5: Train a Simple Classifier
# -------------------------------
classifier = LogisticRegression()
classifier.fit(X_train_tfidf, y_train)

# -------------------------------
# Step 3.6: Evaluate the Model
# -------------------------------
y_pred = classifier.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
print("\nModel Accuracy: {:.2f}%".format(accuracy * 100))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
