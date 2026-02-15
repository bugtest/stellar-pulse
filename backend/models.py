"""StellarPulse - SQLAlchemy Models."""

import os
import sys
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from backend.database import Base
except:
    from database import Base


# ==================== Alert Models ====================

class AlertRule(Base):
    """Alert rule model."""
    __tablename__ = "alert_rules"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    enabled = Column(Boolean, default=True)

    # Alert condition
    metric_name = Column(String(100), nullable=False)  # cpu, memory, pod_status, etc.
    condition = Column(String(50), nullable=False)  # gt, lt, eq, gte, lte
    threshold = Column(Float, nullable=False)

    # Target
    target_type = Column(String(50))  # node, pod, service
    target_name = Column(String(255))  # specific target or pattern

    # Notification
    severity = Column(String(20), default="warning")  # critical, warning, info
    channels = Column(JSON, default=list)  # ["dingtalk", "email"]

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    alerts = relationship("Alert", back_populates="rule")


class Alert(Base):
    """Alert instance model."""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    rule_id = Column(Integer, ForeignKey("alert_rules.id"))
    status = Column(String(20), default="firing")  # firing, resolved, acknowledged

    # Alert details
    title = Column(String(255))
    message = Column(Text)
    severity = Column(String(20))
    value = Column(Float)  # current metric value

    # Target info
    target_type = Column(String(50))
    target_name = Column(String(255))

    # Resolution
    acknowledged_by = Column(String(100))
    acknowledged_at = Column(DateTime)
    resolved_at = Column(DateTime)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    rule = relationship("AlertRule", back_populates="alerts")


# ==================== Task Models ====================

class Task(Base):
    """Task model."""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)

    # Task type
    task_type = Column(String(50), nullable=False)  # script, command, playbook

    # Task content
    script = Column(Text)  # script content or command
    script_type = Column(String(20))  # bash, python, ansible

    # Schedule
    schedule_type = Column(String(20))  # manual, cron, interval
    cron_expression = Column(String(100))
    interval_seconds = Column(Integer)

    # Execution
    enabled = Column(Boolean, default=True)
    timeout = Column(Integer, default=300)  # seconds
    last_run_at = Column(DateTime)
    last_status = Column(String(20))  # success, failed, running

    # Targets
    targets = Column(JSON, default=list)  # target servers/containers

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    runs = relationship("TaskRun", back_populates="task")


class TaskRun(Base):
    """Task execution record."""
    __tablename__ = "task_runs"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))

    # Execution info
    status = Column(String(20), default="pending")  # pending, running, success, failed
    started_at = Column(DateTime)
    finished_at = Column(DateTime)
    duration = Column(Float)  # seconds

    # Output
    stdout = Column(Text)
    stderr = Column(Text)
    exit_code = Column(Integer)

    # Trigger
    triggered_by = Column(String(50))  # manual, schedule, api
    trigger_params = Column(JSON)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    task = relationship("Task", back_populates="runs")


# ==================== Knowledge Models ====================

class KnowledgeCategory(Base):
    """Knowledge category."""
    __tablename__ = "knowledge_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("knowledge_categories.id"))

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    articles = relationship("KnowledgeArticle", back_populates="category")


class KnowledgeArticle(Base):
    """Knowledge article."""
    __tablename__ = "knowledge_articles"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("knowledge_categories.id"))

    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(JSON, default=list)

    # Metadata
    author = Column(String(100))
    views = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    category = relationship("KnowledgeCategory", back_populates="articles")


class KnowledgeCase(Base):
    """故障案例库"""
    __tablename__ = "knowledge_cases"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    problem = Column(Text, nullable=False)
    cause = Column(Text)
    solution = Column(Text)

    # 分类
    category = Column(String(100))
    tags = Column(JSON, default=list)

    # 状态
    status = Column(String(20), default="published")  # draft, published

    # 使用统计
    views = Column(Integer, default=0)
    helpful_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ==================== Settings Models ====================

class Settings(Base):
    """System settings."""
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), nullable=False, unique=True)
    value = Column(Text)
    value_type = Column(String(20), default="string")  # string, int, float, bool, json
    description = Column(Text)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
