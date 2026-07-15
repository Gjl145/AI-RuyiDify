# 03 · 知识库端到端链路

> **最后更新**: 2026-07-15
> **源码分析日期**: 2026-07-15

---

## 1. 核心数据模型

> 源码: `api/models/dataset.py` (1,797 行)

```
Dataset（知识库）
├─ id, name, description, permission
├─ indexing_technique: high_quality | economy
├─ embedding_model, embedding_model_provider
├─ retrieval_model_dict
│   ├─ search_method: semantic_search | full_text_search | hybrid_search
│   ├─ top_k, score_threshold_enabled, score_threshold
│   ├─ reranking_enable, reranking_model
│   └─ weights (混合检索权重)
├─ doc_metadata[] (自定义元数据字段定义)
├─ built_in_field_enabled (内置元数据: 来源/类型/长度等)
└─ runtime_mode: general
    │
    ▼
Document（文档）
├─ id, dataset_id → Dataset
├─ name, data_source_type (upload_file | notion | web)
├─ doc_form (text_model | qa_model), doc_language
├─ indexing_status
│   └─ waiting → parsing → cleaning → splitting
│             → indexing → completed | error
├─ process_rule → DatasetProcessRule
│   ├─ mode: automatic | custom
│   └─ rules: { pre_processing_rules[], segmentation: {delimiter, max_tokens, chunk_overlap} }
├─ doc_metadata (文档级元数据键值对)
└─ dataset_process_rule_id
    │
    ▼
DocumentSegment（分段/chunk）
├─ id, document_id → Document
├─ content, position, word_count, token_count
├─ status: waiting | completed | error | disabled
├─ keywords[] (关键词列表)
├─ answer (QA 模式的答案文本)
└─ ChildChunk (子分段，父子索引模式)
    ├─ id, content, position
    └─ segment_id → DocumentSegment
```

---

## 2. 文档上传与索引流程

### 2.1 时序

```
1. 用户上传文件
   入口: Web UI → 知识库 → 添加文档
   或: POST /v1/datasets/{id}/document/create-by-file
   └─ payload: file + data{indexing_technique, process_rule, doc_form, doc_language}

2. Controller 接收
   controllers/console/datasets/datasets_document.py
   或 controllers/service_api/dataset/document.py
   └─ Pydantic 验证 → Service

3. Service 存储
   services/dataset_service.py → DocumentService
   ├─ UploadFile → 对象存储 (OpenDAL/S3/MinIO)
   ├─ Document 记录 (indexing_status=waiting)
   └─ DatasetProcessRule (切分配置)

4. 异步任务入队
   tasks/document_indexing_task.py
   └─ @shared_task(queue="dataset") → Redis → worker

5. IndexingRunner 编排
   core/indexing_runner.py (855行)
   ├─ Step 1: extract → core/rag/extractor/ (PDF/MD/HTML/CSV/Excel/Notion/网页)
   ├─ Step 2: clean   → core/rag/cleaner/clean_processor.py
   ├─ Step 3: split   → core/rag/splitter/
   │   └─ FixedRecursiveCharacterTextSplitter
   │       参数: delimiter, max_tokens, chunk_overlap (来自 DatasetProcessRule)
   └─ Step 4: index   → core/rag/index_processor/index_processor_factory.py
       └─ 更新 Document.indexing_status = completed

6. 分段写入向量库
   tasks/add_document_to_index_task.py (146行)
   └─ DocumentSegment → embedding → Weaviate/Qdrant/Milvus
       每个分段: {content, embedding_vector, doc_id, position, metadata}
```

### 2.2 关键源码文件

| 步骤 | 文件 | 行数 | 核心类/函数 |
|------|------|:----:|------|
| 模型 | `api/models/dataset.py` | 1,797 | Dataset, Document, DocumentSegment, ChildChunk |
| 服务 | `api/services/dataset_service.py` | 4,341 | DatasetService, DocumentService |
| 索引入队 | `api/tasks/document_indexing_task.py` | 260 | `document_indexing_task()` |
| 索引编排 | `api/core/indexing_runner.py` | 855 | `IndexingRunner.run()` |
| 写入向量库 | `api/tasks/add_document_to_index_task.py` | 146 | `add_document_to_index_task()` |
| 文档提取 | `api/core/rag/extractor/` | — | extract_processor, 多格式提取器 |
| 文本切分 | `api/core/rag/splitter/` | — | FixedRecursiveCharacterTextSplitter |
| 向量嵌入 | `api/core/rag/embedding/` | — | cached_embedding, embedding_base |

---

## 3. 检索与问答流程

### 3.1 检索参数

```json
{
  "query": "用户问题",
  "retrieval_model": {
    "search_method": "semantic_search | full_text_search | hybrid_search",
    "top_k": 3,
    "score_threshold_enabled": false,
    "score_threshold": 0.5,
    "reranking_enable": true,
    "reranking_model": {
      "reranking_provider_name": "...",
      "reranking_model_name": "..."
    },
    "weights": { "vector_weight": 0.7, "keyword_weight": 0.3 }
  }
}
```

### 3.2 检索执行流程

```
1. 检索请求
   POST /v1/datasets/{id}/retrieve
   或 Chatflow Workflow 中 Knowledge Retrieval 节点

2. RetrievalService
   core/rag/datasource/retrieval_service.py (970行)
   ├─ 语义检索
   │   └─ Embedding(query) → Vector DB 相似度搜索 (cosine/euclidean)
   ├─ 全文检索
   │   └─ jieba 分词 → 关键词匹配
   ├─ 混合检索
   │   └─ 语义 + 关键词 + 权重混合 (Weighted Score)
   ├─ 元数据过滤
   │   └─ MetadataFilteringCondition → 筛选候选文档范围
   └─ 后处理
       ├─ Rerank 模型重排序
       │   └─ core/rag/data_post_processor/data_post_processor.py
       ├─ Score Threshold 过滤低分结果
       └─ Top K 截断
```

### 3.3 问答流程

```
Chat 应用完整链路:
  User Input
    → Knowledge Retrieval 节点 (检索相关分段)
        → [Segment1, Segment2, Segment3, ...]
    → LLM 节点 (注入上下文)
        ├─ System Prompt: "请优先根据上下文中的知识回答"
        ├─ Context: segments.content (拼接)
        └─ User Query: original_question
    → Answer 节点
        └─ metadata.retriever_resources: [引用来源列表]
```

### 3.4 检索关键源码

| 组件 | 文件 | 行数 | 核心内容 |
|------|------|:----:|------|
| 检索服务 | `api/core/rag/datasource/retrieval_service.py` | 970 | RetrievalService — 三种检索方法 |
| 向量库工厂 | `api/core/rag/datasource/vdb/vector_factory.py` | — | 20+ VDB 后端统一接口 |
| 关键词检索 | `api/core/rag/datasource/keyword/keyword_factory.py` | — | jieba 分词 + BM25 |
| 数据后处理 | `api/core/rag/data_post_processor/data_post_processor.py` | — | Rerank + 排序 + 过滤 |
| 检索设置实体 | `api/core/rag/entities/retrieval_settings.py` | — | RetrievalModel 定义 |
| 元数据过滤 | `api/core/rag/entities/metadata_entities.py` | — | MetadataFilteringCondition |

---

## 4. 两种索引模式对比

| 维度 | high_quality | economy |
|------|:-----------:|:-------:|
| 需要 Embedding 模型 | ✅ 是 | ❌ 否 |
| 向量化 | ✅ 是 | ❌ 否 |
| 语义检索 | ✅ 支持 | ❌ 不支持 |
| 关键词检索 | ✅ 支持 | ✅ 支持 |
| 混合检索 | ✅ 支持 | ❌ 不支持 |
| Rerank | ✅ 支持 | ❌ 不支持 |
| 检索精度 | 高 | 低 |
| 成本 | 较高（Embedding 调用） | 低 |
| 当前可用 | ❌ 需配置模型供应商 | ✅ 已验证通过 |

---

## 5. 当前验证状态

| 操作 | 状态 | 备注 |
|------|:----:|------|
| 创建 economy 知识库 | ✅ | Console API 验证通过 |
| 查看知识库详情 | ✅ | 完整 JSON 返回 |
| 查看文档列表 | ✅ | 空数据集正确返回 |
| 删除知识库 | ✅ | 成功删除 |
| 上传文档 + 索引 | ⚠️ | 需 Service API Key（ApiToken bug 阻塞） |
| 语义检索 | ⚠️ | 需 embedding 模型 + API Key |
| 问答应用 | ⚠️ | 需创建 Chat 应用 + 配置知识库上下文 |
