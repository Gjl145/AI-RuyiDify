"""文档读取与提取 — 结构化提取文档内容

用法:
    from src.docx import DocReader

    reader = DocReader("input.docx")
    print(reader.text)           # 全文
    print(reader.paragraphs)     # 段落列表
    print(reader.tables_data)    # 表格数据
    print(reader.metadata)       # 元信息
    reader.to_markdown("out.md") # 导出 Markdown
"""

from pathlib import Path

from docx import Document


class DocReader:
    """读取并提取 Word 文档内容"""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"文件不存在: {self.path}")
        self.doc = Document(str(self.path))

    # ── 文本 ──────────────────────────────────

    @property
    def text(self) -> str:
        """全文纯文本"""
        return "\n".join(p.text for p in self.doc.paragraphs if p.text.strip())

    @property
    def paragraphs(self) -> list[str]:
        """段落列表（非空）"""
        return [p.text for p in self.doc.paragraphs if p.text.strip()]

    @property
    def headings(self) -> list[dict]:
        """提取所有标题及其层级"""
        result = []
        for p in self.doc.paragraphs:
            if p.style.name.startswith("Heading"):
                level = int(p.style.name.split()[-1]) if p.style.name.split()[-1].isdigit() else 1
                result.append({"level": level, "text": p.text})
        return result

    # ── 表格 ──────────────────────────────────

    @property
    def tables_data(self) -> list[list[list[str]]]:
        """所有表格数据"""
        return [[[cell.text for cell in row.cells] for row in t.rows] for t in self.doc.tables]

    # ── 图片 ──────────────────────────────────

    @property
    def images(self) -> list[bytes]:
        """提取所有嵌入图片的二进制数据"""
        result = []
        for rel in self.doc.part.rels.values():
            if "image" in rel.reltype:
                result.append(rel.target_part.blob)
        return result

    # ── 元信息 ────────────────────────────────

    @property
    def metadata(self) -> dict:
        """文档属性"""
        props = self.doc.core_properties
        return {
            "author": props.author,
            "created": str(props.created),
            "modified": str(props.modified),
            "title": props.title,
            "paragraphs": len(self.doc.paragraphs),
            "tables": len(self.doc.tables),
            "sections": len(self.doc.sections),
        }

    # ── 导出 ────────────────────────────────

    def to_markdown(self, output_path: str | Path | None = None) -> str:
        """导出为 Markdown"""
        md = []
        for p in self.doc.paragraphs:
            text = p.text.strip()
            if not text:
                md.append("")
                continue
            if p.style.name.startswith("Heading"):
                level = int(p.style.name.split()[-1]) if p.style.name.split()[-1].isdigit() else 1
                md.append("#" * level + " " + text)
            else:
                md.append(text)
        result = "\n".join(md)
        if output_path:
            Path(output_path).write_text(result, encoding="utf-8")
            print(f"已导出: {output_path}")
        return result
