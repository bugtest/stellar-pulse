"""StellarPulse - Pydantic Schemas."""

from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, Field


# ==================== Alert Schemas ====================

class AlertRuleBase(BaseModel):
    """Base alert rule schema."""
    name: str
    description: Optional[str] = None
    enabled: bool = True
    metric_name: str
    condition: str
    threshold: float
    target_type: Optional[str] = None
    target_name: Optional[str] = None
    severity: str = "warning"
    channels: List[str] = []


class AlertRuleCreate(AlertRuleBase):
    """Create alert rule."""
    pass


class AlertRuleUpdate(BaseModel):
    """Update alert rule."""
    name: Optional[str] = None
    description: Optional[str] = None
    enabled: Optional[bool] = None
    metric_name: Optional[str] = None
    condition: Optional[str] = None
    threshold: Optional[float] = None
    target_type: Optional[str] = None
    target_name: Optional[str] = None
    severity: Optional[str] = None
    channels: Optional[List[str]] = None


class AlertRuleResponse(AlertRuleBase):
    """Alert rule response."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AlertBase(BaseModel):
    """Base alert schema."""
    title: str
    message: Optional[str] = None
    severity: str
    value: Optional[float] = None
    target_type: Optional[str] = None
    target_name: Optional[str] = None


class AlertResponse(AlertBase):
    """Alert response."""
    id: int
    rule_id: Optional[int]
    status: str
    acknowledged_by: Optional[str]
    acknowledged_at: Optional[datetime]
    resolved_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class AlertAcknowledge(BaseModel):
    """Acknowledge alert."""
    acknowledged_by: str


# ==================== Task Schemas ====================

class TaskBase(BaseModel):
    """Base task schema."""
    name: str
    description: Optional[str] = None
    task_type: str
    script: str
    script_type: str = "bash"
    schedule_type: str = "manual"
    cron_expression: Optional[str] = None
    interval_seconds: Optional[int] = None
    enabled: bool = True
    timeout: int = 300
    targets: List[str] = []


class TaskCreate(TaskBase):
    """Create task."""
    pass


class TaskUpdate(BaseModel):
    """Update task."""
    name: Optional[str] = None
    description: Optional[str] = None
    script: Optional[str] = None
    script_type: Optional[str] = None
    schedule_type: Optional[str] = None
    cron_expression: Optional[str] = None
    interval_seconds: Optional[int] = None
    enabled: Optional[bool] = None
    timeout: Optional[int] = None
    targets: Optional[List[str]] = None


class TaskResponse(TaskBase):
    """Task response."""
    id: int
    last_run_at: Optional[datetime]
    last_status: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskRunResponse(BaseModel):
    """Task run response."""
    id: int
    task_id: int
    status: str
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    duration: Optional[float]
    stdout: Optional[str]
    stderr: Optional[str]
    exit_code: Optional[int]
    triggered_by: str
    created_at: datetime

    class Config:
        from_attributes = True


class TaskRunCreate(BaseModel):
    """Create task run."""
    triggered_by: str = "manual"
    trigger_params: dict = {}


# ==================== Knowledge Schemas ====================

class KnowledgeCategoryBase(BaseModel):
    """Base knowledge category."""
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


class KnowledgeCategoryResponse(KnowledgeCategoryBase):
    """Category response."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class KnowledgeArticleBase(BaseModel):
    """Base knowledge article."""
    title: str
    content: str
    category_id: Optional[int] = None
    tags: List[str] = []
    author: Optional[str] = None


class KnowledgeArticleCreate(KnowledgeArticleBase):
    """Create article."""
    pass


class KnowledgeArticleUpdate(BaseModel):
    """Update article."""
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None


class KnowledgeArticleResponse(KnowledgeArticleBase):
    """Article response."""
    id: int
    views: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class KnowledgeCaseBase(BaseModel):
    """Base knowledge case."""
    title: str
    problem: str
    cause: Optional[str] = None
    solution: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = []


class KnowledgeCaseCreate(KnowledgeCaseBase):
    """Create case."""
    pass


class KnowledgeCaseResponse(KnowledgeCaseBase):
    """Case response."""
    id: int
    status: str
    views: int
    helpful_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Chat Schemas ====================

class ChatRequest(BaseModel):
    """Chat request."""
    message: str
    session_id: str = "web:direct"
    context: dict = {}


class ChatResponse(BaseModel):
    """Chat response."""
    message: str
    session_id: str
    timestamp: datetime


class DiagnoseRequest(BaseModel):
    """Diagnose request."""
    alert_id: Optional[int] = None
    target_type: Optional[str] = None
    target_name: Optional[str] = None
    symptoms: str


class DiagnoseResponse(BaseModel):
    """Diagnose response."""
    diagnosis: str
    root_cause: Optional[str]
    suggestions: List[str]
    related_cases: List[dict] = []


# ==================== Metrics Schemas ====================

class NodeMetrics(BaseModel):
    """Node metrics."""
    name: str
    status: str
    cpu_percent: float
    memory_percent: float
    memory_used: int
    memory_total: int
    pods: int
    cpu_allocatable: int
    cpu_capacity: int


class PodMetrics(BaseModel):
    """Pod metrics."""
    name: str
    namespace: str
    status: str
    node: str
    cpu_percent: float
    memory_percent: float
    restarts: int
    age: str


class ServiceStatus(BaseModel):
    """Service status."""
    name: str
    namespace: str
    type: str
    cluster_ip: str
    ports: List[dict]
    endpoints: int
    selector: dict = {}


class MetricsHistory(BaseModel):
    """Metrics history."""
    timestamps: List[datetime]
    values: List[float]
