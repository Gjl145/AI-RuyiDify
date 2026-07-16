"""模板渲染 — 基于 Jinja2 模板批量生成文档

用法:
    from src.docx import DocTemplate

    tmpl = DocTemplate("template.docx")
    tmpl.render({"name": "张三", "score": 95, "items": ["任务1", "任务2"]})
    tmpl.save("output.docx")

模板语法 (在 docx 中直接写 Jinja2):
    {{ name }}          — 变量替换
    {% for item in items %} ... {% endfor %}  — 循环
    {% if score > 60 %} 及格 {% endif %}       — 条件
"""

from pathlib import Path
from typing import Any

from docxtpl import DocxTemplate


class DocTemplate:
    """基于 docxtpl 的模板文档渲染器"""

    def __init__(self, template_path: str | Path):
        self.tpl = DocxTemplate(str(template_path))

    def render(self, context: dict[str, Any]):
        """填充模板"""
        self.tpl.render(context)
        return self

    def render_to_new(self, context: dict[str, Any], output_path: str | Path):
        """直接渲染到新文件"""
        self.render(context)
        self.save(output_path)

    def save(self, path: str | Path):
        """保存渲染结果"""
        self.tpl.save(str(path))
        print(f"已保存: {path}")


def make_template(content: dict[str, str], path: str = "template.docx"):
    """快速创建一个模板文件

    content = {
        "title": "{{ title }}",
        "body": "{{ name }} 成绩为 {{ score }}",
        "table": [["项目", "状态"], ["{% for i in items %}{{ i }}{% endfor %}", ""]],
    }
    """
    from .creator import DocCreator
    doc = DocCreator(path)
    if "title" in content:
        doc.add_title(content["title"])
    if "body" in content:
        doc.add_paragraph(content["body"])
    if "table" in content:
        doc.add_table(content["table"])
    doc.save()
    print(f"模板已创建: {path}")
