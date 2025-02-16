import React, { useEffect, useState } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import io from "socket.io-client";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const API_URL = "http://localhost:8000";
const socket = io(API_URL);

function App() {
  const [cpu, setCpu] = useState(0);
  const [memory, setMemory] = useState(0);
  const [events, setEvents] = useState(0);
  const [predictedReplicas, setPredictedReplicas] = useState(1);
  const [anomaly, setAnomaly] = useState(false);
  const [manualReplicas, setManualReplicas] = useState("");
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      { label: "CPU Usage", data: [], borderColor: "blue", fill: false },
      { label: "Memory Usage", data: [], borderColor: "green", fill: false },
      { label: "Event Count", data: [], borderColor: "orange", fill: false },
      { label: "Predicted Replicas", data: [], borderColor: "red", fill: false }
    ]
  });

  useEffect(() => {
    socket.on("update_metrics", (data) => {
      setCpu(data.cpu);
      setMemory(data.memory);
      setEvents(data.events);
      setPredictedReplicas(data.predictedReplicas);
      setAnomaly(data.anomalyDetected);

      setChartData(prevData => ({
        ...prevData,
        labels: [...prevData.labels, new Date().toLocaleTimeString()],
        datasets: [
          { ...prevData.datasets[0], data: [...prevData.datasets[0].data, data.cpu] },
          { ...prevData.datasets[1], data: [...prevData.datasets[1].data, data.memory] },
          { ...prevData.datasets[2], data: [...prevData.datasets[2].data, data.events] },
          { ...prevData.datasets[3], data: [...prevData.datasets[3].data, data.predictedReplicas] }
        ]
      }));
    });
  }, []);

  const applyManualOverride = async () => {
    if (!manualReplicas) return;
    await axios.post(`${API_URL}/manual-override`, { replicas: Number(manualReplicas) });
  };

  const resetManualOverride = async () => {
    await axios.delete(`${API_URL}/manual-override`);
    setManualReplicas("");
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>K8Scaler Dashboard</h1>
      <div>
        <p>
          <strong>CPU:</strong> {cpu}% | <strong>Memory:</strong> {memory}% |{" "}
          <strong>Events:</strong> {events} | <strong>Predicted Replicas:</strong> {predictedReplicas}
        </p>
        {anomaly && (
          <p style={{ color: "red", fontWeight: "bold" }}>
            ⚠️ Anomaly detected! Please review metrics.
          </p>
        )}
      </div>
      <div style={{ margin: "20px 0" }}>
        <h2>Manual Scaling Override</h2>
        <input
          type="number"
          placeholder="Enter replica count"
          value={manualReplicas}
          onChange={(e) => setManualReplicas(e.target.value)}
        />
        <button onClick={applyManualOverride}>Apply Override</button>
        <button onClick={resetManualOverride}>Reset Override</button>
      </div>
      <div>
        <Line data={chartData} />
      </div>
    </div>
  );
}

export default App;
