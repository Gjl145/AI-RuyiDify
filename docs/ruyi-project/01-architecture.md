# 01 · 项目架构分析

> **最后更新**: 2026-07-15
> **源码分析日期**: 2026-07-15
> **分析方式**: 文件系统扫描 + 源码定点阅读 + Docker 实机验证

---

## 1. 项目定位

RuyiDify 是基于 **Dify v1.15.0** 的实战教学项目。核心代码（api/web/docker/dify-agent）来自 Dify 上游，**RuyiDify 的独特价值**在于：

| 层面 | 内容 | 目录 |
|------|------|------|
| 教学文档 | 知识库开发 PPT 素材 + 专题笔记 | `docs/资料/知识库开发入门/` |
| 博客 | 张大鹏第一人称实战博客 6 篇 | `docs/博客/` |
| 示例代码 | 29 个 Python 知识库 API 示例 | `examples/知识库/` |
| AI 辅助 | Claude/Codex/Hermes skill 配置 | `.claude/` `.codex/` `.agents/` |

**核心理念**（引自 `docs/博客/003_*.md`）：知识库不是上传文件这么简单，而是一条 RAG 工程链路。

---

## 2. 技术栈

| 层面 | 技术 | 版本/说明 |
|------|------|-----------|
| 后端 API | Python + Flask (DDD 分层) | `api/pyproject.toml`: requires-python ~=3.12.0 |
| 包管理 | uv | `api/AGENTS.md` L99 |
| 代码质量 | Ruff (format/lint) | `api/.ruff.toml` |
| 前端 Web | Next.js + TypeScript + React | `web/package.json`: dify-web v1.15.0 |
| UI 框架 | Tailwind CSS + @langgenius/dify-ui | `packages/dify-ui/` |
| 状态管理 | Jotai + TanStack Query | `web/AGENTS.md` L33-38 |
| 前端包管理 | pnpm | `pnpm-workspace.yaml` |
| 代码质量 | ESLint | `web/AGENTS.md` L3 |
| 异步任务 | Celery + Redis broker | `api/tasks/`, `docker/.env.example` L120 |
| 数据库 | PostgreSQL 15 (默认) / MySQL 8.0 | `docker-compose.yaml` L417-501 |
| 缓存/消息 | Redis 6 | `docker-compose.yaml` L484-499 |
| 向量数据库 | Weaviate 1.27.0（默认），支持 20+ 种 | `docker/.env.example` L164-183 |
| 对象存储 | OpenDAL (fs 模式本地) | `api/.env.example` L114-118 |
| 代码沙箱 | DifySandbox 0.2.15 | `docker-compose.yaml` L502-504 |
| Agent 运行时 | dify-agent 0.1.0 (Go + Python) | `dify-agent/pyproject.toml` |
| 可观测性 | OpenTelemetry | `api/pyproject.toml` L36-42 |
| 反向代理 | Nginx | `docker-compose.yaml` L665-699 |

---

## 3. 目录职责

### 3.1 核心目录

| 目录 | 行属 | 规模 | 职责 |
|------|:----:|:----:|------|
| `api/` | Dify 原生 | 1,487 .py | Flask 后端，DDD + Clean Architecture |
| `api/models/` | Dify 原生 | 28 .py | SQLAlchemy ORM 模型（Dataset/Document/Segment 等） |
| `api/controllers/` | Dify 原生 | 236 .py | Flask-RESTX 路由（console + service_api） |
| `api/services/` | Dify 原生 | 233 .py | 业务逻辑层 |
| `api/core/` | Dify 原生 | 611 .py | 领域核心（RAG/Agent/Workflow/Model） |
| `api/tasks/` | Dify 原生 | 62 .py | Celery 异步任务 |
| `api/configs/` | Dify 原生 | — | 统一配置入口（禁止直接读 env） |
| `web/` | Dify 原生 | 6,266 .ts/.tsx | Next.js 前端 + 23 种语言 i18n |
| `docker/` | Dify 原生 | 36 env 模板 | Docker Compose 部署 |
| `dify-agent/` | Dify 原生 | — | Agent 后端（AgentOn 框架 + Pydantic AI） |

### 3.2 RuyiDify 扩展目录

| 目录 | 职责 |
|------|------|
| `docs/资料/知识库开发入门/` | 7 份教学专题笔记（切分、检索调参、元数据、外部 API、PPT 规划） |
| `docs/博客/` | 6 篇第一人称实战博客 |
| `docs/ruyi-project/` | **本项目维护文档**（你正在读的这套） |
| `examples/知识库/` | 29 个 Python 示例脚本 |
| `.claude/` `.codex/` `.agents/` | AI 编码助手 skill 配置 |
| `.codegraph/` | CodeGraph 代码关系图谱（需 git 仓库） |

---

## 4. 运行架构

### 4.1 Docker Compose 拓扑

```
                        ┌─────────────────┐
                        │   Nginx :80     │ ← 用户入口
                        └───────┬─────────┘
                                │
               ┌────────────────┼────────────────┐
               ▼                ▼                 ▼
      ┌────────────┐   ┌──────────────┐   ┌──────────────┐
      │  api :5001 │   │ web (Next.js)│   │ api_websocket│
      │  (Flask)   │   │  SSR → api   │   │ (协作模式)    │
      └──────┬─────┘   └──────────────┘   └──────────────┘
             │
      ┌──────┼──────────┬──────────────┬──────────────┐
      ▼      ▼          ▼              ▼              ▼
   ┌──────┐ ┌──────┐ ┌────────┐ ┌──────────┐ ┌───────────┐
   │Redis │ │PG 15 │ │Weaviate│ │ Sandbox  │ │Plugin     │
   │      │ │      │ │1.27.0  │ │(代码执行)│ │Daemon:5003│
   └──────┘ └──────┘ └────────┘ └──────────┘ └───────────┘
      ▲
      │ (Celery broker)
   ┌──┴──────────────┐
   │ worker          │ ← Celery Worker (dataset/workflow/mail 队列)
   │ worker_beat     │ ← Celery Beat (周期任务调度)
   └─────────────────┘
```

> 来源: `docker/docker-compose.yaml`, 实机验证通过 ✅

### 4.2 一次知识库请求的完整路径

```
用户 (浏览器 / API 客户端)
  │
  ▼
Nginx (:80 反向代理)
  ├─ /console/api/* → api:5001    (管理后台)
  ├─ /v1/*          → api:5001    (Service API / 知识库 API)
  └─ /*             → web:3000    (Next.js SSR)
  │
  ▼
Flask API (api:5001)
  │  app_factory.py → create_flask_app_with_configs()
  │  configs/dify_config → 统一配置（禁止直接读 env）
  │
  ├─ 控制台路由:  controllers/console/datasets/
  │     datasets.py           (知识库 CRUD)
  │     datasets_document.py  (文档管理)
  │     datasets_segments.py  (分段管理)
  │     metadata.py           (元数据字段)
  │     hit_testing.py        (检索命中测试)
  │
  └─ Service API: controllers/service_api/dataset/
        dataset.py   (外部 API 知识库管理)
        document.py  (外部 API 文档操作)
        segment.py   (外部 API 分段操作)
        metadata.py  (外部 API 元数据)
  │
  ▼
Service 层 (services/dataset_service.py, 4,341 行)
  │  DatasetService / DocumentService / DatasetPermissionService
  │
  ├─ 同步: SQLAlchemy → PostgreSQL
  │    models/dataset.py (1,797 行)
  │    - Dataset, Document, DocumentSegment, ChildChunk
  │    - DatasetProcessRule, DatasetCollectionBinding
  │
  └─ 异步: Celery task → Redis → worker
       tasks/document_indexing_task.py       (索引入队)
       tasks/add_document_to_index_task.py   (写入向量库)
       tasks/create_segment_to_index_task.py (单分段索引)
  │
  ▼
Core RAG 层 (core/rag/)
  ├─ core/indexing_runner.py                → 索引编排器 (855行)
  ├─ core/rag/extractor/                    → 文档提取 (PDF/MD/HTML/CSV/Excel/Notion)
  ├─ core/rag/splitter/                     → 文本切分 (RecursiveCharacterTextSplitter)
  ├─ core/rag/embedding/                    → 向量嵌入
  ├─ core/rag/datasource/vdb/               → 向量数据库访问 (20+ 后端)
  ├─ core/rag/datasource/keyword/           → 关键词检索 (jieba)
  ├─ core/rag/datasource/retrieval_service.py → 检索服务 (970行)
  ├─ core/rag/rerank/                       → 重排序
  ├─ core/rag/data_post_processor/          → 检索后处理
  └─ core/rag/entities/                     → 实体定义
```

### 4.3 关键架构决策

| 决策 | 说明 | 来源 |
|------|------|------|
| DDD 分层 | controller → service → core/task/model | `api/AGENTS.md` L108 |
| 配置入口 | `configs/dify_config`，禁止直接读 env | `api/AGENTS.md` L206 |
| 租户隔离 | 所有查询必须带 `tenant_id` | `api/AGENTS.md` L207 |
| Celery 队列 | `dataset` 队列专用于知识库任务 | `api/tasks/document_indexing_task.py` L32 |
| Pydantic v2 | DTO 用 Pydantic v2，`extra="forbid"` | `api/AGENTS.md` L148-149 |
| i18n 强制 | 前端字符串必须用 `web/i18n/en-US/` 键 | `web/AGENTS.md` L9 |
| 覆盖层组件 | 必须用 `@langgenius/dify-ui/*` 原语 | `web/AGENTS.md` L15-16 |

---

## 5. 关键文件速查

| 文件 | 行数 | 角色 |
|------|:----:|------|
| `api/models/dataset.py` | 1,797 | Dataset/Document/Segment/ChildChunk ORM |
| `api/services/dataset_service.py` | 4,341 | 知识库业务逻辑（最大单文件） |
| `api/core/rag/datasource/retrieval_service.py` | 970 | 语义/全文/混合检索核心 |
| `api/core/indexing_runner.py` | 855 | 文档 → 提取 → 清洗 → 切分 → 索引编排 |
| `api/tasks/document_indexing_task.py` | 260 | 索引异步任务入口 |
| `api/controllers/console/datasets/datasets.py` | 1,234 | 知识库控制台路由 |
| `api/controllers/service_api/dataset/dataset.py` | 1,092 | 知识库 Service API 路由 |
| `api/app_factory.py` | 233 | Flask 应用工厂 |
| `api/pyproject.toml` | 301 | Python 依赖 (30 VDB + 8 Trace 插件) |
| `docker/docker-compose.yaml` | 1,210 | 12 个服务编排 |
| `docker/.env.example` | 265 | 环境变量模板 |

---

## 6. 当前状态

| 项 | 状态 |
|----|:----:|
| Docker 全部服务 | ✅ 运行中，11/11 healthy |
| API v1.15.0 | ✅ 健康检查通过 |
| Console API CRUD | ✅ 验证通过 |
| Service API (/v1) | ⚠️ ApiToken bug 阻塞 API Key 创建 |
| CodeGraph | ❌ 非 git 仓库，无法运行 |
| Python 本地环境 | ❌ 3.11 不满足 3.12 要求，建议用 Docker |
