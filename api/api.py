from fastapi import FastAPI, HTTPException
from fastapi_socketio import SocketManager
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import IsolationForest

app = FastAPI()
sio = SocketManager(app=app)

# Load pre-trained scaling model (ensure this file is present)
MODEL_FILE = "scaling_model.pkl"
try:
    model = joblib.load(MODEL_FILE)
except Exception as e:
    raise HTTPException(status_code=500, detail="Scaling model not found.")

# Train anomaly detector (for demonstration, using synthetic data)
def train_anomaly_detector():
    normal_data = np.random.normal(loc=50, scale=10, size=(1000, 3))
    detector = IsolationForest(contamination=0.05)
    detector.fit(normal_data)
    return detector

anomaly_detector = train_anomaly_detector()

# Global variable for manual override
manual_override = None

def detect_anomaly(cpu, memory, events):
    sample = np.array([[cpu, memory, events]])
    score = anomaly_detector.decision_function(sample)[0]
    return score < -0.1

def mitigate_anomaly(cpu, memory, events, predicted_replicas):
    if cpu > 80 or memory > 80:
        return min(predicted_replicas + 2, 100)
    elif events > 200:
        return max(predicted_replicas - 2, 1)
    return predicted_replicas

def predict_replicas(cpu, memory, events):
    global manual_override
    if manual_override is not None:
        return manual_override, False
    now = datetime.now()
    hour = now.hour
    day = now.day
    input_data = pd.DataFrame([[cpu, memory, events, hour, day]],
                              columns=["cpu_usage", "memory_usage", "event_count", "hour", "day"])
    predicted = int(model.predict(input_data)[0])
    anomaly = detect_anomaly(cpu, memory, events)
    if anomaly:
        predicted = mitigate_anomaly(cpu, memory, events, predicted)
    return max(1, min(predicted, 100)), anomaly

@app.get("/predict")
def get_prediction(cpu: float, memory: float, events: int):
    replicas, anomaly = predict_replicas(cpu, memory, events)
    return {"predicted_replicas": replicas, "anomaly_detected": anomaly}

@app.post("/manual-override")
def set_manual_override(replicas: int):
    global manual_override
    manual_override = max(1, min(replicas, 100))
    return {"status": "Manual override set", "replicas": manual_override}

@app.delete("/manual-override")
def reset_manual_override():
    global manual_override
    manual_override = None
    return {"status": "Manual override cleared, AI in control"}

@sio.on("metrics_request")
async def send_metrics():
    # In a real scenario, fetch live metrics; here we simulate with random numbers
    cpu_usage = np.random.randint(10, 90)
    memory_usage = np.random.randint(10, 90)
    event_count = np.random.randint(1, 100)
    predicted, anomaly = predict_replicas(cpu_usage, memory_usage, event_count)
    await sio.emit("update_metrics", {
        "cpu": cpu_usage,
        "memory": memory_usage,
        "events": event_count,
        "predictedReplicas": predicted,
        "anomalyDetected": anomaly
    })
