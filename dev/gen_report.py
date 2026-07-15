"""生成 RuyiDify 知识库实战记录 Word 文档"""
# ruff: noqa: E701, E702
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# ===== 封面 =====
for _ in range(2): doc.add_paragraph()
t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run('RuyiDify 知识库实战记录'); r.font.size = Pt(28); r.bold = True
t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run('从零构建 Dify 知识库并实现 AI 问答'); r.font.size = Pt(14); r.font.color.rgb = RGBColor(100, 100, 100)
doc.add_paragraph()
t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
t.add_run('2026年7月15日').font.size = Pt(12)
doc.add_paragraph()
t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run('Dify v1.15.0 + DeepSeek v4 Pro + SiliconFlow BAAI/bge-m3 | Docker Compose · Windows 10')
r.font.size = Pt(10); r.font.color.rgb = RGBColor(130, 130, 130)
doc.add_page_break()

# ===== 目录 =====
doc.add_heading('目录', level=1)
for i, item in enumerate(['练习目标与任务概述', '环境准备与 Bug 修复', '任务一：收集接口形成文档',
    '任务二：上传文档到知识库', '任务三：AI 通过知识库查询', '遇到的 10 个关键问题',
    'Prompt 提示词汇总', '最终成果验证', '关键收获与 RAG 认知'], 1):
    doc.add_paragraph(f'{i}. {item}')
doc.add_page_break()

# ===== 一、目标 =====
doc.add_heading('一、练习目标与任务概述', level=1)
doc.add_paragraph('三个子任务：')
doc.add_paragraph('任务 1：收集 Dify 知识库相关接口，形成《Dify 知识库接口文档》')
doc.add_paragraph('任务 2：将文档上传到 Dify 知识库，完成切分、向量化和索引')
doc.add_paragraph('任务 3：通过聊天助手查询知识库，验证 AI 能否准确回答')
doc.add_heading('技术架构', level=2)
doc.add_paragraph('LLM：DeepSeek v4 Pro — 理解问题、生成回答')
doc.add_paragraph('Embedding：SiliconFlow BAAI/bge-m3 — 文本转向量')
doc.add_paragraph('向量数据库：Weaviate 1.27.0 — 存储向量、语义检索')
doc.add_paragraph('应用框架：Dify v1.15.0 — 低代码编排')
doc.add_paragraph('部署方式：Docker Compose（12 容器）')
doc.add_page_break()

# ===== 二、环境 =====
doc.add_heading('二、环境准备与 Bug 修复', level=1)
doc.add_heading('2.1 Docker', level=2)
doc.add_paragraph('Docker 29.6.1 + Compose v5.2.0 | 12 个容器：api, web, worker, worker_beat, db_postgres, redis, weaviate, sandbox, nginx, plugin_daemon, ssrf_proxy')
doc.add_paragraph('启动：cd docker && docker compose --profile postgresql --profile weaviate up -d')
doc.add_paragraph('访问：http://localhost | 账号：admin@ruyidify.local')
doc.add_heading('2.2 模型配置', level=2)
doc.add_paragraph('DeepSeek：API Key → 对话生成（deepseek-v4-pro）')
doc.add_paragraph('SiliconFlow：API Key → 嵌入向量（BAAI/bge-m3，免费）')
doc.add_heading('2.3 Bug 修复', level=2)
doc.add_paragraph('Bug 1：ApiToken 缺 dataset_id → api/models/model.py L2248 补 mapped_column + DB ALTER TABLE')
doc.add_paragraph('Bug 2：sites 缺 input_placeholder → ALTER TABLE sites ADD COLUMN input_placeholder')
doc.add_page_break()

# ===== 三、任务一 =====
doc.add_heading('三、任务一：收集接口形成文档', level=1)
doc.add_heading('3.1 数据来源', level=2)
doc.add_paragraph('• Dify 官方文档：https://docs.dify.ai/zh/api-reference/guides/knowledge')
doc.add_paragraph('• 源码：api/controllers/service_api/dataset/（5 个控制器文件）')
doc.add_paragraph('• 示例代码：examples/知识库/（29 个 Python 脚本）')
doc.add_heading('3.2 分析方法', level=2)
doc.add_paragraph('1. 逐文件提取 @service_api_ns.route 装饰器中的路径')
doc.add_paragraph('2. 交叉验证示例脚本中实际调用的 URL')
doc.add_paragraph('3. 按功能分组归类，统计各类端点数量')
doc.add_heading('3.3 产出', level=2)
doc.add_paragraph('文件：docs/ruyi-project/06-knowledge-api-reference.md（8,390 字符，217 行）')
table = doc.add_table(rows=8, cols=3, style='Light Grid Accent 1')
h = table.rows[0].cells; h[0].text = '类别'; h[1].text = '数量'; h[2].text = '说明'
for i, (cat, n, desc) in enumerate([
    ('知识库 CRUD', '5', '创建、列表、详情、更新、删除'),
    ('文档管理', '12', '上传/更新/下载/索引状态/批量'),
    ('分段管理', '9', '增删改查+子分段+启用/禁用'), ('检索', '1', '语义/全文/混合检索'),
    ('元数据', '7', '自定义+内置+批量写入'), ('标签', '7', 'CRUD+绑定/解绑'),
    ('模型查询', '1', '查询 Embedding/Rerank 模型'),
]): r = table.rows[i + 1].cells; r[0].text = cat; r[1].text = n; r[2].text = desc
doc.add_paragraph('合计：42 个端点')
doc.add_page_break()

# ===== 四、任务二 =====
doc.add_heading('四、任务二：上传文档到知识库', level=1)
doc.add_heading('4.1 economy 模式（失败）', level=2)
doc.add_paragraph('• 创建知识库「RuyiDify课程资料」，economy 模式')
doc.add_paragraph('• 通过 API POST /v1/datasets/{id}/document/create-by-text 上传')
doc.add_paragraph('• 首次上传被 Shell 转义截断，重新上传后索引完成（19 段）')
doc.add_paragraph('• 检索测试：全部返回 0 条 → economy 不支持 API 语义检索')
doc.add_heading('4.2 切换 high_quality（成功）', level=2)
doc.add_paragraph('• 在 Dify Web UI 配置 SiliconFlow BAAI/bge-m3 嵌入模型')
doc.add_paragraph('• 通过 API PATCH 切换为 high_quality 模式')
doc.add_paragraph('• 删除旧文档，重新上传 → high_quality 下重新索引')
doc.add_paragraph('• 索引完成：19 段向量化，语义检索生效')
doc.add_paragraph('• 检索 score：0.73（标题段）、0.63（「42 个端点」段）')
doc.add_page_break()

# ===== 五、任务三 =====
doc.add_heading('五、任务三：AI 通过知识库查询', level=1)
doc.add_heading('5.1 应用配置', level=2)
doc.add_paragraph('• 类型：聊天助手（Chat Assistant）')
doc.add_paragraph('• 模型：DeepSeek v4 Pro | 知识库：RuyiDify课程资料')
doc.add_paragraph('• 检索：语义检索，Top K=20')
doc.add_heading('5.2 使用的 Prompt', level=2)
p = doc.add_paragraph()
p.add_run('你是文档查询助手，只根据上下文中的资料回答问题。资料不足时明确说明不知道。列出清单类问题时，必须逐段扫描所有上下文，确保不遗漏任何条目。').font.size = Pt(9)
doc.add_heading('5.3 测试结果', level=2)
t2 = doc.add_table(rows=6, cols=2, style='Light Grid Accent 1')
t2.rows[0].cells[0].text = '问题'; t2.rows[0].cells[1].text = 'AI 回答'
for i, (q, a) in enumerate([
    ('Dify 知识库有多少个接口', '42 个端点，7 大类'),
    ('怎么删除文档', 'DELETE /datasets/{id}/documents/{doc_id}'),
    ('文档管理有哪些操作', '列出 11 项操作'),
    ('索引完成后状态是什么', 'completed'),
    ('语义检索需要什么参数', 'query + retrieval_model(semantic_search) + top_k + score_threshold'),
]): t2.rows[i + 1].cells[0].text = q; t2.rows[i + 1].cells[1].text = a
doc.add_page_break()

# ===== 六、问题 =====
doc.add_heading('六、遇到的 10 个关键问题', level=1)
problems = [
    ('1. Docker Desktop 未运行', 'Docker 是 GUI 应用，需开始菜单手动启动。'),
    ('2. Git 仓库缺失', '无 .git 目录 → git init → commit → push 到 GitHub。'),
    ('3. ApiToken 缺 dataset_id', '模型漏声明列 → 补 mapped_column + DB ALTER TABLE。'),
    ('4. sites 缺 input_placeholder', 'DB 迁移未跑全 → 手动 ALTER TABLE 补列。'),
    ('5. economy 无法检索', 'economy 不支持 API 检索 → 切 high_quality + 配 Embedding 模型。'),
    ('6. SiliconFlow 余额为 0', 'embedding 返回 403 → 充值后恢复。'),
    ('7. Shell 转义截断文档', 'curl -d 时内容被截断 → 用 Python json.dumps 编码后上传。'),
    ('8. CSRF Token 过期', '登录态超时 → 重新 login 刷新 Cookie 和 CSRF Token。'),
    ('9. DSL 导入配置复杂', '工作流导入后节点配置不对 → API 获取 draft → 改 JSON → POST 更新 → 发布。'),
    ('10. 「列出所有」漏条目', 'RAG 固有限制，信息分散多段 → 调大 Top K + 改用精准单问。'),
]
for title, desc in problems:
    doc.add_heading(title, level=2)
    doc.add_paragraph(desc)
doc.add_page_break()

# ===== 七、Prompts =====
doc.add_heading('七、Prompt 提示词汇总', level=1)
prompts = [
    ('聊天助手 System Prompt',
     '你是文档查询助手，只根据上下文中的资料回答问题。\n规则：\n1. 只能使用上下文中的信息，绝对禁止使用外部知识或猜测。\n2. 如果资料中没有相关信息，直接回答"当前资料中未找到相关内容"。\n3. 回答要简洁、完整，有数字就给数字，有分类就列分类。\n4. 回答语言与用户问题保持一致。'),
    ('LLM 节点 Prompt（工作流）',
     '你是严格的文档查询助手。只根据上下文中的知识库检索结果回答。\n规则：1. 只用上下文信息。2. 找不到就说"未找到"。3. 简洁准确，列依据。'),
    ('测试查询',
     '• Dify 知识库有多少个接口\n• 列出所有 POST 方法的接口\n• 知识库 API 分为哪几类\n• 文档管理有哪些操作\n• 怎么删除文档\n• 语义检索需要什么参数'),
]
for title, content in prompts:
    doc.add_heading(title, level=2)
    p = doc.add_paragraph(); p.add_run(content).font.size = Pt(9)
doc.add_page_break()

# ===== 八 =====
doc.add_heading('八、最终成果验证', level=1)
doc.add_paragraph('✅ 任务1：《Dify 知识库接口文档》（docs/ruyi-project/06-knowledge-api-reference.md）')
doc.add_paragraph('   42 个端点，7 大类，每类附带示例和参数说明')
doc.add_paragraph('✅ 任务2：文档上传到知识库「RuyiDify课程资料」')
doc.add_paragraph('   high_quality + BAAI/bge-m3，19 分段，语义检索 score 0.73')
doc.add_paragraph('✅ 任务3：AI 聊天助手查询知识库')
doc.add_paragraph('   Q: Dify 知识库有多少个接口？→ A: 42 个端点，7 大类')
doc.add_page_break()

# ===== 九 =====
doc.add_heading('九、关键收获与 RAG 认知', level=1)
doc.add_heading('RAG 核心链路', level=2)
doc.add_paragraph('文档 → 切分(Chunking) → 向量化(Embedding) → 存储(Vector DB) → 检索(Retrieval) → 增强(Augment) → 生成(Generation)')
doc.add_heading('RAG 优势场景', level=2)
doc.add_paragraph('精准问答、归纳总结、代码生成、对比分析')
doc.add_heading('RAG 局限性', level=2)
doc.add_paragraph('「列出所有」类枚举易遗漏；依赖 Top K 和 Embedding 质量')
doc.add_heading('调优经验', level=2)
doc.add_paragraph('• Top K 随段落数调整（本次从 5→20，效果明显）')
doc.add_paragraph('• Prompt 中要求「逐段扫描」可减少遗漏')
doc.add_paragraph('• economy 不适合生产，用 high_quality')
doc.add_paragraph('• 文档结构应每类自包含在一个段落中')

# 保存
doc.save('D:/ai/RuyiDify/docs/ruyi-project/RuyiDify知识库实战记录.docx')
print('SAVED OK')
