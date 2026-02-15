"""StellarPulse - Kubernetes Collector."""

from typing import List, Optional
import asyncio
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)


class KubernetesCollector:
    """Kubernetes metrics collector."""

    def __init__(self, kubeconfig_path: Optional[str] = None):
        # Default to ~/.kube/config
        self.kubeconfig_path = kubeconfig_path or os.path.expanduser("~/.kube/config")
        self._client = None

    async def _get_client(self):
        """Get Kubernetes client."""
        if self._client is None:
            try:
                from kubernetes import client, config
                # Try to load kubeconfig
                try:
                    logger.info(f"Loading kubeconfig from: {self.kubeconfig_path}")
                    config.load_kube_config(config_file=self.kubeconfig_path)
                    logger.info("Kubeconfig loaded successfully")
                except Exception as e:
                    logger.warning(f"Failed to load kubeconfig: {e}")
                    # Try in-cluster config
                    try:
                        logger.info("Trying in-cluster config")
                        config.load_incluster_config()
                        logger.info("In-cluster config loaded successfully")
                    except Exception as e2:
                        logger.warning(f"Failed to load in-cluster config: {e2}")
                        raise RuntimeError(f"Cannot connect to Kubernetes: kubeconfig={e}, incluster={e2}")
                self._client = client
            except ImportError:
                raise RuntimeError("kubernetes client not installed: pip install kubernetes")
        return self._client

    async def get_nodes(self) -> List[dict]:
        """Get node metrics."""
        try:
            client = await self._get_client()
            v1 = client.CoreV1Api()
            nodes = v1.list_node()

            result = []
            for node in nodes.items:
                # Get CPU and memory
                cpu = node.status.capacity.get('cpu', '0')
                mem = node.status.capacity.get('memory', '0')
                alloc_cpu = node.status.allocatable.get('cpu', '0')
                alloc_mem = node.status.allocatable.get('memory', '0')

                # Calculate percentages (simplified)
                try:
                    cpu_cores = int(cpu)
                    alloc_cpu_cores = int(alloc_cpu)
                except:
                    cpu_cores = 1
                    alloc_cpu_cores = 1

                result.append({
                    "name": node.metadata.name,
                    "status": node.status.conditions[-1].type if node.status.conditions else "Unknown",
                    "cpu_cores": cpu_cores,
                    "memory_bytes": self._parse_memory(mem),
                    "allocatable": {
                        "cpu_cores": alloc_cpu_cores,
                        "memory_bytes": self._parse_memory(alloc_mem),
                    }
                })
            return result
        except Exception as e:
            return [{"error": str(e), "mock": True}]

    async def get_pods(self, namespace: str = None) -> List[dict]:
        """Get pod metrics."""
        try:
            client = await self._get_client()
            v1 = client.CoreV1Api()

            if namespace:
                pods = v1.list_namespaced_pod(namespace)
            else:
                pods = v1.list_pod_for_all_namespaces()

            result = []
            for pod in pods.items:
                result.append({
                    "name": pod.metadata.name,
                    "namespace": pod.metadata.namespace,
                    "status": pod.status.phase,
                    "node": pod.spec.node_name,
                    "ip": pod.status.pod_ip,
                    "restarts": sum(c.restart_count for c in pod.status.container_statuses or []),
                    "age": self._get_age(pod.metadata.creation_timestamp),
                })
            return result
        except Exception as e:
            return [{"error": str(e), "mock": True}]

    async def get_services(self, namespace: str = None) -> List[dict]:
        """Get service status."""
        try:
            client = await self._get_client()
            v1 = client.CoreV1Api()

            if namespace:
                services = v1.list_namespaced_service(namespace)
            else:
                services = v1.list_service_for_all_namespaces()

            result = []
            for svc in services.items:
                # Get endpoints
                try:
                    eps = v1.read_namespaced_endpoints(svc.metadata.name, svc.metadata.namespace)
                    endpoint_subsets = len(eps.subsets) if eps.subsets else 0
                except:
                    endpoint_subsets = 0

                result.append({
                    "name": svc.metadata.name,
                    "namespace": svc.metadata.namespace,
                    "type": svc.spec.type,
                    "cluster_ip": svc.spec.cluster_ip,
                    "ports": [{"port": p.port, "protocol": p.protocol} for p in (svc.spec.ports or [])],
                    "endpoints": endpoint_subsets,
                })
            return result
        except Exception as e:
            return [{"error": str(e), "mock": True}]

    async def get_namespaces(self) -> List[dict]:
        """Get namespaces."""
        try:
            client = await self._get_client()
            v1 = client.CoreV1Api()
            namespaces = v1.list_namespace()

            return [{"name": ns.metadata.name, "status": ns.status.phase}
                    for ns in namespaces.items]
        except Exception as e:
            return [{"error": str(e), "mock": True}]

    async def get_deployments(self, namespace: str = None) -> List[dict]:
        """Get deployments."""
        try:
            client = await self._get_client()
            apps_v1 = client.AppsV1Api()

            if namespace:
                deploys = apps_v1.list_namespaced_deployment(namespace)
            else:
                deploys = apps_v1.list_deployment_for_all_namespaces()

            result = []
            for deploy in deploys.items:
                result.append({
                    "name": deploy.metadata.name,
                    "namespace": deploy.metadata.namespace,
                    "replicas": deploy.spec.replicas,
                    "ready_replicas": deploy.status.ready_replicas or 0,
                    "available_replicas": deploy.status.available_replicas or 0,
                    "age": self._get_age(deploy.metadata.creation_timestamp),
                })
            return result
        except Exception as e:
            return [{"error": str(e), "mock": True}]

    def _parse_memory(self, mem_str: str) -> int:
        """Parse memory string to bytes."""
        if not mem_str:
            return 0
        mem_str = mem_str.strip()
        if mem_str.endswith('Ki'):
            return int(mem_str[:-2]) * 1024
        elif mem_str.endswith('Mi'):
            return int(mem_str[:-2]) * 1024 * 1024
        elif mem_str.endswith('Gi'):
            return int(mem_str[:-2]) * 1024 * 1024 * 1024
        elif mem_str.endswith('Ti'):
            return int(mem_str[:-2]) * 1024 * 1024 * 1024 * 1024
        try:
            return int(mem_str)
        except:
            return 0

    def _get_age(self, creation_timestamp) -> str:
        """Get resource age."""
        if not creation_timestamp:
            return "Unknown"
        delta = datetime.utcnow() - creation_timestamp
        days = delta.days
        if days > 0:
            return f"{days}d"
        hours = delta.seconds // 3600
        if hours > 0:
            return f"{hours}h"
        minutes = delta.seconds // 60
        return f"{minutes}m"


# Global collector instance
_k8s_collector = None


def get_k8s_collector() -> KubernetesCollector:
    """Get Kubernetes collector instance."""
    global _k8s_collector
    if _k8s_collector is None:
        _k8s_collector = KubernetesCollector()
    return _k8s_collector
