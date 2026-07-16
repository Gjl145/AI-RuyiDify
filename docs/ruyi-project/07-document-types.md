# Dify 知识库文档支持类型

> **整理日期**: 2026-07-16
> **参考来源**: 项目源码 `api/core/rag/extractor/extract_processor.py`、`api/constants/`、`api/configs/`

---

## 一、数据来源总览

Dify 知识库支持三种数据来源：

| 来源类型 | 说明 |
|----------|------|
| 本地上传文件 | 从本地设备直接上传文档 |
| Notion 导入 | 从 Notion 工作区同步页面和数据库内容 |
| 网页抓取 | 通过 Firecrawl、WaterCrawl 或 Jina Reader 抓取网页内容 |

---

## 二、本地上传文件支持格式

### 2.1 默认提取模式（ETL_TYPE=dify，内置模式）

Dify 内置了多种文档格式的提取器，无需额外配置即可使用：

| 文件类型 | 扩展名 | 提取方式 | 说明 |
|----------|--------|----------|------|
| 纯文本 | .txt | 内置 TextExtractor | 自动检测编码，其他未匹配的扩展名也按纯文本处理 |
| Markdown | .md、.markdown、.mdx | 内置 MarkdownExtractor | 自动检测编码，保留格式结构 |
| PDF | .pdf | 内置 PdfExtractor | 使用 PyPDF2/pypdfium2 解析 |
| Word 文档 | .docx | 内置 WordExtractor | 使用 python-docx 解析 |
| Excel 表格 | .xlsx、.xls | 内置 ExcelExtractor | 提取表格数据 |
| CSV | .csv | 内置 CSVExtractor | 自动检测编码和分隔符 |
| HTML 网页 | .htm、.html | 内置 HtmlExtractor | 提取纯文本内容 |
| EPUB 电子书 | .epub | UnstructuredEpubExtractor | 解析电子书章节内容 |

### 2.2 Unstructured 模式（ETL_TYPE=Unstructured）

当配置了 Unstructured API（设置 UNSTRUCTURED_API_URL 和 UNSTRUCTURED_API_KEY 环境变量）后，额外支持以下格式：

| 文件类型 | 扩展名 | 提取方式 | 说明 |
|----------|--------|----------|------|
| 旧版 Word | .doc | UnstructuredWordExtractor | 需要 Unstructured API |
| PPT 演示文稿 | .ppt | UnstructuredPPTExtractor | 需要 Unstructured API |
| PPTX 演示文稿 | .pptx | UnstructuredPPTXExtractor | 需要 Unstructured API |
| XML 文档 | .xml | UnstructuredXmlExtractor | 需要 Unstructured API |
| Outlook 邮件 | .msg | UnstructuredMsgExtractor | 需要 Unstructured API |
| Email 邮件 | .eml | UnstructuredEmailExtractor | 需要 Unstructured API |

### 2.3 完整文件格式汇总

综合默认模式和 Unstructured 模式，Dify 共支持 17 种文件扩展名：

.txt、.md、.markdown、.mdx、.pdf、.docx、.doc、.xlsx、.xls、.csv、.htm、.html、.epub、.ppt、.pptx、.xml、.msg、.eml

---

## 三、文档处理模式

### 3.1 文档类型（doc_form）

Dify 支持两种文档处理方式：

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| text_model（文本模式） | 将文档内容按段落切分 | 制度文档、产品手册、课程讲义等连续文本 |
| qa_model（问答模式） | 将文档按问答对切分，每对提取问题和答案 | FAQ、客服对话记录等结构化问答 |

### 3.2 索引模式

| 模式 | 说明 | 推荐场景 |
|------|------|----------|
| high_quality（高质量） | 使用 Embedding 模型向量化，支持语义检索、混合检索、重排序 | 需要高精度检索的生产环境 |
| economy（经济） | 使用关键词索引，仅支持关键词匹配 | 简单场景，成本低但不支持 API 检索 |

---

## 四、文档处理规则

### 4.1 处理模式

| 模式 | 说明 |
|------|------|
| automatic（自动） | Dify 自动选择最优的分段策略，适用于大多数场景 |
| custom（自定义） | 手动指定分块参数：分隔符、最大 Token 数、重叠 Token 数 |

### 4.2 预处理规则（仅 automatic 模式）

| 规则 | 说明 |
|------|------|
| 去除多余空格和换行 | 规范化文本空白字符 |
| 去除 URL 和邮箱地址 | 清理无意义的链接信息 |

---

## 五、文件上传限制

| 限制项 | 默认值 | 环境变量 |
|--------|:------:|----------|
| 单个文件最大大小 | 15 MB | UPLOAD_FILE_SIZE_LIMIT |
| 单张图片最大大小 | 10 MB | UPLOAD_IMAGE_FILE_SIZE_LIMIT |
| 单个视频最大大小 | 100 MB | UPLOAD_VIDEO_FILE_SIZE_LIMIT |
| 单个音频最大大小 | 50 MB | UPLOAD_AUDIO_FILE_SIZE_LIMIT |
| 批量上传数量 | 5 个 | UPLOAD_FILE_BATCH_LIMIT |
| 文件扩展名黑名单 | 空（可配置） | UPLOAD_FILE_EXTENSION_BLACKLIST |
| 单文档分段最大 Token | 4000 | INDEXING_MAX_SEGMENTATION_TOKENS_LENGTH |

---

## 六、网页抓取

Dify 支持通过三种提供商抓取网页内容：

| 提供商 | 说明 |
|--------|------|
| Jina Reader | 基于 Jina AI 的网页内容提取服务，支持直接读取网页纯文本 |
| Firecrawl | 专业的网页抓取工具，支持 JavaScript 渲染页面 |
| WaterCrawl | 支持深度爬取和自定义抓取规则 |

网页抓取功能通过环境变量控制启用：ENABLE_WEBSITE_JINAREADER、ENABLE_WEBSITE_FIRECRAWL、ENABLE_WEBSITE_WATERCRAWL。

---

## 七、Notion 导入

Dify 支持从 Notion 工作区导入内容，需要先完成 Notion OAuth 授权绑定。

导入的内容类型包括：
- Notion 页面：普通文档页面，包含富文本、表格、列表等
- Notion 数据库：结构化数据，按行提取

---

## 八、多模态支持

Dify 支持多模态知识库，图片可以与文本一起进入语义检索空间：

| 项目 | 说明 |
|------|------|
| 支持格式 | JPG、PNG、GIF |
| 单图上限 | 2 MB（Markdown 中引用的图片） |
| 检索类型 | Image-to-Text、Text-to-Image、Image-to-Image |
| 适用场景 | 产品照片、架构图、截图、培训手册等含图资料 |

多模态检索需要在 Markdown 文档中通过标准图片语法引用图片文件，Dify 会自动抽取并向量化。

---

## 九、语言支持

| 项目 | 说明 |
|------|------|
| 中文 | 内置 jieba 分词，支持中文关键词提取 |
| 英文 | 标准分词 |
| 其他 | 通过文档语言设置（doc_language）指定，影响分段策略 |

---

## 十、总结

Dify 知识库的文档处理能力覆盖了办公场景的主流格式：

- 文本格式：TXT、Markdown、HTML、XML
- 办公文档：PDF、Word（docx/doc）、Excel（xlsx/xls）、CSV
- 演示文稿：PPT、PPTX
- 邮件：MSG、EML
- 电子书：EPUB
- 网页：通过 Jina Reader、Firecrawl、WaterCrawl 抓取
- 在线协作：Notion 导入
- 多模态：JPG、PNG、GIF 图片

内置模式（默认）支持 8 种格式，配合 Unstructured API 扩展到 16 种。加上网页抓取和 Notion 导入，基本覆盖了企业和个人知识管理的主要数据来源。
