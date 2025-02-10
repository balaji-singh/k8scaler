from kubernetes import client, config

class KubeConfigManager:
    def __init__(self, clusters):
        """
        clusters: dict mapping cluster names to kubeconfig file paths
        e.g., {"cluster1": "/path/to/cluster1.kubeconfig", "cluster2": "/path/to/cluster2.kubeconfig"}
        """
        self.clusters = clusters

    def get_client(self, cluster_name):
        kubeconfig = self.clusters.get(cluster_name)
        if not kubeconfig:
            raise ValueError(f"Kubeconfig for {cluster_name} not found!")
        config.load_kube_config(config_file=kubeconfig)
        return client.AppsV1Api()
