# autoscaler/scalers/kafka_scaler.py
from autoscaler.scalers.base_scaler import BaseScaler
from kafka import KafkaConsumer

class KafkaScaler(BaseScaler):
    def __init__(self, config):
        super().__init__(config)
        self.topic = config.get("topic", "default-topic")
        self.broker = config.get("broker", "localhost:9092")
        self.threshold = config.get("threshold", 100)
        self.consumer = KafkaConsumer(self.topic, bootstrap_servers=self.broker, consumer_timeout_ms=1000)

    def should_scale(self):
        """Determine if scaling is needed based on message lag."""
        # Count messages in the topic
        lag = sum(1 for _ in self.consumer)
        # Reset consumer offset (for demo purposes)
        self.consumer.seek_to_beginning()
        return lag > self.threshold

    def get_replicas(self):
        lag = sum(1 for _ in self.consumer)
        self.consumer.seek_to_beginning()
        # Simple logic: 1 replica per 10 messages, capped at 10
        return min(max(1, lag // 10), 10)
