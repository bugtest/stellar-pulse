"""StellarPulse Backend - API Routes."""

import os
import sys
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.database import get_db
from backend import models, schemas
from backend.api.routes_monitors import router as monitors_router

# Create main router
router = APIRouter()

# Include monitors router
router.include_router(monitors_router, tags=["monitor"])


# ==================== Alert Routes ====================

@router.get("/alerts/rules", response_model=List[schemas.AlertRuleResponse])
def get_alert_rules(db: Session = Depends(get_db)):
    """Get all alert rules."""
    return db.query(models.AlertRule).all()


@router.post("/alerts/rules", response_model=schemas.AlertRuleResponse)
def create_alert_rule(rule: schemas.AlertRuleCreate, db: Session = Depends(get_db)):
    """Create alert rule."""
    db_rule = models.AlertRule(**rule.model_dump())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule


@router.get("/alerts/rules/{rule_id}", response_model=schemas.AlertRuleResponse)
def get_alert_rule(rule_id: int, db: Session = Depends(get_db)):
    """Get alert rule by ID."""
    rule = db.query(models.AlertRule).filter(models.AlertRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule


@router.put("/alerts/rules/{rule_id}", response_model=schemas.AlertRuleResponse)
def update_alert_rule(rule_id: int, rule: schemas.AlertRuleUpdate, db: Session = Depends(get_db)):
    """Update alert rule."""
    db_rule = db.query(models.AlertRule).filter(models.AlertRule.id == rule_id).first()
    if not db_rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    for key, value in rule.model_dump(exclude_unset=True).items():
        setattr(db_rule, key, value)

    db.commit()
    db.refresh(db_rule)
    return db_rule


@router.delete("/alerts/rules/{rule_id}")
def delete_alert_rule(rule_id: int, db: Session = Depends(get_db)):
    """Delete alert rule."""
    db_rule = db.query(models.AlertRule).filter(models.AlertRule.id == rule_id).first()
    if not db_rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    db.delete(db_rule)
    db.commit()
    return {"message": "Rule deleted"}


@router.get("/alerts", response_model=List[schemas.AlertResponse])
def get_alerts(status: str = None, db: Session = Depends(get_db)):
    """Get alerts."""
    query = db.query(models.Alert)
    if status:
        query = query.filter(models.Alert.status == status)
    return query.order_by(models.Alert.created_at.desc()).all()


@router.post("/alerts/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: int, data: schemas.AlertAcknowledge, db: Session = Depends(get_db)):
    """Acknowledge alert."""
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.status = "acknowledged"
    alert.acknowledged_by = data.acknowledged_by
    alert.acknowledged_at = models.func.now()

    db.commit()
    return {"message": "Alert acknowledged"}


# ==================== Task Routes ====================

@router.get("/tasks", response_model=List[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    """Get all tasks."""
    return db.query(models.Task).all()


@router.post("/tasks", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Create task."""
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get task by ID."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """Update task."""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete task."""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted"}


@router.post("/tasks/{task_id}/run", response_model=schemas.TaskRunResponse)
def run_task(task_id: int, db: Session = Depends(get_db)):
    """Run task manually."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Create task run record
    task_run = models.TaskRun(
        task_id=task_id,
        status="running",
        triggered_by="manual"
    )
    db.add(task_run)
    db.commit()
    db.refresh(task_run)

    # TODO: Execute task asynchronously

    return task_run


@router.get("/tasks/{task_id}/runs", response_model=List[schemas.TaskRunResponse])
def get_task_runs(task_id: int, db: Session = Depends(get_db)):
    """Get task run history."""
    runs = db.query(models.TaskRun).filter(
        models.TaskRun.task_id == task_id
    ).order_by(models.TaskRun.created_at.desc()).all()
    return runs


# ==================== Knowledge Routes ====================

@router.get("/knowledge/articles", response_model=List[schemas.KnowledgeArticleResponse])
def get_articles(category_id: int = None, db: Session = Depends(get_db)):
    """Get knowledge articles."""
    query = db.query(models.KnowledgeArticle)
    if category_id:
        query = query.filter(models.KnowledgeArticle.category_id == category_id)
    return query.order_by(models.KnowledgeArticle.updated_at.desc()).all()


@router.post("/knowledge/articles", response_model=schemas.KnowledgeArticleResponse)
def create_article(article: schemas.KnowledgeArticleCreate, db: Session = Depends(get_db)):
    """Create knowledge article."""
    db_article = models.KnowledgeArticle(**article.model_dump())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


@router.get("/knowledge/cases", response_model=List[schemas.KnowledgeCaseResponse])
def get_cases(category: str = None, db: Session = Depends(get_db)):
    """Get knowledge cases."""
    query = db.query(models.KnowledgeCase)
    if category:
        query = query.filter(models.KnowledgeCase.category == category)
    return query.order_by(models.KnowledgeCase.created_at.desc()).all()


@router.post("/knowledge/cases", response_model=schemas.KnowledgeCaseResponse)
def create_case(kase: schemas.KnowledgeCaseCreate, db: Session = Depends(get_db)):
    """Create knowledge case."""
    db_case = models.KnowledgeCase(**kase.model_dump())
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case


@router.get("/knowledge/categories", response_model=List[schemas.KnowledgeCategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """Get knowledge categories."""
    return db.query(models.KnowledgeCategory).all()


# ==================== Chat Routes ====================

@router.post("/chat", response_model=schemas.ChatResponse)
async def chat(request: schemas.ChatRequest):
    """Chat with AI."""
    from datetime import datetime
    from backend.services.nanobot_client import chat_with_nanobot

    response = await chat_with_nanobot(request.message, request.session_id)

    return schemas.ChatResponse(
        message=response,
        session_id=request.session_id,
        timestamp=datetime.utcnow()
    )


@router.post("/diagnose", response_model=schemas.DiagnoseResponse)
async def diagnose(request: schemas.DiagnoseRequest):
    """AI诊断."""
    from backend.services.diagnose import diagnose_issue

    result = await diagnose_issue(
        alert_id=request.alert_id,
        target_type=request.target_type,
        target_name=request.target_name,
        symptoms=request.symptoms
    )

    return result
