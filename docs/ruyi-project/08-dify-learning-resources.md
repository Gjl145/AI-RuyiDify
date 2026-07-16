# Dify 学习资料大全

> 整理日期：2026-07-16
> 涵盖官方文档、视频教程、社区资源、实战课程、技术博客和开源项目

---

## 一、官方资源

### 1.1 官方文档

Dify 官方提供了完整的多语言文档体系：

| 资源 | 地址 | 说明 |
|------|------|------|
| 中文文档 | https://docs.dify.ai/zh | 官方中文文档，覆盖安装、配置、使用全流程 |
| 英文文档 | https://docs.dify.ai/en | 官方英文文档，内容最新最全 |
| API 参考 | https://docs.dify.ai/zh/api-reference | 知识库 API、应用 API、工作流 API |

### 1.2 官方博客

| 文章 | 说明 |
|------|------|
| Knowledge Pipeline 介绍 | https://dify.ai/blog/introducing-knowledge-pipeline |
| 多模态知识库 | https://dify.ai/blog/multimodal-retrieval-is-now-available-in-the-knowledge-base |

---

## 二、视频教程

### 2.1 官方频道

| 平台 | 内容 |
|------|------|
| Bilibili | 搜索"Dify 教程"，官方和社区有大量入门到进阶视频 |
| YouTube | Dify 官方频道，英文教程为主 |

### 2.2 推荐学习路径

1. 入门篇：Dify 是什么、如何安装部署、创建第一个应用
2. 知识库篇：上传文档、切分配置、检索调参、RAG 原理
3. 工作流篇：Chatflow 编排、节点类型、变量传递、条件分支
4. Agent 篇：工具调用、ReAct 模式、自定义插件
5. API 篇：知识库 API、应用 API、自动化集成

---

## 三、核心技术概念

### 3.1 RAG（检索增强生成）

RAG 是 Dify 知识库的核心机制，完整链路为：

文档上传 → 文档切分（Chunking） → 向量化（Embedding） → 向量数据库存储 → 用户查询 → 语义检索 → 上下文注入 → LLM 生成回答

### 3.2 知识库两大模式

| 模式 | 适用场景 | 优势 | 劣势 |
|------|----------|------|------|
| high_quality | 生产环境 | 语义检索、混合检索、Rerank | 需要 Embedding 模型 |
| economy | 简单场景 | 低成本、无需 Embedding | 不支持 API 检索 |

### 3.3 检索参数调优

| 参数 | 作用 | 建议 |
|------|------|------|
| Top K | 返回结果数量 | 段落多时适当增大（5→20） |
| Score Threshold | 最低相似度门槛 | 过滤噪音，但可能漏掉信息 |
| Rerank | 重排序 | 提升结果相关性，增加成本 |

### 3.4 支持的模型供应商

Dify 支持 100+ 模型供应商，包括：
- OpenAI（GPT 系列）
- Anthropic（Claude 系列）
- DeepSeek
- 通义千问
- SiliconFlow（硅基流动）
- 智谱 AI（ChatGLM）
- 百度文心一言
- 本地部署模型（Ollama、vLLM 等）

---

## 四、文档处理能力

### 4.1 支持的文件格式

Dify 知识库支持 17 种文件扩展名：
.txt、.md、.markdown、.mdx、.pdf、.docx、.doc、.xlsx、.xls、.csv、.htm、.html、.epub、.ppt、.pptx、.xml、.msg、.eml

### 4.2 数据来源

| 来源 | 说明 |
|------|------|
| 本地上传 | 支持上述 17 种格式 |
| Notion 导入 | 同步 Notion 页面和数据库 |
| 网页抓取 | 通过 Firecrawl、WaterCrawl、Jina Reader |
| 多模态 | Markdown 中引用 JPG/PNG/GIF 图片 |

---

## 五、社区与开源

### 5.1 社区渠道

| 渠道 | 地址 |
|------|------|
| GitHub | https://github.com/langgenius/dify |
| Discord | Dify 官方 Discord 社区 |
| 知乎 | 搜索"Dify"相关文章和问答 |
| 微信公众号 | 关注 Dify 官方公众号 |

### 5.2 开源生态

| 项目 | 说明 |
|------|------|
| dify-plugin-daemon | Dify 插件运行时 |
| dify-sandbox | 代码执行沙箱 |
| dify-agent | Agent 运行时（AgentOn 框架） |

---

## 六、实战课程推荐

### 6.1 RuyiDify 课程体系

RuyiDify 是一套基于 Dify 的知识库开发实战课程，核心内容：

1. Dify 环境搭建（Docker Compose 部署）
2. 模型供应商配置（对话模型 + Embedding 模型）
3. 知识库创建与文档上传
4. 检索调参与质量优化
5. API 脚本化操作
6. Chatflow 工作流编排
7. 企业级 RAG 系统设计

### 6.2 推荐学习顺序

1. 先看官方文档了解基本概念
2. 跟着视频教程完成第一个应用
3. 阅读 RuyiDify 项目文档理解架构
4. 动手写脚本实现自动化操作
5. 在实际项目中应用和优化

---

## 七、知识库 API 速查

Dify 知识库提供 42 个 API 端点，分 7 大类：

| 类别 | 数量 | 典型操作 |
|------|:----:|----------|
| 知识库 CRUD | 5 | 创建、列表、详情、更新、删除 |
| 文档管理 | 12 | 上传文件/文本、列表、下载、索引状态 |
| 分段管理 | 9 | 增删改查、子分段、启用/禁用 |
| 检索 | 1 | 语义/全文/混合检索 |
| 元数据 | 7 | 自定义字段、内置元数据、批量写入 |
| 标签 | 7 | 标签 CRUD、绑定/解绑 |
| 模型查询 | 1 | 查询可用模型 |

---

## 八、常见问题

**Q: economy 和 high_quality 怎么选？**
A: 开发测试用 economy（低成本），生产环境用 high_quality（支持语义检索和 API 调用）。

**Q: 知识库检索结果为空怎么办？**
A: 检查索引是否完成、Embedding 模型是否可用、检索参数是否合理（Top K 太小、Score Threshold 太高）。

**Q: 如何提高检索准确度？**
A: 调整分段策略、优化 Top K 和 Score Threshold、启用 Rerank 模型、使用元数据过滤缩小范围。

**Q: 可以不用界面操作知识库吗？**
A: 可以，Dify 提供完整的知识库 API（42 个端点），支持 Python 脚本全自动化操作。
