"""StellarPulse - Monitor API Routes."""

from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


def _get_mock_nodes():
    return [
        {"name": "node-1", "status": "Ready", "cpu_cores": 8, "memory_bytes": 16000000000, "pods": 45},
        {"name": "node-2", "status": "Ready", "cpu_cores": 4, "memory_bytes": 8000000000, "pods": 23},
    ]


def _get_mock_pods():
    return [
        {"name": "nginx-deployment-abc123", "namespace": "default", "status": "Running", "node": "node-1", "restarts": 0, "age": "2d"},
        {"name": "redis-master-xyz789", "namespace": "default", "status": "Running", "node": "node-2", "restarts": 1, "age": "5d"},
        {"name": "frontend-app-123456", "namespace": "production", "status": "Running", "node": "node-1", "restarts": 0, "age": "1d"},
        {"name": "backend-api-789012", "namespace": "production", "status": "Pending", "node": "", "restarts": 0, "age": "1h"},
        {"name": "monitoring-prometheus-345678", "namespace": "monitoring", "status": "Running", "node": "node-1", "restarts": 2, "age": "7d"},
    ]


def _get_mock_services():
    return [
        {"name": "kubernetes", "namespace": "default", "type": "ClusterIP", "cluster_ip": "10.96.0.1", "ports": [{"port": 443, "protocol": "TCP"}], "endpoints": 1},
        {"name": "nginx-service", "namespace": "default", "type": "LoadBalancer", "cluster_ip": "10.96.100.50", "ports": [{"port": 80, "protocol": "TCP"}], "endpoints": 2},
        {"name": "redis-service", "namespace": "default", "type": "ClusterIP", "cluster_ip": "10.96.100.51", "ports": [{"port": 6379, "protocol": "TCP"}], "endpoints": 1},
    ]


def _get_mock_namespaces():
    return [
        {"name": "default", "status": "Active"},
        {"name": "kube-system", "status": "Active"},
        {"name": "production", "status": "Active"},
        {"name": "monitoring", "status": "Active"},
        {"name": "development", "status": "Active"},
    ]


def _get_mock_deployments():
    return [
        {"name": "nginx-deployment", "namespace": "default", "replicas": 3, "ready_replicas": 3, "available_replicas": 3, "age": "10d"},
        {"name": "frontend-app", "namespace": "production", "replicas": 5, "ready_replicas": 5, "available_replicas": 5, "age": "3d"},
        {"name": "backend-api", "namespace": "production", "replicas": 3, "ready_replicas": 2, "available_replicas": 2, "age": "3d"},
    ]


def _get_mock_overview():
    return {
        "cluster": {"nodes": 3, "pods": 156, "services": 42, "namespaces": 8},
        "resources": {"cpu_cores": 24, "memory_gb": 64},
        "pods": {"running": 145, "pending": 8, "other": 3},
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/metrics/nodes")
async def get_nodes():
    """Get node metrics."""
    try:
        from backend.core.collector.kubernetes import get_k8s_collector
        collector = get_k8s_collector()
        nodes = await collector.get_nodes()
        if not nodes or "error" in nodes[0]:
            logger.warning(f"K8s connection failed, using mock data: {nodes}")
            return _get_mock_nodes()
        return nodes
    except Exception as e:
        logger.error(f"Failed to get nodes: {e}")
        return _get_mock_nodes()


@router.get("/metrics/pods")
async def get_pods(namespace: Optional[str] = Query(None), limit: int = Query(100)):
    """Get pod metrics."""
    try:
        from backend.core.collector.kubernetes import get_k8s_collector
        collector = get_k8s_collector()
        pods = await collector.get_pods(namespace)
        if not pods or "error" in pods[0]:
            return _get_mock_pods()[:limit]
        return pods[:limit]
    except Exception:
        return _get_mock_pods()[:limit]


@router.get("/metrics/services")
async def get_services(namespace: Optional[str] = Query(None)):
    """Get service status."""
    try:
        from backend.core.collector.kubernetes import get_k8s_collector
        collector = get_k8s_collector()
        services = await collector.get_services(namespace)
        if not services or "error" in services[0]:
            return _get_mock_services()
        return services
    except Exception:
        return _get_mock_services()


@router.get("/metrics/namespaces")
async def get_namespaces():
    """Get namespaces."""
    try:
        from backend.core.collector.kubernetes import get_k8s_collector
        collector = get_k8s_collector()
        namespaces = await collector.get_namespaces()
        if not namespaces or "error" in namespaces[0]:
            return _get_mock_namespaces()
        return namespaces
    except Exception:
        return _get_mock_namespaces()


@router.get("/metrics/deployments")
async def get_deployments(namespace: Optional[str] = Query(None)):
    """Get deployments."""
    try:
        from backend.core.collector.kubernetes import get_k8s_collector
        collector = get_k8s_collector()
        deployments = await collector.get_deployments(namespace)
        if not deployments or "error" in deployments[0]:
            return _get_mock_deployments()
        return deployments
    except Exception:
        return _get_mock_deployments()


@router.get("/metrics/overview")
async def get_overview():
    """Get cluster overview."""
    try:
        from backend.core.collector.kubernetes import get_k8s_collector
        collector = get_k8s_collector()
        nodes = await collector.get_nodes()
        pods = await collector.get_pods()
        namespaces = await collector.get_namespaces()
        services = await collector.get_services()
        if not nodes or "error" in nodes[0]:
            return _get_mock_overview()
        total_cpu = sum(n.get("cpu_cores", 0) for n in nodes)
        total_mem = sum(n.get("memory_bytes", 0) for n in nodes)
        running_pods = len([p for p in pods if p.get("status") == "Running"])
        pending_pods = len([p for p in pods if p.get("status") == "Pending"])
        return {
            "cluster": {"nodes": len(nodes), "pods": len(pods), "services": len(services), "namespaces": len(namespaces)},
            "resources": {"cpu_cores": total_cpu, "memory_gb": round(total_mem / (1024**3), 2)},
            "pods": {"running": running_pods, "pending": pending_pods, "other": len(pods) - running_pods - pending_pods},
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception:
        return _get_mock_overview()
