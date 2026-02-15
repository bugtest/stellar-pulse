"""Initialize database tables."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import database
import models

# Import all models to register them with Base
from models import AlertRule, Alert, Task, TaskRun, KnowledgeCategory, KnowledgeArticle, KnowledgeCase, Settings

print(f"Database URL: {database.DATABASE_URL}")
print(f"Tables: {list(database.Base.metadata.tables.keys())}")

# Create all tables
database.Base.metadata.create_all(bind=database.engine)

print("Database tables created successfully!")
