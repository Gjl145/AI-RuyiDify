"""集成测试 — 验证 src.docx 全部功能"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.docx import DocCreator, DocEditor, DocTemplate, DocReader

OUT = Path(__file__).resolve().parent / "test_output"
OUT.mkdir(exist_ok=True)

# ── 1. Creator — 创建新文档 ──────────────────
print("=== 1. Creator ===")
doc = DocCreator(OUT / "01_created.docx")
doc.set_page(margin_cm=2)
doc.add_title("测试文档")
doc.add_heading("第一节 段落", level=1)
doc.add_paragraph("这是一段普通正文。")
doc.add_paragraph("这是红色加粗文字", bold=True, color="#CC0000")
doc.add_heading("项目列表", level=2)
doc.add_bullet(["第一项", "第二项", "第三项"])
doc.add_heading("编号列表", level=2)
doc.add_numbered(["步骤一", "步骤二", "步骤三"])
doc.add_heading("表格", level=2)
doc.add_table([
    ["姓名", "成绩", "等级"],
    ["张三", "95", "优秀"],
    ["李四", "78", "良好"],
])
doc.save()
print("  ✅ 创建 01_created.docx")

# ── 2. Reader — 读取文档 ─────────────────────
print("\n=== 2. Reader ===")
reader = DocReader(OUT / "01_created.docx")
assert "测试文档" in reader.text
assert len(reader.headings) >= 3
assert len(reader.tables_data) >= 1
md = reader.to_markdown(OUT / "01_created.md")
assert "测试文档" in md
print(f"  ✅ 段落:{len(reader.paragraphs)} 标题:{len(reader.headings)} 表格:{len(reader.tables_data)}")
print(f"  ✅ 导出 Markdown: {OUT / '01_created.md'}")

# ── 3. Editor — 编辑文档 ─────────────────────
print("\n=== 3. Editor ===")
editor = DocEditor(OUT / "01_created.docx")
editor.replace_text("测试文档", "验证文档")
editor.replace_text("张三", "王五")
editor.add_paragraph("本文档由 DocEditor 自动修改生成。", position="start")
editor.save(OUT / "02_edited.docx")
# 验证修改 (表格内文本需单独验证)
reader2 = DocReader(OUT / "02_edited.docx")
assert "验证文档" in reader2.text
assert "DocEditor" in reader2.text
# 验证表格替换
table_text = " ".join(cell.text for row in reader2.doc.tables[0].rows for cell in row.cells)
assert "王五" in table_text
print("  ✅ 编辑 02_edited.docx")

# ── 4. Template — 模板渲染 ────────────────────
print("\n=== 4. Template ===")
# 直接用 DocCreator 做一个简单模板
doc = DocCreator(OUT / "template.docx")
doc.add_title("{{ title }}")
doc.add_paragraph("姓名: {{ name }}    成绩: {{ score }}")
doc.add_bullet(["{% for i in items %}{{ i }}{% endfor %}"])
doc.save()

tmpl = DocTemplate(OUT / "template.docx")
tmpl.render({"title": "成绩单", "name": "赵六", "score": 88, "items": ["作业1", "作业2", "考试"]})
tmpl.save(OUT / "03_rendered.docx")
reader3 = DocReader(OUT / "03_rendered.docx")
assert "成绩单" in reader3.text
assert "赵六" in reader3.text
print("  ✅ 模板渲染 03_rendered.docx")

print(f"\n全部通过！输出目录: {OUT}")
