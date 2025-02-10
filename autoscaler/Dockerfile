FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose any required ports (if using Prometheus metrics server, e.g., port 8000)
EXPOSE 8000

# Start the autoscaler service
CMD ["python", "autoscaler.py"]
