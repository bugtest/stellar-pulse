# CODEBUDDY.md

This file provides guidance to CodeBuddy Code when working with code in this repository.

## Project Overview

StellarPulse 是一个基于 nanobot 的企业级智能运维管理平台，集成 AI 能力实现智能化运维。

## 技术栈

- **后端**: FastAPI + SQLAlchemy + SQLite
- **前端**: React 18 + TypeScript + Ant Design 5 + Vite 5
- **AI**: Nanobot
- **监控**: Kubernetes API

## 常用命令

### 后端开发

```bash
# 安装依赖
cd backend
pip install -r requirements.txt

# 启动后端服务 (端口 8000)
uvicorn main:app --reload --port 8000

# 启动后端 (开发模式，监听所有接口)
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端开发

```bash
# 安装依赖
cd frontend
npm install

# 启动开发服务器 (端口 5173)
npm run dev

# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

## 项目结构

```
stellar_pulse/
├── backend/
│   ├── main.py              # FastAPI 应用入口
│   ├── database.py          # SQLAlchemy 数据库配置
│   ├── models.py           # SQLAlchemy 模型定义
│   ├── schemas.py          # Pydantic 请求/响应模型
│   ├── init_db.py          # 数据库初始化脚本
│   ├── api/
│   │   ├── routes.py        # 主路由 (alerts, tasks, knowledge, chat)
│   │   └── routes_monitors.py # Kubernetes 监控路由
│   ├── core/
│   │   └── collector/
│   │       └── kubernetes.py # Kubernetes 数据采集器
│   └── services/
│       ├── nanobot_client.py # Nanobot AI 客户端
│       └── diagnose.py       # AI 诊断服务
└── frontend/
    ├── src/
    │   ├── main.tsx         # React 入口
    │   ├── App.tsx          # 主应用组件 (路由 + 布局)
    │   ├── api/
    │   │   └── index.ts     # API 客户端 (axios)
    │   ├── pages/
    │   │   ├── Dashboard.tsx # 监控中心
    │   │   ├── Alerts.tsx   # 告警管理
    │   │   ├── Tasks.tsx    # 任务中心
    │   │   ├── Knowledge.tsx# 知识库
    │   │   ├── Chat.tsx     # AI 对话
    │   │   └── Settings.tsx # 系统设置
    │   └── index.css        # 全局样式
    ├── package.json
    ├── vite.config.ts
    └── tsconfig.json
```

## 核心功能模块

### 后端 API 路由 (`/api`)

- `/api/alerts` - 告警管理 (规则 CRUD、告警列表、确认)
- `/api/tasks` - 任务管理 (CRUD、手动执行、运行历史)
- `/api/knowledge` - 知识库 (文章、案例、分类)
- `/api/chat` - AI 对话 (与 Nanobot 交互)
- `/api/diagnose` - AI 故障诊断
- `/api/monitors` - Kubernetes 监控 (nodes, pods, services, deployments)

### 数据库模型

- `AlertRule` - 告警规则
- `Alert` - 告警实例
- `Task` / `TaskRun` - 任务与执行记录
- `KnowledgeCategory` / `KnowledgeArticle` / `KnowledgeCase` - 知识库
- `Settings` - 系统配置

### 前端页面路由

- `/` - 监控中心 (Dashboard)
- `/alerts` - 告警管理
- `/tasks` - 任务中心
- `/knowledge` - 知识库
- `/chat` - AI 对话
- `/settings` - 系统设置

## 开发注意事项

1. **数据库**: 当前使用 SQLite (`stellar_pulse.db`)，首次运行需调用 `init_db()` 初始化
2. **Kubernetes**: 采集器默认读取 `~/.kube/config`，也支持 in-cluster 模式
3. **AI 功能**: Nanobot 客户端在 `backend/services/nanobot_client.py`，当前为占位实现
4. **CORS**: 后端已配置允许所有来源的跨域请求
5. **前端 API**: 基础路径为 `http://localhost:8000/api`，在 `frontend/src/api/index.ts` 中配置

## 健康检查

- 后端健康端点: `GET /health`
- 根端点: `GET /`
