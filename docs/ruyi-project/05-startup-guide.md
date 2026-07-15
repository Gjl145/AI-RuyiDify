# RuyiDify 启动方式完整审查报告

> **审查日期**: 2026-07-15
> **审查范围**: 全仓库（AGENTS.md, Makefile, README, dev/, docker/, api/, web/）
> **原则**: 只读审查，不运行。所有命令来自项目现有脚本或文档。

---

## 1. 启动方式总览

| # | 方式 | 适用场景 | 推荐度 | 来源 |
|---|------|----------|:------:|------|
| A | **Docker Compose 全栈** | 快速体验、演示、无本地开发环境 | ⭐⭐⭐ | `README.md` L74-83 |
| B | **Make dev-setup** | 一键初始化开发环境（中间件+deps） | ⭐⭐⭐ | `Makefile` L18 |
| C | **dev/setup + dev/start-* 系列** | 本地源码开发（分组件启动） | ⭐⭐⭐ | `api/README.md` L19-57 |
| D | **Make prepare-docker** | 仅启动中间件容器 | ⭐⭐ | `Makefile` L22-31 |
| E | **docker-compose.middleware.yaml** | 中间件独立启动（配合手动 api/web） | ⭐⭐ | `docker-compose.middleware.yaml` |
| F | **uv run flask run** (手动) | 后端调试、断点调试 | ⭐ | `dev/start-api` L10-11 |
| G | **pnpm dev** (手动) | 前端热重载开发 | ⭐ | `web/package.json` L29 |
| H | **uv run celery worker** (手动) | 单独调试异步任务 | ⭐ | `dev/start-worker` L127-129 |

---

## 2. 逐项详细说明

### 方式 A：Docker Compose 全栈启动

**适用**: 快速部署，无需本地 Python/Node 环境

**前置**: Docker + Docker Compose

**步骤**（来自 `README.md` L76-83）:
```bash
cd D:\ai\RuyiDify\docker
cp .env.example .env
docker compose up -d                        # 默认: weaviate + postgresql
# 或指定 profiles:
docker compose --profile postgresql --profile weaviate up -d
```

**启动的组件** (12 个服务):

| 服务 | 镜像 | 端口 |
|------|------|------|
| `init_permissions` | busybox:latest | —（一次性） |
| `api` | langgenius/dify-api:1.15.0 | 5001 (内网) |
| `worker` | langgenius/dify-api:1.15.0 | — |
| `worker_beat` | langgenius/dify-api:1.15.0 | — |
| `web` | langgenius/dify-web:1.15.0 | 3000 (内网) |
| `nginx` | nginx:latest | **80→host**, 443→host |
| `db_postgres` | postgres:15-alpine | 5432 (内网) |
| `redis` | redis:6-alpine | 6379 (内网) |
| `weaviate` | semitechnologies/weaviate:1.27.0 | 8080 (内网) |
| `sandbox` | langgenius/dify-sandbox:0.2.15 | 8194 (内网) |
| `plugin_daemon` | langgenius/dify-plugin-daemon:0.6.3-local | 5002 (内网) |
| `ssrf_proxy` | ubuntu/squid:latest | 3128 (内网) |

**环境变量文件**: `docker/.env` (从 `.env.example` 生成)

**停止**: `docker compose down`

**验证**: 浏览器打开 `http://localhost` → Dify 初始化页面

---

### 方式 B：Make dev-setup（一键开发环境初始化）

**适用**: 首次搭建本地开发环境

**前置**: Docker, uv, pnpm, make

**来源**: `Makefile` L18

```bash
make dev-setup
```

等价于依次执行:

| 步骤 | Target | 实际操作 |
|:----:|--------|----------|
| 1 | `prepare-docker` | `cp docker/envs/middleware.env.example docker/middleware.env` → 启动 `docker-compose.middleware.yaml`（仅 6 个中间件） |
| 2 | `prepare-web` | `cp web/.env.example web/.env.local` → `pnpm install` |
| 3 | `prepare-api` | `cp api/.env.example api/.env` → `uv sync --dev` → `flask db upgrade` |

**注意**: 此方式**只准备环境，不启动 API/Web**。启动用方式 C。

---

### 方式 C：dev/setup + dev/start-* 系列（推荐本地开发）

**适用**: 本地源码开发，各组件独立启动和调试

**来源**: `api/README.md` L19-57

```bash
# 1. 一次性环境初始化
./dev/setup

# 2. 启动中间件（PostgreSQL + Redis + Weaviate + Sandbox + Plugin Daemon）
./dev/start-docker-compose

# 3. 启动后端 API (自动运行 db upgrade)
./dev/start-api

# 4. 启动前端 Web (Next.js dev server)
./dev/start-web

# 5. 启动 Celery Worker (异步任务)
./dev/start-worker

# 6. 可选: 启动 Celery Beat (定时任务)
./dev/start-beat
```

**各脚本细节**:

| 脚本 | 工作目录 | 实际命令 | 端口 |
|------|----------|----------|:----:|
| `dev/setup` | 自动 | `cp .env 文件` → `uv sync` → `pnpm install` | — |
| `dev/start-docker-compose` | `docker/` | `docker compose --env-file middleware.env -f docker-compose.middleware.yaml -p dify up -d` | 5432,6379,8080,8194,5002 |
| `dev/start-api` | `api/` | `uv run flask db upgrade` → `uv run flask run --host 0.0.0.0 --port=5001 --debug` | 5001 |
| `dev/start-web` | 仓库根 | `pnpm install && pnpm --dir web dev:inspect` | 3000 (Next.js) |
| `dev/start-worker` | `api/` | `uv run celery -A app.celery worker -P gevent -c 1 -Q dataset,workflow,...` | — |
| `dev/start-beat` | 仓库根 | `uv --directory api run celery -A app.celery beat --loglevel INFO` | — |

**环境变量文件**:
- 后端: `api/.env` (从 `api/.env.example` 生成)
- 前端: `web/.env.local` (从 `web/.env.example` 生成)
- 中间件: `docker/middleware.env` (从 `docker/envs/middleware.env.example` 生成)

**停止**: 
```bash
make dev-clean    # 停止容器 + 清理 volumes
# 或手动 Ctrl+C 停止各 dev 进程
```

---

### 方式 D：仅启动中间件 (Make)

**来源**: `Makefile` L22-31

```bash
make prepare-docker
```

等同:
```bash
cd docker
cp envs/middleware.env.example middleware.env
docker compose -f docker-compose.middleware.yaml --env-file middleware.env -p dify-middlewares-dev up -d
```

启动 6 个中间件：`db_postgres`, `redis`, `weaviate`, `sandbox`, `plugin_daemon`, `ssrf_proxy`

---

### 方式 E：仅启动中间件 (直接 Compose)

**来源**: `docker-compose.middleware.yaml`

```bash
cd D:\ai\RuyiDify\docker
cp envs/middleware.env.example middleware.env
docker compose -f docker-compose.middleware.yaml --env-file middleware.env up -d
```

**暴露端口**（与全栈 Docker 不同，中间件端口直接暴露到宿主机）:

| 服务 | 端口 | 用途 |
|------|:----:|------|
| PostgreSQL | 5432 | 数据库 |
| Redis | 6379 | 缓存/Broker |
| Weaviate | 8080 | 向量数据库 |
| Sandbox (通过 ssrf_proxy) | 8194 | 代码执行 |
| Plugin Daemon | 5002, 5003 | 插件运行时 |

**停止**: `docker compose -f docker-compose.middleware.yaml --env-file middleware.env down`

---

### 方式 F：手动启动 Flask API

**来源**: `dev/start-api` L10-11

```bash
cd D:\ai\RuyiDify\api
uv run flask db upgrade
uv run flask run --host 0.0.0.0 --port=5001 --debug
```

**前置**: 已运行 `dev/setup`，中间件（方式 D/E）已启动

---

### 方式 G：手动启动前端

**来源**: `web/package.json` L29

```bash
cd D:\ai\RuyiDify\web
pnpm dev           # Next.js dev server (端口 3000)
pnpm dev:inspect   # 带 --inspect 调试
pnpm dev:proxy     # 代理到远程 Dify 云实例（不连本地 API）
```

---

### 方式 H：手动启动 Celery Worker/Beat

**来源**: `dev/start-worker` L127-129, `dev/start-beat` L57-59

```bash
# Worker（默认处理全部队列）
cd D:\ai\RuyiDify\api
uv run celery -A app.celery worker -P gevent -c 1 --loglevel INFO -Q dataset,workflow,...

# 指定队列
./dev/start-worker --queues dataset --concurrency 2

# Beat（定时任务调度）
./dev/start-beat
```

---

## 3. 组件与端口表

| 组件 | 全栈 Docker (A) | 中间件 Docker (D/E) | 本地手动 (F/G/H) | 默认端口 | 必需？ |
|------|:---:|:---:|:---:|:----:|:----:|
| Nginx (反向代理) | ✅ | ❌ | ❌ | 80→host | 仅全栈 |
| Flask API | ✅ 容器 | ❌ | ✅ 手动 | 5001 | ✅ |
| Next.js Web | ✅ 容器 SSR | ❌ | ✅ `pnpm dev` | 3000 | ✅ |
| Celery Worker | ✅ 容器 | ❌ | ✅ 手动 | — | ✅ |
| Celery Beat | ✅ 容器 | ❌ | ⬜ 可选 | — | ⬜ |
| PostgreSQL | ✅ 容器 | ✅ 容器 | ✅ 容器 | 5432 | ✅ |
| Redis | ✅ 容器 | ✅ 容器 | ✅ 容器 | 6379 | ✅ |
| Weaviate | ✅ 容器 | ✅ 容器 | ✅ 容器 | 8080 | ✅ |
| Sandbox | ✅ 容器 | ✅ 容器 | ✅ 容器 | 8194 | ✅ (代码执行) |
| Plugin Daemon | ✅ 容器 | ✅ 容器 | ✅ 容器 | 5002 | ⬜ (插件商店) |
| SSRF Proxy | ✅ 容器 | ✅ 容器 | ✅ 容器 | 3128 | ⬜ (安全) |

---

## 4. 环境配置清单

| 文件 | 方式 A (全栈) | 方式 C (本地) | 来源 |
|------|:---:|:---:|------|
| `docker/.env` | ✅ 必需 | ❌ | `docker/.env.example` |
| `docker/middleware.env` | ❌ | ✅ 必需 | `docker/envs/middleware.env.example` |
| `api/.env` | ❌ | ✅ 必需 | `api/.env.example` (786行) |
| `web/.env.local` | ❌ | ✅ 必需 | `web/.env.example` (119行) |
| `docker/middleware.env` | ❌ | ✅ 必需 | `docker/envs/middleware.env.example` (245行) |

---

## 5. 推荐选择流程

```
需要快速跑起来看效果？
├─ 是 → 方式 A: docker compose up -d
│       访问 http://localhost，Dify Web UI 一站式管理
│       缺点: 修改源码不生效，需重新构建镜像
│
└─ 否（需要改代码/调试）
   ├─ 首次搭建？→ 方式 B: make dev-setup (初始化)
   └─ 日常开发 → 方式 C: ./dev/start-* 系列
      ├─ 终端1: ./dev/start-docker-compose (中间件)
      ├─ 终端2: ./dev/start-api (后端, 支持 hot reload)
      ├─ 终端3: ./dev/start-web (前端, HMR)
      ├─ 终端4: ./dev/start-worker (异步任务)
      └─ 终端5: ./dev/start-beat (定时任务, 可选)
```

---

## 6. 风险与待验证项

### 6.1 已验证确认

| 项 | 结论 | 证据 |
|----|:----:|------|
| docker-compose.yaml 语法 | ✅ | `docker compose config` 通过 |
| 全栈 12 服务启动 | ✅ | 2026-07-15 实际验证 |
| 镜像缓存 | ✅ | 10 个镜像已本地缓存 |
| `.env` 生成 | ✅ | `docker/.env` 已存在 |
| Git 初始化 | ✅ | 已推送 GitHub |
| ApiToken bug 修复 | ✅ | 源码已修, ruff lint 通过 |

### 6.2 常见阻塞点

| 阻塞点 | 影响方式 | 说明 |
|--------|:--------:|------|
| **Docker Desktop 未运行** | A, D, E | Windows 必须手动启动 |
| **Python 3.11 vs 3.12** | B, C, F, G, H | `api/pyproject.toml` 要求 3.12，当前环境 3.11 |
| **uv sync 首次慢** | B, C | 30+ VDB 插件 + 全量依赖首次解析需数分钟 |
| **pnpm install** | B, C | 需 pnpm 已安装 |
| **make 不可用** | B, D | Windows 无 make，需手动执行脚本 |
| **端口冲突** | A, C | 5432/6379/8080/3000/5001 不要被占用 |
| **镜像拉取** | A, D, E | 首次 10 个镜像约 5-8 GB |
| **Embedding 模型** | 全部 | 创建 high_quality 知识库前需在 Web UI 配置模型供应商 |

### 6.3 待验证项

| 项 | 最低验证方法 |
|----|-------------|
| 方式 B `make dev-setup` | Windows 安装 make → 执行（需 Python 3.12） |
| 方式 C `./dev/start-*` 全部流程 | Docker Desktop 启动 → 逐脚本执行 |
| 方式 A 修复后 ApiToken 创建 API Key | `docker cp` 修复文件 → restart → POST API |
| Celery 队列实际消费 | 上传文档 → 检查 `document_indexing_task` 执行 |
| 前端代理模式 `pnpm dev:proxy` | 配置 DEV_PROXY_TARGET 后启动 |

---

## 7. Makefile 可用 Targets 速查

> 来源: `Makefile` L187-212

```
开发环境:
  make dev-setup       完整初始化（docker + deps + db）
  make prepare-docker   仅启动中间件容器
  make prepare-web      仅准备前端（配置 + pnpm install）
  make prepare-api      仅准备后端（配置 + uv sync + db upgrade）
  make dev-clean        停止容器 + 清理开发数据

代码质量:
  make format           ruff format
  make check            ruff check
  make lint             ruff format + fix + import-lint + dotenv-lint
  make type-check       pyrefly + mypy
  make test             后端单元测试
  make test-all         全量测试（含 Docker-backed 集成测试）

Docker 构建:
  make build-web        构建 Web 镜像
  make build-api        构建 API 镜像
  make build-all        构建全部镜像
```
