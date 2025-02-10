# scalers/base_scaler.py
class BaseScaler:
    def __init__(self, config):
        """Initialize scaler with configuration parameters."""
        self.config = config

    def should_scale(self):
        """Return True if scaling is required, else False."""
        raise NotImplementedError("Must implement should_scale()")

    def get_replicas(self):
        """Return the desired replica count."""
        raise NotImplementedError("Must implement get_replicas()")
