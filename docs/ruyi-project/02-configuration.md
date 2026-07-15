# 02 · 配置入口参考

> **最后更新**: 2026-07-15
> **源码分析日期**: 2026-07-15

---

## 1. 配置文件清单

### 1.1 Docker 部署配置 (`docker/`)

| 文件 | 行数 | 用途 |
|------|:----:|------|
| `docker/.env.example` | 265 | **主配置模板** — 核心服务、数据库、向量库、存储 |
| `docker/.env` | — | 实际配置（从 .env.example 生成，已存在） |
| `docker/docker-compose.yaml` | 1,210 | 服务编排定义（12 个 services） |
| `docker/docker-compose-template.yaml` | — | Compose 模板（用于生成 docker-compose.yaml） |
| `docker/docker-compose.middleware.yaml` | — | 中间件独立启动（6 个服务） |

### 1.2 核心服务环境变量 (`docker/envs/core-services/`)

| 文件 | 用途 |
|------|------|
| `shared.env.example` | API/Worker 共享变量（DB/Redis/密钥） |
| `api.env.example` | API 专属（服务器、日志） |
| `worker.env.example` | Celery Worker 配置 |
| `worker-beat.env.example` | Celery Beat 调度器配置 |
| `web.env.example` | Next.js 前端配置 |
| `plugin-daemon.env.example` | 插件守护进程配置 |
| `sandbox.env.example` | 代码沙箱配置 |

### 1.3 数据库环境变量 (`docker/envs/databases/`)

| 文件 | 用途 |
|------|------|
| `db-postgres.env.example` | PostgreSQL 连接 |
| `db-mysql.env.example` | MySQL 连接 |
| `redis.env.example` | Redis 连接 |

### 1.4 向量数据库环境变量 (`docker/envs/vectorstores/`)

| 文件 | 用途 |
|------|------|
| `weaviate.env.example` | Weaviate（默认） |
| `qdrant.env.example` | Qdrant |
| `milvus.env.example` | Milvus |
| `pgvector.env.example` | PGVector |
| `pgvecto-rs.env.example` | PGVecto.rs |
| `chroma.env.example` | Chroma |
| `elasticsearch.env.example` | Elasticsearch |
| `opensearch.env.example` | OpenSearch |
| `oceanbase.env.example` | OceanBase |
| `couchbase.env.example` | Couchbase |
| `oracle.env.example` | Oracle |
| `myscale.env.example` | MyScale |
| `opengauss.env.example` | openGauss |
| `vastbase.env.example` | Vastbase |
| `iris.env.example` | IRIS |
| `matrixone.env.example` | MatrixOne |
| `seekdb.env.example` | SeekDB |

> 共 17 个向量数据库配置模板，覆盖全部支持的向量后端。

### 1.5 基础设施 (`docker/envs/infrastructure/`)

| 文件 | 用途 |
|------|------|
| `nginx.env.example` | Nginx 反向代理 |
| `certbot.env.example` | Let's Encrypt 证书 |
| `ssrf-proxy.env.example` | SSRF 防护代理 |
| `minio.env.example` | MinIO 对象存储 |
| `etcd.env.example` | etcd 分布式配置 |
| `milvus-standalone.env.example` | Milvus Standalone 模式 |

### 1.6 本地开发配置

| 文件 | 用途 |
|------|------|
| `api/.env.example` (786行) | API 本地开发完整配置模板 |
| `api/.env` | API 本地配置（**缺失**，需从 .env.example 复制） |
| `dify-agent/.example.env` | dify-agent 配置模板 |

---

## 2. 关键环境变量

### 2.1 数据库

| 变量 | 当前值 | 作用 |
|------|--------|------|
| `DB_TYPE` | `postgresql` | 数据库类型（postgresql/mysql） |
| `DB_USERNAME` | `postgres` | 数据库用户 |
| `DB_HOST` | `db_postgres` | Docker 服务名 |
| `DB_PORT` | `5432` | 数据库端口 |
| `DB_DATABASE` | `dify` | 数据库名 |
| `SQLALCHEMY_POOL_SIZE` | `30` | 连接池大小 |
| `SQLALCHEMY_ECHO` | `false` | SQL 日志 |

### 2.2 Redis / Celery

| 变量 | 当前值 | 作用 |
|------|--------|------|
| `REDIS_HOST` | `redis` | Docker 服务名 |
| `REDIS_PORT` | `6379` | Redis 端口 |
| `REDIS_DB` | `0` | Redis 数据库编号 |
| `CELERY_BROKER_URL` | `redis://...@redis:6379/1` | Celery 消息代理 |
| `CELERY_BACKEND` | `redis` | Celery 结果后端 |

### 2.3 向量数据库

| 变量 | 当前值 | 作用 |
|------|--------|------|
| `VECTOR_STORE` | `weaviate` | 向量数据库选择 |
| `VECTOR_INDEX_NAME_PREFIX` | `Vector_index` | 向量索引名前缀 |
| `WEAVIATE_ENDPOINT` | `http://weaviate:8080` | Weaviate 连接地址 |

### 2.4 存储

| 变量 | 当前值 | 作用 |
|------|--------|------|
| `STORAGE_TYPE` | `opendal` | 存储后端类型 |
| `OPENDAL_SCHEME` | `fs` | OpenDAL 协议（本地文件系统） |
| `OPENDAL_FS_ROOT` | `storage` | 本地存储根目录 |

### 2.5 服务端口

| 变量 | 当前值 | 作用 |
|------|--------|------|
| `DIFY_PORT` | `5001` | API 端口 |
| `NGINX_PORT` | `80` | Nginx HTTP 端口 |
| `NGINX_SSL_PORT` | `443` | Nginx HTTPS 端口 |
| `EXPOSE_NGINX_PORT` | `80` | 宿主机暴露端口 |

### 2.6 文件上传限制

| 变量 | 当前值 | 作用 |
|------|--------|------|
| `UPLOAD_FILE_SIZE_LIMIT` | `15` | 文件上传大小限制 (MB) |
| `UPLOAD_FILE_BATCH_LIMIT` | `5` | 批量上传数量限制 |
| `UPLOAD_IMAGE_FILE_SIZE_LIMIT` | `10` | 图片上传限制 (MB) |
| `INDEXING_MAX_SEGMENTATION_TOKENS_LENGTH` | `4000` | 分段最大 token 数 |
| `TOP_K_MAX_VALUE` | `10` | 检索返回数量上限 |

### 2.7 开发/调试

| 变量 | 当前值 | 作用 |
|------|--------|------|
| `SECRET_KEY` | (空=自动生成) | 会话签名密钥 |
| `DEBUG` | `false` | 调试模式 |
| `LOG_LEVEL` | `INFO` | 日志级别 |
| `ENABLE_COLLABORATION_MODE` | `true` | 协作编辑 |
| `ENABLE_LEARN_APP` | `true` | Learn App 功能 |

### 2.8 模型供应商

| 变量 | 作用 | 配置位置 |
|------|------|----------|
| `OPENAI_API_BASE` | OpenAI 兼容 API 基地址 | `docker/.env.example` L38 |
| 各模型 API Key | 模型供应商鉴权 | **Dify 控制台「设置→模型供应商」中配置** |

> ⚠️ 模型 API Key 不在环境变量中，需通过 Dify Web UI 或 API 配置。

---

## 3. 配置入口架构

```
docker/.env  (主配置，优先级最高)
  ├── docker/envs/core-services/shared.env
  ├── docker/envs/core-services/api.env
  ├── docker/envs/core-services/worker.env
  ├── docker/envs/core-services/worker-beat.env
  ├── docker/envs/core-services/web.env
  ├── docker/envs/core-services/plugin-daemon.env
  ├── docker/envs/core-services/sandbox.env
  ├── docker/envs/databases/db-postgres.env
  ├── docker/envs/databases/redis.env
  ├── docker/envs/vectorstores/weaviate.env
  ├── docker/envs/infrastructure/nginx.env
  ├── docker/envs/infrastructure/ssrf-proxy.env
  ├── docker/envs/infrastructure/minio.env
  ├── docker/envs/middleware.env
  └── docker/envs/security.env
```

Docker Compose 中通过 `env_file` + `required: false` 加载，缺失不报错。`.env` 中的值优先级最高（覆盖 env_file）。

---

## 4. 配置文件创建方法

```bash
# Docker 部署（已执行）
cd docker
cp .env.example .env

# 本地开发（未执行，需时运行）
cd api
cp .env.example .env
```

---

## 5. 注意事项

| 项 | 说明 |
|----|------|
| 敏感变量 | `SECRET_KEY`、数据库密码、Redis 密码、Weaviate API Key、各模型 API Key 不在此文档中记录真实值 |
| Python 版本 | `api/pyproject.toml` 要求 Python 3.12，当前环境 3.11，建议 Docker 运行 |
| INIT_PASSWORD | 为空时不生效；Dify 初始化通过 `/console/api/setup` 接口完成 |
