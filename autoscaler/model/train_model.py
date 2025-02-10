import sqlite3
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor

DB_FILE = "metrics.db"
MODEL_FILE = "scaling_model.pkl"

def train_model():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM metrics", conn)
    conn.close()

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    df["day"] = df["timestamp"].dt.day

    X = df[["cpu_usage", "memory_usage", "event_count", "hour", "day"]]
    y = df["cpu_usage"] * 10  # Example logic for replica count

    model = RandomForestRegressor(n_estimators=100)
    model.fit(X, y)
    joblib.dump(model, MODEL_FILE)
    print("Model trained and saved!")

train_model()
