"""文档编辑与修改 — 打开已有文档进行增删改

用法:
    from src.docx import DocEditor

    editor = DocEditor("input.docx")
    editor.replace_text("旧文本", "新文本")
    editor.insert_after("关键词", "插入的内容")
    editor.delete_paragraph_containing("删除包含此词")
    editor.save("output.docx")
"""

from pathlib import Path

from docx import Document


class DocEditor:
    """编辑已有的 Word 文档"""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"文件不存在: {self.path}")
        self.doc = Document(str(self.path))

    # ── 文本替换 ──────────────────────────────

    def replace_text(self, old: str, new: str, whole_word: bool = False):
        """全文替换文本（段落 + 表格）"""
        count = 0
        count += self._replace_in_paragraphs(old, new, whole_word)
        count += self._replace_in_tables(old, new, whole_word)
        count += self._replace_in_headers_footers(old, new)
        print(f"替换 {count} 处")
        return count

    def _replace_in_paragraphs(self, old: str, new: str, whole_word: bool) -> int:
        count = 0
        for p in self.doc.paragraphs:
            if old in p.text:
                for run in p.runs:
                    if old in run.text:
                        if whole_word:
                            import re
                            run.text = re.sub(r'\b' + re.escape(old) + r'\b', new, run.text)
                        else:
                            run.text = run.text.replace(old, new)
                        count += 1
        return count

    def _replace_in_tables(self, old: str, new: str, whole_word: bool) -> int:
        count = 0
        for table in self.doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        if old in p.text:
                            for run in p.runs:
                                if old in run.text:
                                    run.text = run.text.replace(old, new)
                                    count += 1
        return count

    def _replace_in_headers_footers(self, old: str, new: str) -> int:
        count = 0
        for section in self.doc.sections:
            for place in [section.header, section.footer, section.first_page_header, section.first_page_footer]:
                if place is None:
                    continue
                for p in place.paragraphs:
                    for run in p.runs:
                        if old in run.text:
                            run.text = run.text.replace(old, new)
                            count += 1
        return count

    # ── 插入 ──────────────────────────────────

    def insert_after(self, keyword: str, text: str):
        """在包含关键词的段落之后插入新段落"""
        for i, p in enumerate(self.doc.paragraphs):
            if keyword in p.text:
                self.doc.paragraphs[i].insert_paragraph_after(text)
                return True
        return False

    def add_paragraph(self, text: str, position: str = "end"):
        """添加段落。position: 'end'(末尾) 或 'start'(开头)"""
        if position == "start":
            self.doc.paragraphs[0].insert_paragraph_before(text)
        else:
            self.doc.add_paragraph(text)

    # ── 修改 ──────────────────────────────────

    def set_text_bold(self, keyword: str):
        """将包含关键词的文本设为粗体"""
        for p in self.doc.paragraphs:
            if keyword in p.text:
                for run in p.runs:
                    if keyword in run.text:
                        run.bold = True

    # ── 删除 ──────────────────────────────────

    def delete_paragraph_containing(self, keyword: str):
        """删除包含关键词的段落（表格内不处理）"""
        for p in self.doc.paragraphs:
            if keyword in p.text:
                p._element.getparent().remove(p._element)

    # ── 合并 ──────────────────────────────────

    def append_document(self, other_path: str | Path):
        """将另一个文档追加到末尾"""
        other = Document(str(other_path))
        for element in other.element.body:
            self.doc.element.body.append(element)

    # ── 保存 ──────────────────────────────────

    def save(self, path: str | Path | None = None):
        target = Path(path) if path else self.path
        self.doc.save(str(target))
        print(f"已保存: {target}")
