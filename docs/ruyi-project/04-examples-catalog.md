# 04 · 示例脚本分类目录

> **最后更新**: 2026-07-15
> **源码分析日期**: 2026-07-15
> **脚本总数**: 29 个 (全部通过 Python 语法检查)
> **脚本路径**: `examples/知识库/`

---

## 1. 分类总览

| 分类 | 数量 | 文件 |
|------|:----:|------|
| 知识库管理 | 5 | 15, 21, 22, 23, *(API Key)* |
| 文档管理 | 8 | 01, 02, 05, 06, 24, 25, 26, 27, 28 |
| 分段管理 | 5 | 03, 07, 08, 09, 10 |
| 元数据 | 3 | 12, 13, 14 |
| 标签 | 1 | 11 |
| 检索调参 | 7 | 04, 16, 17, 18, 19, 20 |
| 问答应用 | 1 | 32 |

> 编号 29–31 不存在（跳号）。

---

## 2. 知识库管理

| 文件 | API | 学到什么 |
|------|-----|----------|
| `21_创建知识库.py` | `POST /v1/datasets` | 创建知识库，指定 embedding_model、provider、permission、indexing_technique |
| `22_更新知识库配置.py` | `PATCH /v1/datasets/{id}` | 更新名称、描述、权限 |
| `23_获取知识库详情.py` | `GET /v1/datasets/{id}` | 查询知识库完整信息 |
| `15_查询可用模型.py` | 模型列表 API | 查询供应商可用的 embedding/rerank 模型 |
| *(API Key 页面)* | Dify 控制台 | 创建 dataset- 开头的知识库 API 密钥 |

---

## 3. 文档管理

| 文件 | API | 学到什么 |
|------|-----|----------|
| `01_上传文档.py` | `POST /v1/datasets/{id}/document/create-by-file` | 上传本地文件，自动切分模式 |
| `25_通过文本创建文档.py` | `POST .../document/create-by-text` | 直接用文本内容创建文档 |
| `26_通过文本更新文档.py` | `POST .../document/update-by-text` | 更新已有文本类型文档的内容 |
| `02_查看文档列表.py` | `GET /v1/datasets/{id}/documents` | 分页查询文档列表 |
| `05_更新已有文档.py` | `PATCH .../documents/{doc_id}` | 更新文档处理规则 |
| `06_删除文档.py` | `DELETE .../documents/{doc_id}` | 删除指定文档 |
| `24_查询文档索引状态.py` | `GET .../documents/{doc_id}/indexing-status` | 查看 indexing_status: waiting→completed/error |
| `27_下载文档.py` | `GET .../documents/{doc_id}/download` | 下载原始文件 |
| `28_批量更新文档状态.py` | `PATCH .../documents/status` | 批量启用/禁用/归档文档 |

---

## 4. 分段管理

| 文件 | API | 学到什么 |
|------|-----|----------|
| `03_查看文档分段.py` | `GET .../documents/{doc_id}/segments` | 查看文档的所有分段 |
| `07_新增分段.py` | `POST .../segments` | 手动添加自定义分段 |
| `08_更新分段.py` | `PATCH .../segments/{seg_id}` | 更新分段内容和关键词 |
| `09_删除分段.py` | `DELETE .../segments/{seg_id}` | 删除指定分段 |
| `10_禁用和启用分段.py` | `PATCH .../segments/{seg_id}/status` | 控制分段的启用/禁用（影响检索可见性） |

---

## 5. 元数据

| 文件 | API | 学到什么 |
|------|-----|----------|
| `12_创建并删除元数据字段.py` | `POST/DELETE /v1/datasets/{id}/metadata` | 管理知识库级自定义元数据字段（type: string/number） |
| `13_给文档写入元数据.py` | `PATCH .../documents/{doc_id}` | 给文档写入 metadata 键值对 |
| `14_启用和禁用内置元数据.py` | API 配置 | 控制 Dify 内置元数据（来源/类型/分段长度等）是否参与检索过滤 |

---

## 6. 标签

| 文件 | API | 学到什么 |
|------|-----|----------|
| `11_创建并绑定标签.py` | Tag + TagBinding API | 对文档/分段打标签，标签检索与过滤 |

---

## 7. 检索调参

| 文件 | API | 检索方式 | 重点 |
|------|-----|----------|------|
| `04_检索知识库.py` | `POST /v1/datasets/{id}/retrieve` | 默认参数 | 基础检索入门 |
| `16_语义检索知识库.py` | 同上 + `search_method: semantic_search` | 语义 | 依赖 Embedding 模型，按含义相似度查找 |
| `17_混合检索知识库.py` | 同上 + `search_method: hybrid_search` | 混合 | 语义 + 关键词权重混合，多知识库适用 |
| `18_重排序检索知识库.py` | 同上 + `reranking_enable: true` | 语义 + Rerank | 对比启用和不启用 rerank 的排序差异 |
| `19_设置相似度阈值.py` | 同上 + `score_threshold_enabled: true` | 阈值过滤 | 控制最低相似度门槛，过滤低质结果 |
| `20_调整返回结果数量.py` | 同上 + `top_k` 参数 | TopK 调节 | 返回数量对答案质量的影响 |

---

## 8. 问答应用

| 文件 | API | 学到什么 |
|------|-----|----------|
| `32_用Python调用知识库应用.py` | `POST /v1/chat-messages` | **区别于检索**：用 App API Key（app- 开头），让 LLM 基于检索结果生成回答。`response_mode: blocking` 返回完整结果 + `retriever_resources` 引用来源 |

---

## 9. 运行前置条件

| 条件 | 状态 | 说明 |
|------|:----:|------|
| Dify API 运行 | ✅ | Docker Compose 启动后 `localhost/v1` 可达 |
| 知识库 API Key | ❌ | **ApiToken 模型 bug 阻塞** (BUG-001)，无法通过 Console API 创建 |
| Embedding 模型 | ❌ | 需在 Dify 控制台配置模型供应商 |
| 应用 API Key | ⚠️ | 需在 Dify 控制台创建 Chat 应用 + 发布 |

### 最小运行方法（当 ApiToken 修复后）

```bash
# 1. 创建 API Key
#    通过 Dify Web UI: 知识库 → API 访问 → 创建 API Key
#    或修复 BUG-001 后通过 Console API 创建

# 2. 修改示例脚本
#    编辑 scripts 中的 API_BASE_URL = "http://localhost/v1"
#    编辑 API_KEY = "dataset-xxx"  # 上一步获取的密钥

# 3. 运行
cd examples/知识库
python 21_创建知识库.py
```
