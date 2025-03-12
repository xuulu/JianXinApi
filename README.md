# 简心Api项目规范文档

简心API：https://api.qvqa.cn/

## 项目概述

本规范基于以下技术栈构建高可用全栈应用：

- **前端**：Vite + TypeScript + Ant Design 5.x等
- **后端**：FastAPI + Tortoise ORM + HTTPX + ORJSON等
- **部署**：Nginx + Gunicorn + uvicorn

---

## 环境准备

### 开发工具要求

| 工具      | 版本要求  | 说明     |
|---------|-------|--------|
| Node.js | ≥18.x | 前端开发环境 |
| Python  | ≥3.11 | 后端开发环境 |

---

## -前端规范 (Vite+TS+Antd)

```bash
# 创建Vite项目
npm create vite@latest

# 安装核心依赖
npm install
```

---

## -后端规范 (FastAPI+)

```bash
# Windows创建虚拟环境
python -m venv fastapi

# 激活环境
source /fastapi/bin/activate	

# 安装核心依赖
pip install -r requirements.txt

```
