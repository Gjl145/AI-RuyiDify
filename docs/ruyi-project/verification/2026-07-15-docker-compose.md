# Docker Compose 验证报告

> **验证日期**: 2026-07-15
> **验证人**: Hermes Agent (deepseek-v4-pro)
> **环境**: Docker 29.6.1 + Compose v5.2.0, Windows 10, D:\ai\RuyiDify\docker

---

## 执行摘要

| 结果 | 说明 |
|:----:|------|
| ✅ **全部通过** | 11/11 容器正常运行，API/DB/Redis/Weaviate 健康检查通过，Console API CRUD 验证通过 |

---

## 1. 环境检查

| 项 | 版本/状态 |
|----|-----------|
| Docker | 29.6.1 ✅ |
| Docker Compose | v5.2.0 ✅ |
| OS Arch | linux/x86_64 |
| 内存 | ~8 GB |
| 磁盘可用 | 111 GB (D: 271G) |
| `.env` 文件 | ✅ 已从 `.env.example` 生成 |
| `api/.env` | ❌ 缺失（本地开发需要时才需创建） |

---

## 2. 镜像拉取

| 镜像 | Tag | 大小 |
|------|-----|------|
| busybox | latest | 6.81 MB |
| redis | 6-alpine | 41.8 MB |
| nginx | latest | 241 MB |
| postgres | 15-alpine | 417 MB |
| semitechnologies/weaviate | 1.27.0 | 234 MB |
| ubuntu/squid | latest | 303 MB |
| langgenius/dify-web | 1.15.0 | 805 MB |
| langgenius/dify-sandbox | 0.2.15 | 848 MB |
| langgenius/dify-api | 1.15.0 | ~1 GB |
| langgenius/dify-plugin-daemon | 0.6.3-local | ~500 MB |

> 首次拉取约 10 分钟，取决于网络速度。

---

## 3. 启动命令

```bash
cd D:\ai\RuyiDify\docker
docker compose --profile postgresql --profile weaviate up -d
```

---

## 4. 服务状态

| # | 服务 | 状态 | 端口 | 健康检查 |
|---|------|:----:|------|:----:|
| 1 | `init_permissions` | Exited (0) | — | 一次性任务 ✅ |
| 2 | `api` | Up | 5001 (内网) | ✅ healthy |
| 3 | `web` | Up | 3000 (内网) | — |
| 4 | `worker` | Up | — | — |
| 5 | `worker_beat` | Up | — | — |
| 6 | `db_postgres` | Up | 5432 (内网) | ✅ healthy |
| 7 | `redis` | Up | 6379 (内网) | ✅ healthy |
| 8 | `weaviate` | Up | 8080 (内网) | ✅ v1.27.0 |
| 9 | `sandbox` | Up | — | ✅ healthy |
| 10 | `plugin_daemon` | Up | 5003 → host | — |
| 11 | `ssrf_proxy` | Up | 3128 (内网) | — |
| 12 | `nginx` | Up | 80 → host, 443 → host | — |

---

## 5. 健康检查

```bash
# API 健康检查
$ curl http://localhost:5001/health
{"pid":75,"status":"ok","version":"1.15.0"}              ✅

# PostgreSQL
$ docker exec docker-db_postgres-1 pg_isready -U postgres
/var/run/postgresql:5432 - accepting connections         ✅

# Redis
$ docker exec docker-redis-1 redis-cli -a difyai123456 ping
PONG                                                     ✅

# Weaviate
$ docker exec docker-api-1 curl -s http://weaviate:8080/v1/meta
{"hostname":"http://[::]:8080","modules":{},"version":"1.27.0"}  ✅
```

---

## 6. Dify 系统初始化

```bash
# 初始化管理员账号
POST /console/api/setup
{"email":"admin@ruyidify.local","name":"Admin","password":"RuyiDify2026!"}
→ {"result":"success"}                                   ✅

# 登录（密码需 Base64 编码）
POST /console/api/login
{"email":"admin@ruyidify.local","password":"<Base64>"}
→ {"result":"success"}                                   ✅
```

### ⚠️ 密码编码说明

Dify 前端 (`web/utils/encryption.ts`) 在发送登录请求前对密码做 Base64 编码：
```javascript
const utf8Bytes = new TextEncoder().encode(password)
const base64 = btoa(String.fromCharCode(...utf8Bytes))
```

CLI 等效操作：
```bash
echo -n "RuyiDify2026!" | base64
# → UnV5aURpZnkyMDI2IQ==
```

---

## 7. Console API CRUD 验证

```bash
# 创建知识库 (economy 模式)
POST /console/api/datasets
{"name":"test-knowledge-base","indexing_technique":"economy"}
→ id: d5d953f7-...                                       ✅

# 列出知识库
GET /console/api/datasets
→ {"total":1,"data":[...]}                               ✅

# 查看详情
GET /console/api/datasets/{id}
→ 完整 JSON，包含 retrieval_model_dict                   ✅

# 查看文档列表
GET /console/api/datasets/{id}/documents
→ {"data":[],"total":0}                                  ✅

# 删除知识库
DELETE /console/api/datasets/{id}
→ 200 OK (空 body)                                       ✅

# 确认删除
GET /console/api/datasets
→ {"total":0}                                            ✅
```

---

## 8. 发现的问题

| # | 问题 | 严重度 | 详情 |
|---|------|:------:|------|
| **BUG-001** | ApiToken 模型缺陷 | 🔴 阻塞 | `api/models/model.py` L2236 有注释 `"bug: this uses setattr so idk the field."`，`ApiToken` 缺少 `dataset_id` 属性导致 `POST /console/api/datasets/{id}/api-keys` 返回 500。**无法创建知识库 API Key。** |
| **ENV-001** | Python 版本不匹配 | 🟡 | 本地 Python 3.11.15，`api/pyproject.toml` 要求 `~=3.12.0`。Docker 容器内为 3.12，不受影响。 |
| **ISSUE-001** | Embedding 模型未配置 | 🟡 | `high_quality` 索引模式需要 embedding 模型供应商，当前未配置。仅 `economy` 可用。 |
| **ISSUE-002** | Weaviate 端口未暴露 | 🟢 低 | 8080 仅在 Docker 内网，不影响任何功能。 |

---

## 9. 后续步骤

1. 🔴 **修复 BUG-001**：在 `api/models/model.py` 的 `ApiToken` 类中添加 `dataset_id` 字段
2. 🟡 **配置 Embedding 模型**：在 Dify Web UI (http://localhost) → 设置 → 模型供应商 → 添加（如 SiliconFlow + BAAI/bge-m3）
3. 🟢 运行 `examples/知识库/` 示例脚本，验证完整知识库链路
