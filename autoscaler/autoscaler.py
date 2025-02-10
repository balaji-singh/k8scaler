import importlib
import yaml
from kubernetes import client, config
import time
from prometheus_client import start_http_server, Gauge

scaled_pods = Gauge("autoscaler_scaled_pods", "Number of pods scaled")
last_scale_time = Gauge("autoscaler_last_scale_time", "Timestamp of last scale event")

start_http_server(8000)  # Exposes metrics on port 8000

config.load_incluster_config()
apps_v1 = client.AppsV1Api()
batch_v1 = client.BatchV1Api()

# Load scaler configurations
with open("scalers_config.yaml", "r") as f:
    scaler_configs = yaml.safe_load(f)

scalers = []
for scaler_name, config in scaler_configs.items():
    module = importlib.import_module(f"scalers.{config['module']}")
    scaler_class = getattr(module, config["class"])
    scalers.append(scaler_class(config))

def check_scaling():
    for scaler in scalers:
        if scaler.should_scale():
            replicas = scaler.get_replicas()
            scale_deployment("default", "my-app", replicas)


def scale_deployment(namespace, deployment_name, replicas):
    body = {"spec": {"replicas": replicas}}
    apps_v1.patch_namespaced_deployment_scale(deployment_name, namespace, body)
    print(f"Scaled {deployment_name} in {namespace} to {replicas} replicas.")


def create_job(namespace, job_name, image):
    job_manifest = {
        "apiVersion": "batch/v1",
        "kind": "Job",
        "metadata": {"name": job_name},
        "spec": {
            "template": {
                "metadata": {"labels": {"app": "autoscaled-job"}},
                "spec": {
                    "containers": [{"name": "worker", "image": image}],
                    "restartPolicy": "Never"
                }
            }
        }
    }
    batch_v1.create_namespaced_job(namespace, job_manifest)


def update_metrics(replicas):
    scaled_pods.set(replicas)
    last_scale_time.set(time.time())
