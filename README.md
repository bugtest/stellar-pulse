# StellarPulse - 智能运维管理平台

## 简介

基于nanobot打造的企业级智能运维管理平台，集成AI能力实现智能化运维。

## 功能特性

- 监控中心 - Kubernetes集群状态、Pod/Node指标
- 告警系统 - 规则引擎、多渠道通知
- 运维自动化 - 脚本执行、定时任务
- 故障诊断 - AI驱动的根因分析
- 知识库 - 文档管理+AI问答

## 快速开始

```bash
# 安装依赖
cd backend
pip install -r requirements.txt

# 启动后端
uvicorn main:app --reload --port 8000

# 启动前端
cd ../frontend
npm install
npm run dev
```

访问 http://localhost:5173

## 技术栈

- 后端: FastAPI + SQLAlchemy + SQLite
- 前端: React + TypeScript + Ant Design
- AI: Nanobot
- 监控: Kubernetes API
