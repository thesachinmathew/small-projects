import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import os

# Reduce TensorFlow resource usage
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
tf.config.threading.set_inter_op_parallelism_threads(2)
tf.config.threading.set_intra_op_parallelism_threads(2)

# Load dataset
data_path = "F:/geodata.csv"
df = pd.read_csv(data_path)

# Assuming last column is the target variable
y = df.iloc[:, -1]
X = df.iloc[:, :-1]

# Normalize data
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train Random Forest
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

# Train LSTM
X_train_lstm = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test_lstm = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
    LSTM(50),
    Dense(1)
])

model.compile(optimizer='adam', loss='mse')
model.fit(X_train_lstm, y_train, epochs=10, batch_size=8, verbose=1)
y_pred_lstm = model.predict(X_test_lstm).flatten()

# Calculate metrics
def calculate_metrics(y_true, y_pred):
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "MSE": mean_squared_error(y_true, y_pred),
        "R2 Score": r2_score(y_true, y_pred)
    }

metrics_rf = calculate_metrics(y_test, y_pred_rf)
metrics_lstm = calculate_metrics(y_test, y_pred_lstm)

# GUI using Tkinter
def show_graph():
    plt.figure(figsize=(10, 5))
    plt.plot(y_test.values, label='Actual', color='blue')
    plt.plot(y_pred_rf, label='Random Forest Prediction', color='green')
    plt.plot(y_pred_lstm, label='LSTM Prediction', color='red')
    plt.legend()
    plt.xlabel("Samples")
    plt.ylabel("Target Value")
    plt.title("Model Comparison")
    plt.show()

def show_metrics():
    result_text.set(f"Random Forest - R2: {metrics_rf['R2 Score']:.2f}\nLSTM - R2: {metrics_lstm['R2 Score']:.2f}")

root = tk.Tk()
root.title("Model Comparison")
root.geometry("400x300")

result_text = tk.StringVar()
result_label = ttk.Label(root, textvariable=result_text, font=("Arial", 12))
result_label.pack(pady=10)

metrics_button = ttk.Button(root, text="Show Metrics", command=show_metrics)
metrics_button.pack(pady=5)

graph_button = ttk.Button(root, text="Show Graph", command=show_graph)
graph_button.pack(pady=5)

root.mainloop()
