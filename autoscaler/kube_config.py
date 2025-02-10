from kubernetes import client, config

# Helper for multi-cluster Kubernetes client handling

def load_kube_config():
    config.load_kube_config()  # Load kube config from default location

# Additional functions to interact with Kubernetes clusters
