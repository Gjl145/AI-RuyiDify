# 06 · Dify 知识库 API 参考

> **整理日期**: 2026-07-15
> **参考来源**: 
> - 官方文档 https://docs.dify.ai/zh/api-reference/guides/knowledge
> - 项目源码 `api/controllers/service_api/dataset/`
> - 示例代码 `examples/知识库/`

---

## API 总览

**共 42 个端点**，分 7 大类：

| 类别 | 端点数 | 说明 |
|------|:------:|------|
| 知识库 CRUD | 5 | 创建、列表、详情、更新、删除知识库 |
| 文档管理 | 12 | 上传文件/文本、列表、更新、下载、索引状态 |
| 分段管理 | 9 | 增删改查分段 + 子分段 + 启用/禁用 |
| 检索 | 1 | 语义/全文/混合检索 + 命中测试 |
| 元数据 | 7 | 自定义字段 + 内置元数据 + 批量写入 |
| 标签 | 7 | 标签 CRUD + 绑定/解绑 |
| 模型查询 | 1 | 查询可用 Embedding/Rerank 模型 |

> 知识库问答不属于知识库 API，是 Chat 应用 API (`POST /v1/chat-messages`)，知识库作为上下文接入。

---

## 1. 知识库 CRUD（5 个）

Base URL: `/v1`

| 方法 | 路径 | 说明 | 示例 |
|:----:|------|------|:----:|
| `POST` | `/datasets` | 创建知识库 | `21_创建知识库.py` |
| `GET` | `/datasets` | 列出知识库 | `23_获取知识库详情.py` |
| `GET` | `/datasets/{dataset_id}` | 获取详情 | `23_获取知识库详情.py` |
| `PATCH` | `/datasets/{dataset_id}` | 更新配置 | `22_更新知识库配置.py` |
| `DELETE` | `/datasets/{dataset_id}` | 删除知识库 | — |

**创建请求示例**:
```json
{
  "name": "my-knowledge-base",
  "indexing_technique": "high_quality",
  "embedding_model": "BAAI/bge-m3",
  "embedding_model_provider": "langgenius/siliconflow/siliconflow",
  "permission": "only_me",
  "provider": "vendor"
}
```

---

## 2. 文档管理（12 个）

| 方法 | 路径 | 说明 | 示例 |
|:----:|------|------|:----:|
| `POST` | `/datasets/{id}/document/create-by-file` | 上传文件创建文档 | `01_上传文档.py` |
| `POST` | `/datasets/{id}/document/create-by-text` | 通过文本创建文档 | `25_通过文本创建文档.py` |
| `POST` | `/datasets/{id}/documents/{doc_id}/update-by-file` | 通过文件更新文档 | `05_更新已有文档.py` |
| `POST` | `/datasets/{id}/documents/{doc_id}/update-by-text` | 通过文本更新文档 | `26_通过文本更新文档.py` |
| `GET` | `/datasets/{id}/documents` | 查看文档列表（分页） | `02_查看文档列表.py` |
| `GET` | `/datasets/{id}/documents/{doc_id}` | 获取文档详情 | `27_下载文档.py` |
| `PATCH` | `/datasets/{id}/documents/{doc_id}` | 更新文档元数据 | `13_给文档写入元数据.py` |
| `DELETE` | `/datasets/{id}/documents/{doc_id}` | 删除文档 | `06_删除文档.py` |
| `GET` | `/datasets/{id}/documents/{doc_id}/download` | 下载原始文件 | `27_下载文档.py` |
| `GET` | `/datasets/{id}/documents/{batch}/indexing-status` | 查询索引状态 | `24_查询文档索引状态.py` |
| `POST` | `/datasets/{id}/documents/download-zip` | 批量下载为 ZIP | — |
| `PATCH` | `/datasets/{id}/documents/status/{action}` | 批量更新状态 | `28_批量更新文档状态.py` |

`{action}` 可选值: `enable`, `disable`, `archive`, `un_archive`

---

## 3. 分段管理（9 个）

| 方法 | 路径 | 说明 | 示例 |
|:----:|------|------|:----:|
| `POST` | `/datasets/{id}/documents/{doc_id}/segments` | 新增分段 | `07_新增分段.py` |
| `GET` | `/datasets/{id}/documents/{doc_id}/segments` | 查看分段列表 | `03_查看文档分段.py` |
| `POST` | `/datasets/{id}/documents/{doc_id}/segments/{seg_id}` | 更新分段内容/关键词 | `08_更新分段.py` |
| `GET` | `.../segments/{seg_id}` | 查看分段详情 (含子分段) | — |
| `DELETE` | `.../segments/{seg_id}` | 删除分段 | `09_删除分段.py` |
| `POST` | `.../segments/{seg_id}/status` | 启用/禁用分段 | `10_禁用和启用分段.py` |
| `GET` | `.../segments/{seg_id}/child-chunks` | 查看子分段列表 | — |
| `DELETE` | `.../child-chunks/{chunk_id}` | 删除子分段 | — |
| `PATCH` | `.../child-chunks/{chunk_id}` | 更新子分段 | — |

---

## 4. 检索（1 个）

| 方法 | 路径 | 说明 | 示例 |
|:----:|------|------|:----:|
| `POST` | `/datasets/{id}/retrieve` (同 `/hit-testing`) | 检索知识库 | `04/16/17/18/19/20_*.py` |

**检索参数**:
```json
{
  "query": "用户问题",
  "retrieval_model": {
    "search_method": "semantic_search | full_text_search | hybrid_search",
    "top_k": 3,
    "score_threshold_enabled": false,
    "score_threshold": 0.5,
    "reranking_enable": false,
    "reranking_model": {
      "reranking_provider_name": "...",
      "reranking_model_name": "..."
    },
    "weights": { "vector_weight": 0.7, "keyword_weight": 0.3 }
  }
}
```

---

## 5. 元数据（7 个）

| 方法 | 路径 | 说明 | 示例 |
|:----:|------|------|:----:|
| `POST` | `/datasets/{id}/metadata` | 创建自定义元数据字段 | `12_创建并删除元数据字段.py` |
| `GET` | `/datasets/{id}/metadata` | 查看元数据字段列表 | `12/14` |
| `PATCH` | `/datasets/{id}/metadata/{meta_id}` | 更新元数据字段 | — |
| `DELETE` | `/datasets/{id}/metadata/{meta_id}` | 删除元数据字段 | `12_创建并删除元数据字段.py` |
| `GET` | `/datasets/{id}/metadata/built-in` | 查看内置元数据 | `14_启用和禁用内置元数据.py` |
| `POST` | `/datasets/{id}/metadata/built-in/{action}` | 启用/禁用内置元数据 | `14_启用和禁用内置元数据.py` |
| `POST` | `/datasets/{id}/documents/metadata` | 批量写入文档元数据 | `13_给文档写入元数据.py` |

---

## 6. 标签（7 个）

| 方法 | 路径 | 说明 | 示例 |
|:----:|------|------|:----:|
| `GET` | `/datasets/tags` | 查看标签列表 | — |
| `POST` | `/datasets/tags` | 创建标签 | `11_创建并绑定标签.py` |
| `PATCH` | `/datasets/tags` | 更新标签 | — |
| `DELETE` | `/datasets/tags` | 删除标签 | — |
| `POST` | `/datasets/tags/binding` | 绑定标签到文档/分段 | `11_创建并绑定标签.py` |
| `POST` | `/datasets/tags/unbinding` | 解绑标签 | — |
| `GET` | `/datasets/{id}/tags` | 查看知识库标签 | — |

---

## 7. 模型查询（1 个）

| 方法 | 路径 | 说明 | 示例 |
|:----:|------|------|:----:|
| `GET` | `/workspaces/current/models/model-types/{type}` | 查询可用模型 | `15_查询可用模型.py` |

`{type}` 可选: `text-embedding`, `rerank`, `speech2text`, `tts`, `moderation`

---

## 认证方式

所有请求需携带 `Authorization: Bearer {dataset_api_key}` 头：

```python
headers = {"Authorization": "Bearer dataset-xxx"}
```

API Key 通过 Dify 控制台「知识库 → API 访问」创建，格式为 `dataset-` 开头。

---

## 索引状态值

| 状态 | 说明 |
|------|------|
| `waiting` | 排队等待处理 |
| `parsing` | 正在解析文件内容 |
| `cleaning` | 正在清洗文本 |
| `splitting` | 正在切分文档 |
| `indexing` | 正在向量化和建立索引 |
| `completed` | 索引完成，可检索 |
| `error` | 处理出错 |

---

## 与 Chat 应用 API 的关系

知识库 API 只管理数据和检索，**不生成回答**。要让 LLM 基于检索结果生成回答，需使用 Chat 应用 API：

```
POST /v1/chat-messages
{
  "query": "用户问题",
  "response_mode": "blocking",
  "user": "user-id"
}
```

Chat 应用需要先在控制台创建，将知识库接入上下文，并发布获取 App API Key（`app-` 开头）。

---

## 示例脚本对照

| 脚本 | 对应端点 |
|------|----------|
| `21_创建知识库.py` | `POST /datasets` + `DELETE /datasets/{id}` |
| `01_上传文档.py` | `POST .../document/create-by-file` |
| `25_通过文本创建文档.py` | `POST .../document/create-by-text` |
| `02_查看文档列表.py` | `GET .../documents` |
| `24_查询文档索引状态.py` | `GET .../documents/{batch}/indexing-status` |
| `03_查看文档分段.py` | `GET .../segments` |
| `04_检索知识库.py` | `POST .../retrieve` |
| `16_语义检索知识库.py` | `POST .../retrieve` (semantic_search) |
| `17_混合检索知识库.py` | `POST .../retrieve` (hybrid_search) |
| `12_创建并删除元数据字段.py` | `POST/DELETE .../metadata` |
| `11_创建并绑定标签.py` | `POST /tags` + `POST /tags/binding` |
| `15_查询可用模型.py` | `GET /workspaces/.../models/model-types/{type}` |
| `32_用Python调用知识库应用.py` | `POST /chat-messages` |
