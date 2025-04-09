import pandas as pd
import re
import string
import joblib
import tkinter as tk
from tkinter import messagebox
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Sample dataset (Replace with a larger dataset)
data = {
    "text": [
        "I love this product! It's amazing.",
        "This is the worst thing I've ever bought.",
        "Absolutely fantastic service, will buy again!",
        "I hate this so much, totally useless.",
        "Not bad, but could be better.",
        "Wow, this exceeded my expectations!",
        "Terrible experience, do not recommend.",
        "I am so angry right now!",
        "This made me incredibly happy!",
        "What a disappointing purchase.",
        "I'm feeling really excited about this!",
        "This is okay, nothing special.",
        "I'm frustrated beyond words.",
        "So boring, I almost fell asleep.",
        "This is a masterpiece!"
    ],
    "label": ["Happy", "Angry", "Happy", "Angry", "Neutral", "Excited", "Angry",
              "Angry", "Happy", "Sad", "Excited", "Neutral", "Frustrated", "Bored", "Happy"]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Text Preprocessing Function
def preprocess_text(text):
    text = text.lower()  
    text = re.sub(r'\d+', '', text)  
    text = text.translate(str.maketrans('', '', string.punctuation))  
    text = re.sub(r'\s+', ' ', text).strip()  
    return text

df['clean_text'] = df['text'].apply(preprocess_text)

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(df['clean_text'], df['label'], test_size=0.2, random_state=42)

# Convert text to numerical features using TF-IDF
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train Naive Bayes classifier
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# Model evaluation
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save model & vectorizer
joblib.dump(model, "emotion_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("Model and vectorizer saved!")

# Load model
model = joblib.load("emotion_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Emotion-based classification using keywords
emotion_dict = {
    "Happy": ["love", "awesome", "fantastic", "amazing", "great", "happy", "joy", "wonderful"],
    "Angry": ["hate", "worst", "terrible", "furious", "mad", "angry", "useless"],
    "Sad": ["disappoint", "bad", "upset", "depress", "miserable", "cry"],
    "Excited": ["wow", "excited", "thrilled", "fantastic", "adventure", "amazing"],
    "Neutral": ["okay", "fine", "normal", "not bad", "meh"],
    "Frustrated": ["annoy", "frustrated", "irritated", "ugh"],
    "Bored": ["boring", "sleepy", "dull", "yawn"]
}

# Function to detect emotion from text
def detect_emotion(text):
    words = text.split()
    for emotion, keywords in emotion_dict.items():
        if any(word in words for word in keywords):
            return emotion
    return "Neutral"

# GUI Functionality
def analyze_emotion():
    user_input = entry.get()
    if not user_input.strip():
        messagebox.showwarning("Warning", "Please enter some text!")
        return

    processed_text = preprocess_text(user_input)
    input_tfidf = vectorizer.transform([processed_text])
    prediction = model.predict(input_tfidf)[0]

    # Rule-based correction (if needed)
    detected_emotion = detect_emotion(processed_text)
    if detected_emotion != "Neutral":
        prediction = detected_emotion

    # Set result label
    emotion_map = {
        "Happy": ("😊", "green"),
        "Angry": ("😡", "red"),
        "Sad": ("😢", "blue"),
        "Excited": ("🤩", "orange"),
        "Neutral": ("😐", "gray"),
        "Frustrated": ("😠", "brown"),
        "Bored": ("🥱", "purple"),
    }

    emoji, color = emotion_map.get(prediction, ("❓", "black"))
    result_label.config(text=f"Emotion: {prediction} {emoji}", fg=color)

# GUI Setup
root = tk.Tk()
root.title("Emotion Detector")
root.geometry("420x280")
root.configure(bg="#1E1E1E")

# UI Elements
tk.Label(root, text="Enter text for emotion analysis:", font=("Arial", 12), bg="#1E1E1E", fg="white").pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

analyze_button = tk.Button(root, text="Analyze Emotion", command=analyze_emotion, bg="#FFCC00", fg="black")
analyze_button.pack(pady=10)
    
result_label = tk.Label(root, text="", font=("Arial", 14, "bold"), bg="#1E1E1E", fg="white")
result_label.pack(pady=10)

# Run GUI
root.mainloop()
